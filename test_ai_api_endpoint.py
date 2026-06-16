#!/usr/bin/env python
"""Test the AI Analysis API endpoint"""
import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cn_project.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User

# Create a test client
client = Client()

print("=" * 60)
print("Testing AI Analysis API")
print("=" * 60)

# Create/login as admin
try:
    admin_user = User.objects.get(username='admin')
except User.DoesNotExist:
    admin_user = User.objects.create_superuser('admin', 'admin@test.com', 'adminpass')

client.login(username='admin', password='adminpass')
print("✓ Logged in as admin")

# Make a GET request to the API
try:
    response = client.get('/admin-panel/api/explainable-ai-analysis/')
    print(f"\nStatus Code: {response.status_code}")
    print(f"Content-Type: {response.get('Content-Type', 'Not Set')}")
    print("\nResponse Content:")
    content = response.content.decode('utf-8')
    print(content[:1500])
    
    # Try to parse as JSON
    try:
        data = response.json()
        if data.get('success'):
            print("\n✅ Valid JSON response:")
            print(json.dumps(data, indent=2)[:2000])
        else:
            print(f"\n❌ API Error: {data.get('message')}")
            if 'error_trace' in data:
                print(f"Error trace:\n{data['error_trace'][:500]}")
    except Exception as e:
        print(f"\n❌ Invalid JSON: {e}")
        print(f"Raw response: {content[:500]}")
        
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
