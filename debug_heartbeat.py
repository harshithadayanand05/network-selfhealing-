#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cn_project.settings')
django.setup()

from students.models import Student
from network_sim.client_node_monitor import ClientNodeMonitor
from django.utils import timezone

now = timezone.now()
print("Current Time:", now)

akshaya = Student.objects.get(user__username='akshaya')

# Get activities
activities = ClientNodeMonitor.get_client_activity_sources(akshaya, timeframe_seconds=600)

print(f"\nakshaya activities:")
print(f"  last_activity: {activities['last_activity']}")
print(f"  last_heartbeat: {activities.get('last_heartbeat')}")

if activities['last_activity']:
    time_diff = (now - activities['last_activity']).total_seconds()
    print(f"  time_since_activity: {time_diff}s")

if activities.get('last_heartbeat'):
    time_diff = (now - activities['last_heartbeat']).total_seconds()
    print(f"  time_since_heartbeat: {time_diff}s")

print(f"  request_logs: {len(activities['request_logs'])} logs")
for log in activities['request_logs'][:3]:
    print(f"    - {log.timestamp}: {log.method} {log.path}")
