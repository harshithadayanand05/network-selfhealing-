#!/usr/bin/env python
"""
Populate active connections for testing the clients tab
This creates test data showing connected clients
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cn_project.settings')
django.setup()

from students.models import Student
from network_sim.models import ActiveConnection
from django.utils import timezone
import random

print("=" * 60)
print("POPULATING ACTIVE CONNECTIONS FOR TESTING")
print("=" * 60)

# Get non-admin students
students = Student.objects.filter(user__is_staff=False, user__is_superuser=False).select_related('user')

if not students.exists():
    print("❌ No students found in database!")
    exit(1)

# IP addresses for testing
test_ips = [
    '192.168.1.101',
    '192.168.1.102',
    '192.168.1.103',
    '192.168.1.104',
    '192.168.1.105',
    '10.0.0.51',
    '10.0.0.52',
    '10.0.0.53',
    '172.16.0.10',
    '172.16.0.11',
]

# Clear old inactive connections (optional - comment out to keep history)
# ActiveConnection.objects.filter(is_active=False).delete()

# Create active connections for first 5 students
count = 0
for i, student in enumerate(students[:5]):
    # Delete any existing inactive connections for this student
    ActiveConnection.objects.filter(student=student, is_active=False).delete()
    
    # Create new active connection
    conn = ActiveConnection.objects.create(
        student=student,
        session_key=f'session_key_{i}',
        ip_address=test_ips[i % len(test_ips)],
        is_active=True,
        connected_at=timezone.now(),
        last_activity=timezone.now()
    )
    count += 1
    print(f"✅ Created: {student.user.username} | IP: {conn.ip_address}")

print("\n" + "=" * 60)
print(f"RESULT: Created {count} active connections")
print("=" * 60)

# Verify
active_conns = ActiveConnection.objects.filter(is_active=True).count()
print(f"\n✅ Total Active Connections in DB: {active_conns}")
print("\n🎯 You should now see connected clients in the Clients tab!")
