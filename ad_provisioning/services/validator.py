from typing import List, Tuple
from models.user import User
import json
import os


class FieldValidator:
    """Validator for user data fields"""
    
    def __init__(self, config_path: str = "config/config.json"):
        """Initialize validator with configuration"""
        self.config = self._load_config(config_path)
        self.mandatory_fields = self.config.get('validation', {}).get('mandatory_fields', [])
    
    def _load_config(self, config_path: str) -> dict:
        """Load validation configuration from JSON file"""
        # If config_path is absolute or already contains parent directory, use as-is
        if os.path.isabs(config_path) or 'config/' in config_path:
            full_path = config_path
        else:
            full_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), config_path)
        
        with open(full_path, 'r') as f:
            config = json.load(f)
        return config
    
    def validate_user(self, user: User) -> Tuple[bool, List[str]]:
        """Validate user data and return (is_valid, missing_fields)"""
        missing_fields = []
        
        for field in self.mandatory_fields:
            if not hasattr(user, field) or getattr(user, field) is None or getattr(user, field) == "":
                missing_fields.append(field)
        
        return len(missing_fields) == 0, missing_fields
    
    def validate_email(self, email: str) -> bool:
        """Validate email format"""
        if not email:
            return False
        
        # Basic email validation
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def validate_employee_id(self, employee_id: str) -> bool:
        """Validate employee ID format"""
        if not employee_id:
            return False
        
        # Employee ID should not be empty and should be alphanumeric
        return len(employee_id) > 0 and employee_id.replace('.', '').replace('_', '').isalnum()
    
    def validate_phone_number(self, phone_number: str) -> bool:
        """Validate phone number format"""
        if not phone_number:
            return True  # Phone number is optional
        
        # Basic phone validation - digits, spaces, dashes, parentheses
        import re
        pattern = r'^[\d\s\-\(\)\+]+$'
        return re.match(pattern, phone_number) is not None
    
    def validate_username(self, username: str) -> bool:
        """Validate username format"""
        if not username:
            return False
        
        # Username should be alphanumeric with dots
        import re
        pattern = r'^[a-zA-Z0-9\.]+$'
        return re.match(pattern, username) is not None
    
    def get_validation_summary(self, user: User) -> dict:
        """Get comprehensive validation summary for a user"""
        is_valid, missing_fields = self.validate_user(user)
        
        summary = {
            'is_valid': is_valid,
            'missing_fields': missing_fields,
            'email_valid': self.validate_email(user.email),
            'employee_id_valid': self.validate_employee_id(user.employee_id),
            'phone_valid': self.validate_phone_number(user.phone_number) if user.phone_number else True,
            'mobile_valid': self.validate_phone_number(user.mobile_number) if user.mobile_number else True
        }
        
        return summary
