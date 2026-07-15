# Dropdown value mappings for ELMS system
# These mappings convert human-readable values to system dropdown IDs

LOCATION_MAP = {
    "Ujjain": "100001",
    "dewas": "100002",
    "INDORE": "100001",  # Fallback to Ujjain
}

DEPARTMENT_MAP = {
    "IT": "10030",
    "Information Technology": "10030",
}

DESIGNATION_MAP = {
    "Manager": "1",
    "Executive": "2",
    "testDesignation": "5",
    "Executive - IT": "2",  # Fallback mapping
}

ROLE_MAP = {
    " Admin": "1",
    "Department Training Coordinator": "4",
    "Global Admin": "6",
    "Global Training Coordinator": "2",
    "Location Training Coordinator": "3",
    "Training Manager": "7",
    "Training Manager_8": "10",
    "User": "5",
    "Employee": "5",  # Fallback mapping
}

JOB_ROLE_MAP = {
    "SPL. MGT.": "1",
    "ASSISTANT": "8",
    "Software Engineer": "1",  # Fallback mapping
}
