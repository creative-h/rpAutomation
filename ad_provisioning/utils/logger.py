import logging
import os
from datetime import datetime
from typing import Optional


class Logger:
    """Centralized logging utility for AD provisioning automation"""
    
    def __init__(self, log_file: str = "logs/ad_provisioning.log", log_level: str = "INFO"):
        """Initialize logger with file and console handlers"""
        self.logger = logging.getLogger("ADProvisioning")
        self.logger.setLevel(getattr(logging, log_level.upper()))
        
        # Create logs directory if it doesn't exist
        log_dir = os.path.dirname(log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        # File handler
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(getattr(logging, log_level.upper()))
        file_formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(file_formatter)
        self.logger.addHandler(file_handler)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(getattr(logging, log_level.upper()))
        console_formatter = logging.Formatter('%(asctime)s | %(levelname)-8s | %(message)s')
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)
    
    def info(self, message: str):
        """Log info message"""
        self.logger.info(message)
    
    def warning(self, message: str):
        """Log warning message"""
        self.logger.warning(message)
    
    def error(self, message: str):
        """Log error message"""
        self.logger.error(message)
    
    def debug(self, message: str):
        """Log debug message"""
        self.logger.debug(message)
    
    def log_user_creation(self, user, status: str, error: Optional[str] = None):
        """Log user creation attempt with details"""
        log_message = (
            f"User Creation | "
            f"Request ID: {user.request_id} | "
            f"Employee ID: {user.employee_id} | "
            f"Username: {user.username} | "
            f"Email: {user.email} | "
            f"Department: {user.department} | "
            f"Status: {status}"
        )
        
        if error:
            log_message += f" | Error: {error}"
        
        if status == "success":
            self.info(log_message)
        elif status == "failed":
            self.error(log_message)
        else:
            self.warning(log_message)
    
    def log_ldap_operation(self, operation: str, status: str, details: str = ""):
        """Log LDAP operation"""
        log_message = f"LDAP Operation | {operation} | Status: {status}"
        if details:
            log_message += f" | Details: {details}"
        
        if status == "success":
            self.info(log_message)
        elif status == "failed":
            self.error(log_message)
        else:
            self.warning(log_message)
    
    def log_portal_operation(self, operation: str, status: str, details: str = ""):
        """Log portal operation"""
        log_message = f"Portal Operation | {operation} | Status: {status}"
        if details:
            log_message += f" | Details: {details}"
        
        if status == "success":
            self.info(log_message)
        elif status == "failed":
            self.error(log_message)
        else:
            self.warning(log_message)
    
    def log_validation_error(self, user, missing_fields: list):
        """Log validation error for missing mandatory fields"""
        log_message = (
            f"Validation Error | "
            f"Request ID: {user.request_id} | "
            f"Employee ID: {user.employee_id} | "
            f"Missing Fields: {', '.join(missing_fields)}"
        )
        self.error(log_message)
    
    def log_duplicate_user(self, user, existing_field: str):
        """Log duplicate user detection"""
        log_message = (
            f"Duplicate User | "
            f"Request ID: {user.request_id} | "
            f"Employee ID: {user.employee_id} | "
            f"Duplicate Field: {existing_field}"
        )
        self.warning(log_message)
