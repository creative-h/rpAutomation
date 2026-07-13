# User model
from dataclasses import dataclass, field
from typing import Dict

@dataclass
class User:
    ad_id: str
    first_name: str
    last_name: str
    email: str
    employee_id: str
    department: str
    role: str
    metadata: Dict[str, str] = field(default_factory=dict)