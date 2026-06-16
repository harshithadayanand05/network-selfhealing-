#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cn_project.settings')
django.setup()

from students.models import Student
from network_sim.models import ActiveConnection, RequestLog
from network_sim.client_node_monitor import ClientNodeMonitor
from django.utils import timezone
from datetime import timedelta

now = timezone.now()
print("Current Time:", now)
print("\n" + "="*70)
print("STUDENT CONNECTION & ACTIVITY STATUS")
print("="*70 + "\n")

students = Student.objects.filter(user__is_staff=False).order_by('user__username')

for student in students:
    print(f"\n{student.user.username}:")
    print(f"  is_online: {student.is_online}")
    print(f"  login_time: {student.login_time}")
    
    # Check active connections
    active_conns = ActiveConnection.objects.filter(student=student, is_active=True)
    print(f"  Active Connections: {active_conns.count()}")
    for conn in active_conns:
        print(f"    - connected_at: {conn.connected_at}, last_activity: {conn.last_activity}")
        if conn.last_activity:
            time_diff = (now - conn.last_activity).total_seconds()
            print(f"      (activity {time_diff:.0f}s ago)")
    
    # Check recent requests
    recent_requests = RequestLog.objects.filter(
        user=student.user,
        timestamp__gte=now - timedelta(minutes=5)
    ).order_by('-timestamp')[:3]
    
    print(f"  Recent Requests (last 5 min): {RequestLog.objects.filter(user=student.user, timestamp__gte=now - timedelta(minutes=5)).count()}")
    if recent_requests:
        for req in recent_requests:
            print(f"    - {req.timestamp}: {req.method} {req.path}")
    
    # Get activity sources
    activities = ClientNodeMonitor.get_client_activity_sources(student, timeframe_seconds=600)
    print(f"  Last Activity (from all sources): {activities['last_activity']}")
    if activities['last_activity']:
        time_diff = (now - activities['last_activity']).total_seconds()
        print(f"    (activity {time_diff:.0f}s ago)")
