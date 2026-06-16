#!/usr/bin/env python
"""
Reorganize project structure to separate backend and frontend
Backend: Django apps, models, views, settings, management commands
Frontend: Templates, static files (CSS, JS)
"""
import os
import shutil
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent

# Define backend items
BACKEND_ITEMS = [
    'manage.py',
    'cn_project',
    'admin_panel',
    'students',
    'network_sim',
    'db.sqlite3',
    'requirements.txt',
    'seed_data.py',
    'run_seed.py',
    'analysis_report.py',
    'check_clients.py',
    'check_status.py',
    'debug_heartbeat.py',
    'detailed_diagnostic.py',
    'diagnose_activity.py',
    'network_dashboard.py',
    'populate_test_clients.py',
    'test_ai_analysis.py',
    'test_ai_api.py',
    'test_ai_api_endpoint.py',
    'test_ai_prediction.py',
    'test_api_endpoints.py',
    'test_looping_detection.py',
]

# Define frontend items
FRONTEND_ITEMS = [
    'templates',
    'static',
]

print("=" * 70)
print("PROJECT REORGANIZATION: Backend & Frontend Separation")
print("=" * 70)

# Move backend items
print("\n📦 Moving Backend Files...")
backend_path = PROJECT_ROOT / 'backend'
for item in BACKEND_ITEMS:
    src = PROJECT_ROOT / item
    dst = backend_path / item
    if src.exists():
        print(f"  Moving: {item}")
        if src.is_dir():
            if dst.exists():
                shutil.rmtree(dst)
            shutil.move(str(src), str(dst))
        else:
            shutil.move(str(src), str(dst))
    else:
        print(f"  ⚠️  Skipping (not found): {item}")

# Move frontend items
print("\n🎨 Moving Frontend Files...")
frontend_path = PROJECT_ROOT / 'frontend'
for item in FRONTEND_ITEMS:
    src = PROJECT_ROOT / item
    dst = frontend_path / item
    if src.exists():
        print(f"  Moving: {item}")
        if src.is_dir():
            if dst.exists():
                shutil.rmtree(dst)
            shutil.move(str(src), str(dst))
        else:
            shutil.move(str(src), str(dst))
    else:
        print(f"  ⚠️  Skipping (not found): {item}")

print("\n✅ File reorganization complete!")
print("\n📁 New Structure:")
print("  cn_exam_network/")
print("    backend/          (Django apps, models, views, management, etc.)")
print("    frontend/         (Templates, static files)")
print("    .venv/            (Virtual environment)")
print("    TECHNOLOGIES/     (Documentation)")
print("    *.md              (Documentation)")
print("    README.md         (Project readme)")
print("\n⚠️  NEXT: Update Django settings and paths")
print("=" * 70)
