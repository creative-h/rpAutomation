from ldap3 import SUBTREE
from typing import Optional, Dict, List
from ldap.connection import LDAPConnection


class LDAPSearch:
    """LDAP search operations for Active Directory"""
    
    def __init__(self, ldap_connection: LDAPConnection):
        """Initialize LDAP search with connection"""
        self.connection = ldap_connection
    
    def search_by_employee_id(self, employee_id: str) -> Optional[Dict]:
        """Search for user by employee ID"""
        if not self.connection.is_connected():
            return None
        
        base_dn = self.connection.get_base_dn()
        search_filter = f"(employeeID={employee_id})"
        
        try:
            self.connection.get_connection().search(
                search_base=base_dn,
                search_filter=search_filter,
                search_scope=SUBTREE,
                attributes=['*']
            )
            
            if self.connection.get_connection().entries:
                return self.connection.get_connection().entries[0].entry_attributes_as_dict
            return None
        except Exception as e:
            print(f"Search by employee ID failed: {str(e)}")
            return None
    
    def search_by_email(self, email: str) -> Optional[Dict]:
        """Search for user by email"""
        if not self.connection.is_connected():
            return None
        
        base_dn = self.connection.get_base_dn()
        search_filter = f"(mail={email})"
        
        try:
            self.connection.get_connection().search(
                search_base=base_dn,
                search_filter=search_filter,
                search_scope=SUBTREE,
                attributes=['*']
            )
            
            if self.connection.get_connection().entries:
                return self.connection.get_connection().entries[0].entry_attributes_as_dict
            return None
        except Exception as e:
            print(f"Search by email failed: {str(e)}")
            return None
    
    def search_by_username(self, username: str) -> Optional[Dict]:
        """Search for user by username (sAMAccountName)"""
        if not self.connection.is_connected():
            return None
        
        base_dn = self.connection.get_base_dn()
        search_filter = f"(sAMAccountName={username})"
        
        try:
            print(f"Searching for user: {username} with filter: {search_filter}")
            print(f"Base DN: {base_dn}")
            self.connection.get_connection().search(
                search_base=base_dn,
                search_filter=search_filter,
                search_scope=SUBTREE,
                attributes=['*']
            )
            
            print(f"Search returned {len(self.connection.get_connection().entries)} entries")
            if self.connection.get_connection().entries:
                return self.connection.get_connection().entries[0].entry_attributes_as_dict
            
            # If not found, try searching for all users to debug
            print("User not found, searching for all users to debug...")
            self.connection.get_connection().search(
                search_base=base_dn,
                search_filter="(objectClass=user)",
                search_scope=SUBTREE,
                attributes=['sAMAccountName', 'distinguishedName']
            )
            print(f"Total users in AD: {len(self.connection.get_connection().entries)}")
            for entry in self.connection.get_connection().entries[:5]:  # Show first 5
                print(f"  - {entry.sAMAccountName}: {entry.distinguishedName}")
            
            return None
        except Exception as e:
            print(f"Search by username failed: {str(e)}")
            import traceback
            traceback.print_exc()
            return None
    
    def check_duplicate_user(self, employee_id: str = None, email: str = None, username: str = None) -> Optional[Dict]:
        """Check if user exists by any identifier"""
        if employee_id:
            result = self.search_by_employee_id(employee_id)
            if result:
                return result
        
        if email:
            result = self.search_by_email(email)
            if result:
                return result
        
        if username:
            result = self.search_by_username(username)
            if result:
                return result
        
        return None
    
    def search_users_by_department(self, department: str) -> List[Dict]:
        """Search for all users in a specific department"""
        if not self.connection.is_connected():
            return []
        
        base_dn = self.connection.get_base_dn()
        search_filter = f"(department={department})"
        
        try:
            self.connection.get_connection().search(
                search_base=base_dn,
                search_filter=search_filter,
                search_scope=SUBTREE,
                attributes=['sAMAccountName', 'displayName', 'mail', 'department']
            )
            
            return [entry.entry_attributes_as_dict for entry in self.connection.get_connection().entries]
        except Exception as e:
            print(f"Search by department failed: {str(e)}")
            return []
    
    def search_by_dn(self, user_dn: str) -> Optional[Dict]:
        """Search for user by distinguished name"""
        if not self.connection.is_connected():
            return None
        
        try:
            print(f"Searching for user by DN: {user_dn}")
            self.connection.get_connection().search(
                search_base=user_dn,
                search_filter="(objectClass=user)",
                search_scope='BASE',
                attributes=['*']
            )
            
            print(f"DN search returned {len(self.connection.get_connection().entries)} entries")
            if self.connection.get_connection().entries:
                return self.connection.get_connection().entries[0].entry_attributes_as_dict
            return None
        except Exception as e:
            print(f"Search by DN failed: {str(e)}")
            return None
    
    def get_user_dn(self, username: str) -> Optional[str]:
        if not self.connection.is_connected():
            return None
        
        base_dn = self.connection.get_base_dn()
        search_filter = f"(sAMAccountName={username})"
        
        try:
            self.connection.get_connection().search(
                search_base=base_dn,
                search_filter=search_filter,
                search_scope=SUBTREE,
                attributes=['distinguishedName']
            )
            
            if self.connection.get_connection().entries:
                return str(self.connection.get_connection().entries[0].distinguishedName)
            return None
        except Exception as e:
            print(f"Get user DN failed: {str(e)}")
            return None
