from typing import Optional
from ldap.search import LDAPSearch
from ldap.connection import LDAPConnection


class UsernameGenerator:
    """Generate unique usernames for Active Directory"""
    
    def __init__(self, ldap_connection: LDAPConnection):
        """Initialize username generator with LDAP connection"""
        self.ldap_search = LDAPSearch(ldap_connection)
    
    def generate_username(self, first_name: str, last_name: str) -> str:
        """Generate base username from first and last name"""
        # Convert to lowercase and join with dot
        base_username = f"{first_name.lower()}.{last_name.lower()}"
        return base_username
    
    def get_unique_username(self, first_name: str, last_name: str, max_attempts: int = 100) -> Optional[str]:
        """Generate a unique username that doesn't exist in AD"""
        base_username = self.generate_username(first_name, last_name)
        
        # Check if base username is available
        if not self.ldap_search.search_by_username(base_username):
            return base_username
        
        # Try incrementing suffix
        for i in range(1, max_attempts + 1):
            username = f"{base_username}{i}"
            if not self.ldap_search.search_by_username(username):
                return username
        
        return None
    
    def get_unique_username_with_counter(self, first_name: str, last_name: str, start_counter: int = 1) -> str:
        """Generate unique username starting from a specific counter"""
        base_username = self.generate_username(first_name, last_name)
        counter = start_counter
        
        while True:
            username = f"{base_username}{counter}"
            if not self.ldap_search.search_by_username(username):
                return username
            counter += 1
    
    def sanitize_username(self, username: str) -> str:
        """Sanitize username to meet AD requirements"""
        # Remove special characters except dots
        sanitized = ''.join(c for c in username if c.isalnum() or c == '.')
        
        # Ensure username doesn't start or end with dot
        sanitized = sanitized.strip('.')
        
        # Ensure username is not empty
        if not sanitized:
            sanitized = "user"
        
        # Limit username length (AD max is 20 characters for sAMAccountName)
        if len(sanitized) > 20:
            sanitized = sanitized[:20]
        
        return sanitized
    
    def validate_username(self, username: str) -> bool:
        """Validate username meets AD requirements"""
        if not username:
            return False
        
        # Check length
        if len(username) > 20 or len(username) < 1:
            return False
        
        # Check for valid characters
        import re
        pattern = r'^[a-zA-Z0-9\.]+$'
        return re.match(pattern, username) is not None
