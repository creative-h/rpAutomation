from ldap3 import Server, Connection, ALL, NTLM
from typing import Optional
import json
import os


class LDAPConnection:
    """Centralized LDAP client for Active Directory operations"""
    
    def __init__(self, config_path: str = "config/config.json"):
        """Initialize LDAP connection with configuration"""
        self.config = self._load_config(config_path)
        self.server: Optional[Server] = None
        self.connection: Optional[Connection] = None
        self._initialize_server()
    
    def _load_config(self, config_path: str) -> dict:
        """Load LDAP configuration from JSON file"""
        full_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), config_path)
        with open(full_path, 'r') as f:
            config = json.load(f)
        return config['ldap']
    
    def _initialize_server(self):
        """Initialize LDAP server connection"""
        server_url = self.config['server']
        port = self.config['port']
        use_ssl = self.config.get('use_ssl', False)
        
        self.server = Server(
            server_url,
            port=port,
            use_ssl=use_ssl,
            get_info=ALL
        )
    
    def connect(self) -> bool:
        """Establish connection to Active Directory"""
        try:
            bind_user = self.config['bind_user']
            bind_password = self.config['bind_password']
            
            self.connection = Connection(
                self.server,
                user=bind_user,
                password=bind_password,
                authentication=NTLM,
                auto_bind=True
            )
            return True
        except Exception as e:
            print(f"LDAP connection failed: {str(e)}")
            return False
    
    def disconnect(self):
        """Close LDAP connection"""
        if self.connection:
            self.connection.unbind()
            self.connection = None
    
    def is_connected(self) -> bool:
        """Check if connection is active"""
        return self.connection is not None and self.connection.bound
    
    def get_base_dn(self) -> str:
        """Get base distinguished name from configuration"""
        return self.config['base_dn']
    
    def get_connection(self) -> Optional[Connection]:
        """Get the active LDAP connection"""
        return self.connection
    
    def __enter__(self):
        """Context manager entry"""
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.disconnect()
