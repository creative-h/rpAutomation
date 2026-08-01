from typing import Optional
import json
import os
from ldap.connection import LDAPConnection


class OUManager:
    """Active Directory Organizational Unit management"""
    
    def __init__(self, ldap_connection: LDAPConnection):
        """Initialize OU manager with connection"""
        self.connection = ldap_connection
        self.ou_mapping = self._load_ou_mapping()
    
    def _load_ou_mapping(self) -> dict:
        """Load location to OU mapping from JSON file"""
        config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config/groups.json')
        with open(config_path, 'r') as f:
            config = json.load(f)
        return config.get('location_ou_mapping', {})
    
    def get_ou_for_location(self, location: str) -> str:
        """Get OU path for a specific location"""
        if not location:
            return self.ou_mapping.get('DEFAULT')
        
        return self.ou_mapping.get(location.upper(), self.ou_mapping.get('DEFAULT'))
    
    def move_user_to_ou(self, user_dn: str, target_ou: str) -> bool:
        """Move user to a different Organizational Unit"""
        if not self.connection.is_connected():
            return False
        
        try:
            # Extract the CN (Common Name) from the current DN
            cn = user_dn.split(',')[0]
            new_dn = f"{cn},{target_ou}"
            
            # Move the user object
            self.connection.get_connection().modify_dn(
                user_dn,
                new_dn,
                new_superior=target_ou
            )
            return True
        except Exception as e:
            print(f"Move user to OU failed: {str(e)}")
            return False
    
    def create_ou(self, ou_path: str) -> bool:
        """Create a new Organizational Unit"""
        if not self.connection.is_connected():
            return False
        
        try:
            # Split the OU path and create from top to bottom
            ou_parts = ou_path.split(',')
            base_dn = ','.join(ou_parts[1:])  # Everything except the first OU
            
            for i in range(len(ou_parts)):
                current_ou = ','.join(ou_parts[:i+1])
                current_base = ','.join(ou_parts[i+1:]) if i+1 < len(ou_parts) else ''
                
                ou_name = ou_parts[i].split('=')[1]
                ou_dn = f"OU={ou_name},{current_base}" if current_base else f"OU={ou_name}"
                
                # Check if OU already exists
                try:
                    self.connection.get_connection().search(
                        search_base=ou_dn,
                        search_filter='(objectClass=organizationalUnit)',
                        search_scope='BASE'
                    )
                    if not self.connection.get_connection().entries:
                        # Create the OU
                        self.connection.get_connection().add(
                            ou_dn,
                            attributes={'objectClass': 'organizationalUnit'}
                        )
                except:
                    # Create the OU if search fails
                    self.connection.get_connection().add(
                        ou_dn,
                        attributes={'objectClass': 'organizationalUnit'}
                    )
            
            return True
        except Exception as e:
            print(f"Create OU failed: {str(e)}")
            return False
    
    def get_user_ou(self, user_dn: str) -> Optional[str]:
        """Get the OU path for a user"""
        if not user_dn:
            return None
        
        # Extract OU from DN (everything after the first comma)
        parts = user_dn.split(',')
        if len(parts) > 1:
            return ','.join(parts[1:])
        return None
    
    def list_ous(self, base_dn: str = None) -> list:
        """List all OUs under a base DN"""
        if not self.connection.is_connected():
            return []
        
        base_dn = base_dn or self.connection.get_base_dn()
        
        try:
            self.connection.get_connection().search(
                search_base=base_dn,
                search_filter='(objectClass=organizationalUnit)',
                search_scope='SUBTREE',
                attributes=['distinguishedName']
            )
            
            return [str(entry.distinguishedName) for entry in self.connection.get_connection().entries]
        except Exception as e:
            print(f"List OUs failed: {str(e)}")
            return []
