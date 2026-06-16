#!/usr/bin/env python
"""
Test script to diagnose AI analysis API issues
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cn_project.settings')
django.setup()

from django.test import RequestFactory
from django.contrib.auth.models import User
from admin_panel.network_api_views import api_explainable_ai_analysis
import json

print("=" * 80)
print("Testing AI Analysis API Endpoint")
print("=" * 80)

# Create a test request
factory = RequestFactory()
request = factory.get('/admin-panel/api/explainable-ai-analysis/')

# Get or create a test admin user
admin_user, created = User.objects.get_or_create(
    username='testadmin',
    defaults={'is_staff': True, 'is_superuser': True}
)

request.user = admin_user

print(f"\n✓ Using admin user: {admin_user.username} (is_staff={admin_user.is_staff})")

# Test the API
print("\nCalling api_explainable_ai_analysis()...")
try:
    response = api_explainable_ai_analysis(request)
    print(f"✓ Response Status: {response.status_code}")
    
    # Parse the response
    data = json.loads(response.content)
    
    if data.get('success'):
        print("\n✓ API Response: SUCCESS")
        print(f"  - Risk Level: {data['prediction']['risk_level']}")
        print(f"  - Confidence: {data['prediction']['confidence']}%")
        print(f"  - Contributing Factors: {data['factor_count']}")
        print(f"  - Timestamp: {data['timestamp']}")
    else:
        print("\n✗ API Response: FAILED")
        print(f"  - Error: {data.get('message', 'Unknown error')}")
        if 'error_trace' in data:
            print(f"\n  Full Error Trace:\n{data['error_trace']}")
    
    # Print full response for debugging
    print("\n" + "=" * 80)
    print("Full API Response:")
    print("=" * 80)
    print(json.dumps(data, indent=2, default=str))
    
except Exception as e:
    print(f"\n✗ Exception occurred: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 80)
