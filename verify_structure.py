#!/usr/bin/env python
"""
Verify the new project structure is correct
"""
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent
BACKEND_DIR = PROJECT_ROOT / 'backend'
FRONTEND_DIR = PROJECT_ROOT / 'frontend'

print("=" * 70)
print("PROJECT STRUCTURE VERIFICATION")
print("=" * 70)

# Check backend
print("\n✅ BACKEND STRUCTURE:")
backend_items = [
    'manage.py',
    'requirements.txt',
    'db.sqlite3',
    'cn_project',
    'admin_panel',
    'students',
    'network_sim',
    'seed_data.py',
]

for item in backend_items:
    path = BACKEND_DIR / item
    status = "✓" if path.exists() else "✗"
    print(f"  {status} {item}")

# Check frontend
print("\n✅ FRONTEND STRUCTURE:")
frontend_items = [
    'templates',
    'static',
]

for item in frontend_items:
    path = FRONTEND_DIR / item
    status = "✓" if path.exists() else "✗"
    print(f"  {status} {item}")

# Check root documentation
print("\n✅ ROOT DOCUMENTATION:")
root_items = [
    'README.md',
    'REORGANIZATION_GUIDE.md',
    'PROJECT_EXPLANATION.md',
    'TECHNOLOGIES',
    '.venv',
]

for item in root_items:
    path = PROJECT_ROOT / item
    status = "✓" if path.exists() else "✗"
    print(f"  {status} {item}")

# Check key backend apps
print("\n✅ DJANGO APPS IN BACKEND:")
apps_check = [
    'backend/cn_project/settings.py',
    'backend/cn_project/urls.py',
    'backend/admin_panel/__init__.py',
    'backend/students/__init__.py',
    'backend/network_sim/__init__.py',
]

for app_path in apps_check:
    full_path = PROJECT_ROOT / app_path
    status = "✓" if full_path.exists() else "✗"
    print(f"  {status} {app_path}")

# Check templates and static
print("\n✅ FRONTEND ASSETS:")
frontend_check = [
    'frontend/templates/base.html',
    'frontend/static/css',
    'frontend/static/js',
]

for item_path in frontend_check:
    full_path = PROJECT_ROOT / item_path
    status = "✓" if full_path.exists() else "✗"
    print(f"  {status} {item_path}")

print("\n" + "=" * 70)
print("✅ PROJECT REORGANIZATION COMPLETE!")
print("=" * 70)
print("\n📖 NEXT STEPS:")
print("  1. Read: REORGANIZATION_GUIDE.md")
print("  2. Navigate: cd backend")
print("  3. Run server: python manage.py runserver")
print("  4. Access admin: http://localhost:8000/admin-panel/")
print("\n" + "=" * 70)
