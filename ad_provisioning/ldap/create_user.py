from ldap3 import MODIFY_ADD, MODIFY_REPLACE
from typing import Optional
import json
import os
from ldap.connection import LDAPConnection
from models.user import User


class ADUserCreator:
    """Active Directory user creation operations"""
    
    def __init__(self, ldap_connection: LDAPConnection):
        """Initialize AD user creator with connection"""
        self.connection = ldap_connection
        self.config = self._load_config()
    
    def _load_config(self) -> dict:
        """Load AD configuration from JSON file"""
        config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config/config.json')
        with open(config_path, 'r') as f:
            config = json.load(f)
        return config['ad']
    
    def create_user(self, user: User, ou: str = None) -> Optional[str]:
        """Create user in Active Directory and return distinguished name"""
        if not self.connection.is_connected():
            return None
        
        # Use provided OU or default from config
        target_ou = ou or self.config['default_ou']
        user_dn = f"CN={user.display_name},{target_ou}"
        
        # Build user attributes (matching PHP logic)
        attributes = {
            'objectClass': ['top', 'person', 'organizationalPerson', 'user'],
            'cn': user.display_name,
            'sn': user.last_name,
            'givenName': user.first_name,
            'displayName': user.display_name,
            'sAMAccountName': user.username,
            'userPrincipalName': f"{user.username}@{self.connection.config['domain']}",
            'department': user.department
        }
        
        # Add optional attributes if provided
        if user.email:
            attributes['mail'] = user.email
        if user.employee_id:
            attributes['employeeID'] = user.employee_id
        if user.designation:
            attributes['title'] = user.designation
        if user.company:
            attributes['company'] = user.company
        if user.office:
            attributes['physicalDeliveryOfficeName'] = user.office
        if user.phone_number:
            attributes['telephoneNumber'] = user.phone_number
        if user.mobile_number:
            attributes['mobile'] = user.mobile_number
        if user.manager:
            attributes['manager'] = user.manager
        if user.employee_type:
            attributes['employeeType'] = user.employee_type
        if user.business_unit:
            attributes['businessCategory'] = user.business_unit
        if user.cost_center:
            attributes['extensionAttribute1'] = user.cost_center
        
        try:
            # Create user object
            print(f"Creating user with DN: {user_dn}")
            print(f"Attributes: {attributes}")
            
            # Check if DN already exists
            try:
                self.connection.get_connection().search(
                    search_base=user_dn,
                    search_filter='(objectClass=*)',
                    search_scope='BASE'
                )
                if self.connection.get_connection().entries:
                    print(f"ERROR: DN {user_dn} already exists!")
                    return None
            except:
                # DN doesn't exist, which is expected
                pass
            
            # Try to add the user with minimal attributes first
            minimal_attributes = {
                'objectClass': ['top', 'person', 'organizationalPerson', 'user'],
                'cn': user.display_name,
                'sAMAccountName': user.username
            }
            
            print(f"Attempting add with minimal attributes: {minimal_attributes}")
            result = self.connection.get_connection().add(user_dn, attributes=minimal_attributes)
            print(f"Add operation result: {result}")
            
            if not result:
                print(f"ERROR: Add operation returned False")
                # Check connection result for more details
                if self.connection.get_connection().result:
                    print(f"LDAP result: {self.connection.get_connection().result}")
                return None
            
            # Immediately verify the add
            self.connection.get_connection().search(
                search_base=user_dn,
                search_filter='(objectClass=user)',
                search_scope='BASE'
            )
            if not self.connection.get_connection().entries:
                print(f"ERROR: User not found immediately after add operation!")
                return None
            
            print("User object created successfully with minimal attributes")
            
            # Now add additional attributes
            print("Adding additional attributes...")
            additional_attrs = {}
            if user.last_name:
                additional_attrs['sn'] = user.last_name
            if user.first_name:
                additional_attrs['givenName'] = user.first_name
            if user.display_name:
                additional_attrs['displayName'] = user.display_name
            if user.email:
                additional_attrs['mail'] = user.email
            if user.employee_id:
                additional_attrs['employeeID'] = user.employee_id
            
            if additional_attrs:
                from ldap3 import MODIFY_REPLACE
                self.connection.get_connection().modify(user_dn, {k: [(MODIFY_REPLACE, v)] for k, v in additional_attrs.items()})
                print("Additional attributes added")
            
            # Set password
            print(f"Setting password...")
            self._set_password(user_dn, self.config['default_password'])
            print("Password set successfully")
            
            # Enable account
            print(f"Enabling account...")
            self._enable_account(user_dn)
            print("Account enabled successfully")
            
            # Force password change if configured
            if self.config.get('force_password_change', True):
                print(f"Forcing password change...")
                self._force_password_change(user_dn)
                print("Password change forced successfully")
            
            # Final verification
            self.connection.get_connection().search(
                search_base=user_dn,
                search_filter='(objectClass=user)',
                search_scope='BASE',
                attributes=['*']
            )
            if self.connection.get_connection().entries:
                print(f"Final verification successful: User {user_dn} exists in AD")
            else:
                print(f"WARNING: Final verification failed!")
            
            print(f"User creation completed successfully: {user_dn}")
            return user_dn
        except Exception as e:
            print(f"User creation failed: {str(e)}")
            import traceback
            traceback.print_exc()
            return None
    
    def _set_password(self, user_dn: str, password: str):
        """Set user password"""
        try:
            # Encode password as UTF-16LE with quotes for AD
            encoded_password = ('"%s"' % password).encode('utf-16-le')
            self.connection.get_connection().modify(
                user_dn,
                {'unicodePwd': [(MODIFY_ADD, encoded_password)]}
            )
        except Exception as e:
            print(f"Password set failed: {str(e)}")
    
    def _enable_account(self, user_dn: str):
        """Enable user account by setting userAccountControl"""
        try:
            # 512 = NORMAL_ACCOUNT (enabled), 514 = disabled
            # Use REPLACE to set the value, not ADD
            self.connection.get_connection().modify(
                user_dn,
                {'userAccountControl': [(MODIFY_REPLACE, 512)]}
            )
        except Exception as e:
            print(f"Account enable failed: {str(e)}")
    
    def _force_password_change(self, user_dn: str):
        """Force user to change password at next logon"""
        try:
            # pwdLastSet = 0 forces password change
            self.connection.get_connection().modify(
                user_dn,
                {'pwdLastSet': [(MODIFY_REPLACE, 0)]}
            )
        except Exception as e:
            print(f"Force password change failed: {str(e)}")
    
    def update_user_attributes(self, user_dn: str, attributes: dict) -> bool:
        """Update user attributes"""
        if not self.connection.is_connected():
            return False
        
        try:
            self.connection.get_connection().modify(user_dn, attributes)
            return True
        except Exception as e:
            print(f"User attribute update failed: {str(e)}")
            return False
    
    def delete_user(self, user_dn: str) -> bool:
        """Delete user from Active Directory"""
        if not self.connection.is_connected():
            return False
        
        try:
            self.connection.get_connection().delete(user_dn)
            return True
        except Exception as e:
            print(f"User deletion failed: {str(e)}")
            return False
