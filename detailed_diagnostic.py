#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cn_project.settings')
django.setup()

from network_sim.models import ClientNodeStatus, ActiveConnection, RequestLog
from students.models import Student
from django.utils import timezone
from datetime import timedelta

print("=" * 80)
print("DETAILED NODE DIAGNOSTIC REPORT")
print("=" * 80)

current_time = timezone.now()
print(f"\nCurrent Time: {current_time}")

# Get all students
students = Student.objects.filter(user__is_staff=False, user__is_superuser=False)

for student in students:
    print(f"\n{'-' * 80}")
    print(f"STUDENT: {student.user.username}")
    print(f"{'-' * 80}")
    
    # Check NodeStatus
    node_status = ClientNodeStatus.objects.filter(student=student).first()
    if node_status:
        print(f"\n📊 CLIENT NODE STATUS:")
        print(f"  Status: {node_status.status}")
        print(f"  Last Heartbeat: {node_status.last_heartbeat}")
        print(f"  Last Activity: {node_status.last_activity}")
        print(f"  Connected At: {node_status.connected_at}")
        print(f"  IP Address: {node_status.ip_address}")
        print(f"  Heartbeat Timeout: {node_status.heartbeat_timeout_seconds}s")
        print(f"  Activity Timeout: {node_status.activity_timeout_seconds}s")
        
        # Calculate time since
        if node_status.last_heartbeat:
            time_since_heartbeat = (current_time - node_status.last_heartbeat).total_seconds()
            print(f"  ⏱️ Time Since Heartbeat: {time_since_heartbeat:.0f}s")
        else:
            print(f"  ⏱️ Time Since Heartbeat: NEVER")
            
        if node_status.last_activity:
            time_since_activity = (current_time - node_status.last_activity).total_seconds()
            print(f"  ⏱️ Time Since Activity: {time_since_activity:.0f}s")
        else:
            print(f"  ⏱️ Time Since Activity: NEVER")
    else:
        print(f"\n❌ No ClientNodeStatus found")
    
    # Check ActiveConnections
    active_conns = ActiveConnection.objects.filter(student=student).order_by('-connected_at')
    print(f"\n🔗 ACTIVE CONNECTIONS: ({active_conns.count()} total)")
    for i, conn in enumerate(active_conns[:5], 1):  # Show last 5
        status_icon = "✅" if conn.is_active else "❌"
        print(f"  {i}. {status_icon} Active={conn.is_active}, Last={conn.last_activity}, Connected={conn.connected_at}")
    
    # Check RequestLogs
    req_logs = RequestLog.objects.filter(user=student.user).order_by('-timestamp')
    print(f"\n📝 REQUEST LOGS: ({req_logs.count()} total)")
    for i, req in enumerate(req_logs[:5], 1):  # Show last 5
        if req.user:
            print(f"  {i}. {req.path} @ {req.timestamp}")
        
print(f"\n{'=' * 80}")
print("SUMMARY")
print(f"{'=' * 80}")

summary = {
    'ACTIVE': 0,
    'INACTIVE': 0,
    'NODE_FAILURE': 0
}

for student in students:
    node_status = ClientNodeStatus.objects.filter(student=student).first()
    if node_status:
        summary[node_status.status] = summary.get(node_status.status, 0) + 1

print(f"\nTotal Students: {students.count()}")
print(f"ACTIVE Nodes: {summary['ACTIVE']}")
print(f"INACTIVE Nodes: {summary['INACTIVE']}")
print(f"NODE_FAILURE: {summary['NODE_FAILURE']}")
