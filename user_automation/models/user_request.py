# User request model
from dataclasses import dataclass, field
from typing import Dict

@dataclass
class UserRequest:
    """Dataclass to hold user request details from Website 1"""
    request_type: str
    first_name: str
    last_name: str
    request_category: str
    ad_id: str
    job_location: str
    metadata: Dict[str, str] = field(default_factory=dict)
