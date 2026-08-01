from ldap3 import MODIFY_ADD
from typing import List, Optional
import json
import os
from ldap.connection import LDAPConnection
from ldap.search import LDAPSearch


class GroupManager:
    """Active Directory security group management"""
    
    def __init__(self, ldap_connection: LDAPConnection):
        """Initialize group manager with connection"""
        self.connection = ldap_connection
        self.search = LDAPSearch(ldap_connection)
        self.group_mapping = self._load_group_mapping()
        self.default_groups = self._load_default_groups()
    
    def _load_group_mapping(self) -> dict:
        """Load department to group mapping from JSON file"""
        config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config/groups.json')
        with open(config_path, 'r') as f:
            config = json.load(f)
        return config.get('department_group_mapping', {})
    
    def _load_default_groups(self) -> List[str]:
        """Load default groups from JSON file"""
        config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config/groups.json')
        with open(config_path, 'r') as f:
            config = json.load(f)
        return config.get('default_groups', [])
    
    def get_groups_for_department(self, department: str) -> List[str]:
        """Get security groups for a specific department"""
        groups = self.default_groups.copy()
        
        # Add department-specific group if mapping exists
        dept_group = self.group_mapping.get(department.upper())
        if dept_group:
            groups.append(dept_group)
        
        return groups
    
    def get_group_dn(self, group_name: str) -> Optional[str]:
        """Get distinguished name for a security group"""
        if not self.connection.is_connected():
            return None
        
        base_dn = self.connection.get_base_dn()
        search_filter = f"(sAMAccountName={group_name})"
        
        try:
            self.connection.get_connection().search(
                search_base=base_dn,
                search_filter=search_filter,
                search_scope='SUBTREE',
                attributes=['distinguishedName']
            )
            
            if self.connection.get_connection().entries:
                return str(self.connection.get_connection().entries[0].distinguishedName)
            return None
        except Exception as e:
            print(f"Get group DN failed: {str(e)}")
            return None
    
    def add_user_to_group(self, user_dn: str, group_name: str) -> bool:
        """Add user to a security group"""
        if not self.connection.is_connected():
            return False
        
        group_dn = self.get_group_dn(group_name)
        if not group_dn:
            print(f"Group {group_name} not found")
            return False
        
        try:
            self.connection.get_connection().modify(
                group_dn,
                {'member': [(MODIFY_ADD, user_dn)]}
            )
            return True
        except Exception as e:
            print(f"Add user to group failed: {str(e)}")
            return False
    
    def remove_user_from_group(self, user_dn: str, group_name: str) -> bool:
        """Remove user from a security group"""
        if not self.connection.is_connected():
            return False
        
        group_dn = self.get_group_dn(group_name)
        if not group_dn:
            print(f"Group {group_name} not found")
            return False
        
        try:
            self.connection.get_connection().modify(
                group_dn,
                {'member': [(MODIFY_DELETE, user_dn)]}
            )
            return True
        except Exception as e:
            print(f"Remove user from group failed: {str(e)}")
            return False
    
    def assign_user_groups(self, user_dn: str, department: str, additional_groups: List[str] = None) -> bool:
        """Assign all required groups to a user"""
        groups = self.get_groups_for_department(department)
        
        if additional_groups:
            groups.extend(additional_groups)
        
        success = True
        for group in groups:
            if not self.add_user_to_group(user_dn, group):
                print(f"Failed to add user to group: {group}")
                success = False
        
        return success
    
    def get_user_groups(self, user_dn: str) -> List[str]:
        """Get all groups a user is member of"""
        if not self.connection.is_connected():
            return []
        
        try:
            self.connection.get_connection().search(
                search_base=user_dn,
                search_filter='(objectClass=user)',
                search_scope='BASE',
                attributes=['memberOf']
            )
            
            if self.connection.get_connection().entries:
                member_of = self.connection.get_connection().entries[0].memberOf.values
                return [str(group) for group in member_of]
            return []
        except Exception as e:
            print(f"Get user groups failed: {str(e)}")
            return []
