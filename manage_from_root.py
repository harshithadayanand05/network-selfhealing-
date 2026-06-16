#!/usr/bin/env python
"""
Helper script to run Django management commands from the reorganized project structure.
Usage: python manage_from_root.py runserver
       python manage_from_root.py migrate
       python manage_from_root.py shell
"""
import os
import sys
import django
from pathlib import Path

# Add backend to Python path
PROJECT_ROOT = Path(__file__).resolve().parent
BACKEND_DIR = PROJECT_ROOT / 'backend'
sys.path.insert(0, str(BACKEND_DIR))

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cn_project.settings')

# Setup Django
django.setup()

# Run management command
if __name__ == '__main__':
    from django.core.management import execute_from_command_line
    
    # If no command provided, show help
    if len(sys.argv) == 1:
        sys.argv.append('help')
    
    # Change to backend directory for command execution
    os.chdir(str(BACKEND_DIR))
    
    execute_from_command_line(sys.argv)
