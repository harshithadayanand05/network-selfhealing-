#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cn_project.settings')
django.setup()

from network_sim.client_node_monitor import ClientNodeMonitor

summary = ClientNodeMonitor.get_network_summary(timeout_seconds=60)

print(f"Total Nodes: {summary['total_nodes']}")
print(f"Active Nodes: {summary['active_nodes']}")
print(f"Inactive Nodes: {summary['inactive_nodes']}")
print(f"Failed Nodes: {summary['failed_nodes']}\n")

print("Status Breakdown:")
print("-" * 70)

for node in summary['client_nodes']:
    status_icon = node['status_badge']['icon']
    print(f"{status_icon} {node['username']:12} | {node['status']:12} | Last: {node['last_activity_formatted']:15}")
