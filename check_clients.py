#!/usr/bin/env python
"""Check connected clients and debug missing connections"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cn_project.settings')
django.setup()

from students.models import Student, Exam, ExamAttempt
from network_sim.models import ServerNode, ActiveConnection, NetworkEvent
from django.utils import timezone

print("=" * 60)
print("DIAGNOSTIC: CLIENT CONNECTION CHECK")
print("=" * 60)

# 1. Check total students
total_students = Student.objects.count()
print(f"\n1. Total Students in DB: {total_students}")
students = Student.objects.select_related('user').values_list('user__username', 'is_online', 'ip_address', 'login_time')
for username, is_online, ip, login_time in students[:10]:
    print(f"   - {username} | Online: {is_online} | IP: {ip} | Login: {login_time}")

# 2. Check ActiveConnection records
print(f"\n2. Active Connections in DB:")
active_conns = ActiveConnection.objects.all().select_related('student__user', 'server_node')
print(f"   Total: {active_conns.count()}")
for conn in active_conns:
    print(f"   - {conn.student.user.username} | IP: {conn.ip_address} | Active: {conn.is_active} | Connected: {conn.connected_at}")

# 3. Check what the clients view would see
print(f"\n3. What admin_clients view sees:")
students_query = Student.objects.filter(user__is_staff=False, user__is_superuser=False).select_related('user')
print(f"   Eligible Students: {students_query.count()}")

active_connections_query = ActiveConnection.objects.filter(is_active=True).exclude(student__user__is_staff=True).exclude(student__user__is_superuser=True).select_related('student', 'server_node')
print(f"   Active Connections (is_active=True): {active_connections_query.count()}")

for conn in active_connections_query:
    print(f"   - {conn.student.user.username} | IP: {conn.ip_address} | Server: {conn.server_node}")

# 4. Check ServerNodes
print(f"\n4. Server Nodes:")
nodes = ServerNode.objects.all()
print(f"   Total: {nodes.count()}")
for node in nodes:
    print(f"   - {node.name} | IP: {node.ip_address} | Healthy: {node.is_healthy} | Load: {node.current_load}/{node.max_capacity}")

# 5. Check Recent NetworkEvents
print(f"\n5. Recent Network Events:")
events = NetworkEvent.objects.all().order_by('-timestamp')[:5]
for event in events:
    print(f"   - {event.event_type}: {event.description[:50]}... | Severity: {event.severity}")

# 6. Check ExamAttempts
print(f"\n6. Recent Exam Attempts:")
attempts = ExamAttempt.objects.all().order_by('-started_at')[:5]
for attempt in attempts:
    print(f"   - {attempt.student.user.username} | Exam: {attempt.exam.name} | Started: {attempt.started_at}")

print("\n" + "=" * 60)
print("RECOMMENDATION:")
print("=" * 60)
if active_connections_query.count() == 0:
    print("❌ No active connections found!")
    print("\nTo populate connections, you need to:")
    print("1. Ensure students are logged in and taking exams")
    print("2. Check if middleware is creating ActiveConnection records")
    print("3. Verify student middleware is working in network_sim/middleware.py")
    print("\nTry running: python manage.py seed_data (if available)")
else:
    print(f"✅ Found {active_connections_query.count()} active connections!")
    print("The clients tab should be populated correctly.")
