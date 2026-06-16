#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cn_project.settings')
django.setup()

from network_sim.models import ClientNodeStatus, ActiveConnection, RequestLog
from students.models import Student
from django.utils import timezone
from datetime import timedelta

print("\n" + "=" * 90)
print(" " * 20 + "NODE STATUS ANALYSIS & RECOMMENDATIONS")
print("=" * 90)

current_time = timezone.now()

students = Student.objects.filter(user__is_staff=False, user__is_superuser=False)

print(f"\n📋 CURRENT STATUS (Time: {current_time}):\n")

for student in students:
    node_status = ClientNodeStatus.objects.filter(student=student).first()
    active_conns = ActiveConnection.objects.filter(student=student, is_active=True)
    
    if not node_status:
        continue
    
    # Get detailed status
    has_active_connection = active_conns.exists()
    has_recent_heartbeat = node_status.last_heartbeat and \
                          (current_time - node_status.last_heartbeat).total_seconds() <= 60
    has_recent_activity = node_status.last_activity and \
                         (current_time - node_status.last_activity).total_seconds() <= 60
    
    # Analysis
    analysis = []
    
    if has_active_connection:
        conn = active_conns.first()
        time_since_conn_activity = (current_time - conn.last_activity).total_seconds()
        analysis.append(f"✅ ACTIVE CONNECTION: is_active=True (Connection last activity: {time_since_conn_activity:.0f}s ago)")
    else:
        analysis.append(f"❌ NO ACTIVE CONNECTION: is_active=False")
    
    if has_recent_heartbeat:
        time_since_hb = (current_time - node_status.last_heartbeat).total_seconds()
        analysis.append(f"❤️  RECENT HEARTBEAT: {time_since_hb:.0f}s ago")
    elif node_status.last_heartbeat:
        time_since_hb = (current_time - node_status.last_heartbeat).total_seconds()
        analysis.append(f"❤️  STALE HEARTBEAT: {time_since_hb:.0f}s ago (timeout={node_status.heartbeat_timeout_seconds}s)")
    else:
        analysis.append(f"❤️  NO HEARTBEAT: Never received")
    
    if has_recent_activity:
        time_since_act = (current_time - node_status.last_activity).total_seconds()
        analysis.append(f"🖱️  RECENT ACTIVITY: {time_since_act:.0f}s ago")
    elif node_status.last_activity:
        time_since_act = (current_time - node_status.last_activity).total_seconds()
        analysis.append(f"🖱️  STALE ACTIVITY: {time_since_act:.0f}s ago (timeout={node_status.activity_timeout_seconds}s)")
    else:
        analysis.append(f"🖱️  NO ACTIVITY: Never")
    
    # Recommendation
    if has_active_connection and (has_recent_heartbeat or has_recent_activity or node_status.last_heartbeat):
        recommended_status = "INACTIVE (Screen off - connection established, no user activity)"
    elif not has_active_connection and not node_status.last_heartbeat:
        recommended_status = "NODE_FAILURE (Completely disconnected)"
    elif not has_active_connection:
        recommended_status = "NODE_FAILURE (Connection lost)"
    else:
        recommended_status = "ACTIVE (User is active)" if has_recent_activity else "INACTIVE (Connected but idle)"
    
    print(f"\n👤 {student.user.username.upper()}")
    print(f"   Current Status: {node_status.status}")
    for line in analysis:
        print(f"   {line}")
    print(f"   ✅ Recommended Status: {recommended_status}")

print("\n" + "=" * 90)
print(" " * 30 + "KEY ISSUE IDENTIFIED")
print("=" * 90)
print("""
🔴 PROBLEM:
   - All nodes show as NODE_FAILURE, but some have ACTIVE CONNECTIONS (is_active=True)
   - This is contradictory: if connection is active, the node shouldn't be marked as failed
   
💡 ROOT CAUSE:
   - The logic checks heartbeat_timeout (30s) against timestamps from 8+ hours ago
   - ActiveConnection.is_active is NOT being considered in the status determination
   - The heartbeat/activity timestamps are very stale, but the connection is still marked as "active"

✅ SOLUTION:
   - Modify ClientNodeMonitor.update_client_node_status() to:
     1. First check if ActiveConnection.is_active = True
     2. If active connection exists: status should be ACTIVE or INACTIVE (not NODE_FAILURE)
     3. Only mark NODE_FAILURE if is_active = False AND no heartbeat/activity for extended time
     
   - This aligns with the requirement:
     • NODE_FAILURE = Completely disconnected (is_active=False, no heartbeat)
     • INACTIVE = Connection established but screen off (is_active=True, no activity)
""")
