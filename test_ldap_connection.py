#!/usr/bin/env python3
"""Test LDAP connection with different credentials"""

from ldap3 import Server, Connection, ALL
import sys

def test_ldap_connection(server, domain, bind_user, bind_password, base_dn):
    """Test LDAP connection with given credentials"""
    try:
        print(f"Testing LDAP connection...")
        print(f"Server: {server}")
        print(f"Domain: {domain}")
        print(f"Bind User: {bind_user}")
        print(f"Base DN: {base_dn}")
        print("-" * 50)
        
        # Try different bind user formats
        username_only = bind_user.split('\\')[-1]
        bind_formats = [
            bind_user,  # As provided
            f"{domain}\\{username_only}",  # domain\username
            username_only,  # Just username
            f"{username_only}@{domain}",  # username@domain
        ]
        
        for i, user_format in enumerate(bind_formats, 1):
            try:
                print(f"\nAttempt {i}: Binding as '{user_format}'")
                server_obj = Server(server, get_info=ALL)
                conn = Connection(server_obj, user=user_format, password=bind_password, auto_bind=True)
                
                if conn.bind():
                    print(f"[SUCCESS] Connected as '{user_format}'")
                    print(f"[SUCCESS] Bound successfully")
                    
                    # Test search
                    conn.search(base_dn, '(objectclass=user)', attributes=['cn', 'sAMAccountName'])
                    print(f"[SUCCESS] Search successful: Found {len(conn.entries)} users")
                    
                    conn.unbind()
                    return True, user_format
            except Exception as e:
                print(f"[FAILED] {str(e)}")
                continue
        
        print("\n[FAILED] All bind attempts failed")
        return False, None
        
    except Exception as e:
        print(f"[FAILED] Connection error: {str(e)}")
        return False, None

if __name__ == "__main__":
    # Test server credentials
    print("=" * 50)
    print("Testing Test Server (192.168.56.101)")
    print("=" * 50)
    success, user_format = test_ldap_connection(
        server="192.168.56.101",
        domain="automation.local",
        bind_user="AUTOMATION\\Administrator",
        bind_password="Admin@12345",
        base_dn="DC=automation,DC=local"
    )
    
    if success:
        print(f"\n[SUCCESS] Working credentials: {user_format}")
        print("Update config_test.json with this bind_user format")
    else:
        print("\n[FAILED] Please verify credentials on the test server")
        print("Try running this on the test server:")
        print("  - Open Active Directory Users and Computers")
        print("  - Find the automation user account")
        print("  - Check the username and reset password if needed")
