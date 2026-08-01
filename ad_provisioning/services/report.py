import csv
import json
import os
from datetime import datetime
from typing import List
from models.user import User


class ReportGenerator:
    """Generate execution reports for AD provisioning automation"""
    
    def __init__(self, output_dir: str = "reports", format: str = "csv"):
        """Initialize report generator with output directory and format"""
        self.output_dir = output_dir
        self.format = format.lower()
        self._ensure_directory_exists()
    
    def _ensure_directory_exists(self):
        """Create output directory if it doesn't exist"""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
    
    def generate_csv_report(self, users: List[User], filename: str = None) -> str:
        """Generate CSV report from user data"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"ad_provisioning_report_{timestamp}.csv"
        
        filepath = os.path.join(self.output_dir, filename)
        
        if not users:
            # Create empty report with headers
            headers = [
                'request_id', 'employee_id', 'username', 'first_name', 'last_name',
                'email', 'department', 'location', 'ad_status', 'ldap_status',
                'portal_status', 'error_message', 'distinguished_name', 'created_at'
            ]
            with open(filepath, 'w', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=headers)
                writer.writeheader()
            return filepath
        
        # Write user data
        with open(filepath, 'w', newline='') as csvfile:
            fieldnames = [
                'request_id', 'employee_id', 'username', 'first_name', 'last_name',
                'email', 'department', 'location', 'ad_status', 'ldap_status',
                'portal_status', 'error_message', 'distinguished_name', 'created_at'
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for user in users:
                writer.writerow({
                    'request_id': user.request_id,
                    'employee_id': user.employee_id,
                    'username': user.username,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'email': user.email,
                    'department': user.department,
                    'location': user.location,
                    'ad_status': user.ad_status,
                    'ldap_status': user.ldap_status,
                    'portal_status': user.portal_status,
                    'error_message': user.error_message,
                    'distinguished_name': user.distinguished_name,
                    'created_at': user.created_at
                })
        
        return filepath
    
    def generate_json_report(self, users: List[User], filename: str = None) -> str:
        """Generate JSON report from user data"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"ad_provisioning_report_{timestamp}.json"
        
        filepath = os.path.join(self.output_dir, filename)
        
        report_data = {
            'generated_at': datetime.now().isoformat(),
            'total_users': len(users),
            'successful': len([u for u in users if u.ad_status == 'success']),
            'failed': len([u for u in users if u.ad_status == 'failed']),
            'skipped': len([u for u in users if u.ad_status == 'skipped']),
            'users': [user.to_dict() for user in users]
        }
        
        with open(filepath, 'w') as jsonfile:
            json.dump(report_data, jsonfile, indent=2)
        
        return filepath
    
    def generate_summary_report(self, users: List[User]) -> dict:
        """Generate summary statistics from user data"""
        total = len(users)
        successful = len([u for u in users if u.ad_status == 'success'])
        failed = len([u for u in users if u.ad_status == 'failed'])
        skipped = len([u for u in users if u.ad_status == 'skipped'])
        pending = len([u for u in users if u.ad_status == 'pending'])
        
        summary = {
            'total_requests': total,
            'successful_creations': successful,
            'failed_creations': failed,
            'skipped_duplicates': skipped,
            'pending_processing': pending,
            'success_rate': (successful / total * 100) if total > 0 else 0,
            'failure_rate': (failed / total * 100) if total > 0 else 0
        }
        
        return summary
    
    def generate_report(self, users: List[User], filename: str = None) -> str:
        """Generate report in configured format"""
        if self.format == 'csv':
            return self.generate_csv_report(users, filename)
        elif self.format == 'json':
            return self.generate_json_report(users, filename)
        else:
            raise ValueError(f"Unsupported format: {self.format}")
    
    def append_user_to_report(self, user: User, filename: str = "current_run.csv"):
        """Append a single user to an existing report"""
        filepath = os.path.join(self.output_dir, filename)
        
        # Check if file exists
        file_exists = os.path.isfile(filepath)
        
        with open(filepath, 'a', newline='') as csvfile:
            fieldnames = [
                'request_id', 'employee_id', 'username', 'first_name', 'last_name',
                'email', 'department', 'location', 'ad_status', 'ldap_status',
                'portal_status', 'error_message', 'distinguished_name', 'created_at'
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            if not file_exists:
                writer.writeheader()
            
            writer.writerow({
                'request_id': user.request_id,
                'employee_id': user.employee_id,
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'department': user.department,
                'location': user.location,
                'ad_status': user.ad_status,
                'ldap_status': user.ldap_status,
                'portal_status': user.portal_status,
                'error_message': user.error_message,
                'distinguished_name': user.distinguished_name,
                'created_at': user.created_at
            })
        
        return filepath
