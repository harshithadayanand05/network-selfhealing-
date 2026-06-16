#!/usr/bin/env python
"""
Enhanced Network Status Dashboard
Shows current node status with detailed information for troubleshooting
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cn_project.settings')
django.setup()

from network_sim.models import ClientNodeStatus, ActiveConnection, RequestLog
from students.models import Student
from django.utils import timezone
from datetime import timedelta

def print_header(title):
    print(f"\n{'='*90}")
    print(f"  {title.center(86)}")
    print(f"{'='*90}\n")

def print_node_card(student, node_status, active_conn):
    """Print a formatted card for each node"""
    status_icons = {
        'ACTIVE': '🟢 ACTIVE',
        'INACTIVE': '🟡 INACTIVE',
        'NODE_FAILURE': '🔴 NODE_FAILURE'
    }
    
    status_text = status_icons.get(node_status.status, '⚪ UNKNOWN')
    
    # Connection indicator
    conn_indicator = "✅ Connected" if active_conn else "❌ Disconnected"
    
    # Last activity
    if node_status.last_activity:
        now = timezone.now()
        time_diff = (now - node_status.last_activity).total_seconds()
        if time_diff < 60:
            last_activity_text = f"{int(time_diff)}s ago"
        elif time_diff < 3600:
            last_activity_text = f"{int(time_diff//60)}m ago"
        elif time_diff < 86400:
            last_activity_text = f"{int(time_diff//3600)}h ago"
        else:
            last_activity_text = f"{int(time_diff//86400)}d ago"
    else:
        last_activity_text = "Never"
    
    # IP address
    ip_text = node_status.ip_address if node_status.ip_address else "Not assigned"
    
    print(f"┌{'─'*88}┐")
    print(f"│ {status_text.ljust(15)} │ {student.user.username.upper().ljust(25)} │ {conn_indicator.ljust(15)} │")
    print(f"├{'─'*88}┤")
    print(f"│ IP Address: {ip_text.ljust(40)} │ Last Activity: {last_activity_text.ljust(15)} │")
    
    if node_status.connected_at:
        connected_time = node_status.connected_at.strftime('%Y-%m-%d %H:%M:%S')
        print(f"│ Connected: {connected_time.ljust(40)} │")
    
    print(f"└{'─'*88}┘")

# Main display
print_header("NETWORK MONITORING DASHBOARD")

current_time = timezone.now()
print(f"Current Time: {current_time.strftime('%Y-%m-%d %H:%M:%S UTC')}\n")

# Get all students
students = Student.objects.filter(
    user__is_staff=False, 
    user__is_superuser=False
).select_related('user').order_by('user__username')

# Statistics
total = 0
active = 0
inactive = 0
failed = 0

for student in students:
    node_status = ClientNodeStatus.objects.filter(student=student).first()
    if node_status:
        total += 1
        if node_status.status == 'ACTIVE':
            active += 1
        elif node_status.status == 'INACTIVE':
            inactive += 1
        elif node_status.status == 'NODE_FAILURE':
            failed += 1

# Summary statistics
print(f"\n{'SUMMARY STATISTICS'.center(90)}")
print(f"{'─'*90}")
print(f"Total Nodes: {total:<10} | 🟢 Active: {active:<10} | 🟡 Inactive: {inactive:<10} | 🔴 Failed: {failed:<10}")
print(f"{'─'*90}\n")

# Node details
print_header("DETAILED NODE STATUS")

# Sort by status and activity
nodes_data = []
for student in students:
    node_status = ClientNodeStatus.objects.filter(student=student).first()
    active_conn = ActiveConnection.objects.filter(student=student, is_active=True).exists()
    if node_status:
        nodes_data.append((student, node_status, active_conn))

# Sort: ACTIVE -> INACTIVE -> NODE_FAILURE
status_order = {'ACTIVE': 0, 'INACTIVE': 1, 'NODE_FAILURE': 2}
nodes_data.sort(key=lambda x: status_order.get(x[1].status, 3))

for student, node_status, active_conn in nodes_data:
    print_node_card(student, node_status, active_conn)

# Footer
print(f"\n{'='*90}")
print(f"  LEGEND:".ljust(86))
print(f"  🟢 ACTIVE      = User actively working on exam")
print(f"  🟡 INACTIVE    = System connected but idle (screen off)")
print(f"  🔴 NODE_FAILURE = Completely disconnected from network")
print(f"{'='*90}\n")

# Action items
print(f"\n{'ACTION ITEMS'.center(90)}")
print(f"{'─'*90}\n")

if failed > 0:
    print(f"⚠️  {failed} node(s) require attention:")
    for student, node_status, active_conn in nodes_data:
        if node_status.status == 'NODE_FAILURE':
            print(f"   • {student.user.username.upper()}: Check network connection, power status, and connectivity")
else:
    print(f"✅ All nodes are reachable on the network!")

if inactive > 0:
    print(f"\n✓ {inactive} node(s) are on standby (may resume work):")
    for student, node_status, active_conn in nodes_data:
        if node_status.status == 'INACTIVE':
            print(f"   • {student.user.username.upper()}: Ready for exam work")

print(f"\n{'─'*90}\n")
