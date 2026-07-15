# Approval request model
from dataclasses import dataclass, field
from typing import Dict

@dataclass
class ApprovalRequest:
    request_id: str
    category: str
    requested_user: str
    email: str
    department: str
    requested_by: str
    system: str
    status: str
    metadata: Dict[str, str] = field(default_factory=dict)
