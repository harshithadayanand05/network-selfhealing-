#!/usr/bin/env python
"""Test that Django loads correctly with new structure"""
import os
import sys
from pathlib import Path

# Add backend to path
PROJECT_ROOT = Path(__file__).resolve().parent
BACKEND_DIR = PROJECT_ROOT / 'backend'
sys.path.insert(0, str(BACKEND_DIR))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cn_project.settings')

print("=" * 70)
print("DJANGO CONFIGURATION TEST")
print("=" * 70)

try:
    import django
    print(f"\n✓ Django version: {django.get_version()}")
    
    # Setup Django
    django.setup()
    print("✓ Django setup successful")
    
    # Test imports
    from django.conf import settings
    print(f"✓ Settings loaded from: {settings.SETTINGS_MODULE}")
    
    # Verify important settings
    print(f"\n📁 Configuration Paths:")
    print(f"  BASE_DIR: {settings.BASE_DIR}")
    print(f"  PROJECT_ROOT: {settings.PROJECT_ROOT}")
    print(f"  Templates: {settings.TEMPLATES[0]['DIRS']}")
    print(f"  Static files: {settings.STATICFILES_DIRS}")
    print(f"  Database: {settings.DATABASES['default']['NAME']}")
    
    # Test installed apps
    print(f"\n📦 Installed Apps:")
    for app in ['admin_panel', 'students', 'network_sim']:
        if app in settings.INSTALLED_APPS:
            print(f"  ✓ {app}")
        else:
            print(f"  ✗ {app} - NOT FOUND!")
    
    # Test database connection
    from django.db import connection
    connection.ensure_connection()
    print(f"\n✓ Database connection successful")
    
    # Test models can be imported
    from students.models import Student, Exam
    from network_sim.models import ActiveConnection, ServerNode, NetworkEvent
    print(f"✓ All models imported successfully")
    
    print("\n" + "=" * 70)
    print("✅ ALL TESTS PASSED - Django is ready to run!")
    print("=" * 70)
    print("\n🚀 Run server with: cd backend && python manage.py runserver")
    
except Exception as e:
    print(f"\n❌ ERROR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
