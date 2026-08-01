"""
UI Module Package
"""

from .dashboard import show_dashboard
from .automation import show_automation
from .reports import show_reports
from .logs import show_logs
from .screenshots import show_screenshots
from .settings import show_settings
from .about import show_about

__all__ = [
    'show_dashboard',
    'show_automation',
    'show_reports',
    'show_logs',
    'show_screenshots',
    'show_settings',
    'show_about'
]
