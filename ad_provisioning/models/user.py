from dataclasses import dataclass, field
from typing import Optional, List
from datetime import datetime


@dataclass
class User:
    """Dataclass representing a user to be created in Active Directory"""
    
    # Basic Information (Required)
    employee_id: str
    first_name: str
    last_name: str
    email: str
    department: str
    
    # Basic Information (Optional)
    middle_name: Optional[str] = None
    display_name: Optional[str] = None
    
    # Organizational Information
    designation: Optional[str] = None
    manager: Optional[str] = None
    company: Optional[str] = None
    location: Optional[str] = None
    office: Optional[str] = None
    country: Optional[str] = None
    state: Optional[str] = None
    city: Optional[str] = None
    
    # Employment Details
    employee_type: Optional[str] = None
    business_unit: Optional[str] = None
    cost_center: Optional[str] = None
    start_date: Optional[str] = None
    
    # Contact Information
    phone_number: Optional[str] = None
    mobile_number: Optional[str] = None
    
    # AD Specific
    username: Optional[str] = None
    ou: Optional[str] = None
    security_groups: List[str] = field(default_factory=list)
    
    # Request Information
    request_id: Optional[str] = None
    requested_by: Optional[str] = None
    requested_date: Optional[str] = None
    
    # Status
    ad_status: str = "pending"
    ldap_status: str = "pending"
    portal_status: str = "pending"
    error_message: Optional[str] = None
    distinguished_name: Optional[str] = None
    
    # Timestamps
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def __post_init__(self):
        """Generate display name if not provided"""
        if not self.display_name:
            self.display_name = f"{self.first_name} {self.last_name}"
    
    def to_dict(self) -> dict:
        """Convert user to dictionary"""
        return {
            "employee_id": self.employee_id,
            "first_name": self.first_name,
            "middle_name": self.middle_name,
            "last_name": self.last_name,
            "display_name": self.display_name,
            "email": self.email,
            "department": self.department,
            "designation": self.designation,
            "manager": self.manager,
            "company": self.company,
            "location": self.location,
            "office": self.office,
            "country": self.country,
            "state": self.state,
            "city": self.city,
            "employee_type": self.employee_type,
            "business_unit": self.business_unit,
            "cost_center": self.cost_center,
            "start_date": self.start_date,
            "phone_number": self.phone_number,
            "mobile_number": self.mobile_number,
            "username": self.username,
            "ou": self.ou,
            "security_groups": self.security_groups,
            "request_id": self.request_id,
            "requested_by": self.requested_by,
            "requested_date": self.requested_date,
            "ad_status": self.ad_status,
            "ldap_status": self.ldap_status,
            "portal_status": self.portal_status,
            "error_message": self.error_message,
            "distinguished_name": self.distinguished_name,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
