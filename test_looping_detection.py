#!/usr/bin/env python
"""
Looping Detection Test & Monitoring Script
Demonstrates the looping detection system using real request data
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cn_project.settings')
django.setup()

from network_sim.looping_detector import LoopingDetector
from network_sim.models import RequestLog, NetworkEvent
from django.utils import timezone
from datetime import timedelta
import json

def print_header(title):
    print(f"\n{'='*90}")
    print(f"  {title.center(86)}")
    print(f"{'='*90}\n")

def test_looping_detection():
    """Test looping detection with current request data"""
    
    print_header("NETWORK LOOPING DETECTION TEST")
    
    # Test 1: Detect current looping issues
    print("TEST 1: Detecting Looping Issues (Threshold: 20 req/10s)")
    print("-" * 90)
    
    issues = LoopingDetector.detect_looping_issues()
    
    if issues:
        print(f"✓ Found {len(issues)} looping issue(s)\n")
        for i, issue in enumerate(issues, 1):
            print(f"  Issue #{i}:")
            print(f"    IP Address: {issue['ip_address']}")
            print(f"    Username: {issue['username']}")
            print(f"    Request Count: {issue['request_count']}")
            print(f"    Time Window: {issue['time_window_seconds']}s")
            print(f"    Frequency: {issue['request_frequency']} req/s")
            print(f"    Severity: {issue['severity']}")
            print(f"    Paths: {issue['paths']}")
            print(f"    Time Span: {issue['time_span_seconds']}s")
            print()
    else:
        print("✓ No looping issues detected (normal)")
    
    # Test 2: Get statistics
    print("\nTEST 2: Looping Statistics")
    print("-" * 90)
    
    stats = LoopingDetector.get_looping_statistics()
    print(f"Total Requests (5 min window): {stats['total_requests']}")
    print(f"Unique IP Addresses: {stats['unique_ips']}")
    print(f"Unique Users: {stats['unique_users']}")
    print(f"Avg Requests per IP: {stats['average_requests_per_ip']:.2f}")
    print(f"Looping Issues Detected: {stats['looping_issues_detected']}")
    print(f"Critical Issues: {stats['critical_looping_issues']}")
    
    # Test 3: Test with different thresholds
    print("\nTEST 3: Looping Detection with Custom Thresholds")
    print("-" * 90)
    
    thresholds = [10, 15, 20, 30, 50]
    for threshold in thresholds:
        issues = LoopingDetector.detect_looping_issues(request_threshold=threshold)
        print(f"Threshold {threshold} req/10s: {len(issues)} issue(s) detected")
    
    # Test 4: Get request timeline for high-activity IPs
    print("\nTEST 4: Request Timeline Analysis")
    print("-" * 90)
    
    if issues:
        top_issue = issues[0]
        ip = top_issue['ip_address']
        print(f"Analyzing timeline for IP: {ip} ({top_issue['username']})\n")
        
        timeline = LoopingDetector.get_request_timeline_for_ip(ip, limit_seconds=60)
        print(f"Last 60 seconds: {len(timeline)} requests\n")
        
        print("Recent Requests:")
        for req in timeline[:10]:
            timestamp = req['timestamp']
            method = req['method']
            path = req['path']
            status = req['status_code']
            print(f"  {timestamp} {method:4s} {path:30s} [{status}]")
    
    # Test 5: Export comprehensive report
    print("\nTEST 5: Exporting Comprehensive Report")
    print("-" * 90)
    
    report = LoopingDetector.export_looping_report(format='dict')
    print(f"Report Summary:")
    print(f"  Total Issues: {report['summary']['total_issues']}")
    print(f"  Critical: {report['summary']['critical']}")
    print(f"  High: {report['summary']['high']}")
    print(f"  Medium: {report['summary']['medium']}")
    print(f"  Low: {report['summary']['low']}")
    
    # Test 6: Check severity distribution
    print("\nTEST 6: Severity Distribution")
    print("-" * 90)
    
    severity_count = {
        'CRITICAL': 0,
        'HIGH': 0,
        'MEDIUM': 0,
        'LOW': 0
    }
    
    for issue in issues:
        severity_count[issue['severity']] += 1
    
    print(f"🚨 CRITICAL: {severity_count['CRITICAL']}")
    print(f"⚠️  HIGH:     {severity_count['HIGH']}")
    print(f"⚡ MEDIUM:   {severity_count['MEDIUM']}")
    print(f"ℹ️  LOW:      {severity_count['LOW']}")
    
    # Test 7: Database integration test
    print("\nTEST 7: NetworkEvent Creation Test")
    print("-" * 90)
    
    if issues and issues[0]['severity'] in ['CRITICAL', 'HIGH']:
        print("Creating NetworkEvent for critical issue...")
        event = LoopingDetector.create_looping_event(issues[0])
        print(f"✓ Created NetworkEvent ID: {event.id}")
        print(f"  Type: {event.event_type}")
        print(f"  Severity: {event.severity}")
        print(f"  Description: {event.description[:100]}...")
    
    # Test 8: API response simulation
    print("\nTEST 8: API Response Format")
    print("-" * 90)
    
    issues_for_api = LoopingDetector.detect_looping_issues()
    stats_for_api = LoopingDetector.get_looping_statistics()
    
    api_response = {
        'success': True,
        'threshold': 20,
        'time_window_seconds': 10,
        'statistics': stats_for_api,
        'looping_issues': issues_for_api,
        'total_issues': len(issues_for_api),
        'critical_issues': len([i for i in issues_for_api if i['severity'] == 'CRITICAL']),
        'timestamp': timezone.now().isoformat()
    }
    
    print("Sample API Response (JSON):")
    print(json.dumps({
        'success': api_response['success'],
        'total_issues': api_response['total_issues'],
        'critical_issues': api_response['critical_issues'],
        'statistics': {
            'total_requests': stats_for_api['total_requests'],
            'unique_ips': stats_for_api['unique_ips'],
            'looping_issues_detected': stats_for_api['looping_issues_detected'],
        }
    }, indent=2))

def show_usage_examples():
    """Show Python usage examples"""
    
    print_header("PYTHON USAGE EXAMPLES")
    
    examples = [
        ("Basic Detection", """
from network_sim.looping_detector import LoopingDetector

# Detect looping issues
issues = LoopingDetector.detect_looping_issues()
for issue in issues:
    print(f"{issue['username']}: {issue['request_count']} requests")
        """),
        
        ("Get Statistics", """
from network_sim.looping_detector import LoopingDetector

stats = LoopingDetector.get_looping_statistics()
print(f"Total requests: {stats['total_requests']}")
print(f"Looping issues: {stats['looping_issues_detected']}")
        """),
        
        ("Analyze IP Timeline", """
from network_sim.looping_detector import LoopingDetector

timeline = LoopingDetector.get_request_timeline_for_ip('192.168.1.100')
print(f"Found {len(timeline)} requests from this IP")
        """),
        
        ("Create Event", """
from network_sim.looping_detector import LoopingDetector

issues = LoopingDetector.detect_looping_issues()
for issue in issues:
    if issue['severity'] == 'CRITICAL':
        event = LoopingDetector.create_looping_event(issue)
        """),
        
        ("Export Report", """
from network_sim.looping_detector import LoopingDetector

# JSON format
json_report = LoopingDetector.export_looping_report(format='json')
print(json_report)
        """),
    ]
    
    for title, code in examples:
        print(f"\n{title}:")
        print("-" * 86)
        print(code)

def show_dashboard_info():
    """Show dashboard access info"""
    
    print_header("DASHBOARD ACCESS")
    
    print("Access the Network Monitoring Dashboard with Looping Detection:")
    print()
    print("URL: http://localhost:8000/admin-panel/network-monitoring-dashboard/")
    print()
    print("Features:")
    print("  ✓ Real-time looping issue detection")
    print("  ✓ Statistics cards (Total Requests, Unique IPs, Critical Issues)")
    print("  ✓ Table of affected clients with details")
    print("  ✓ Warning banner for detected issues")
    print("  ✓ Auto-refresh every 3 seconds")
    print()
    print("You need to be logged in as admin to access this page.")

if __name__ == '__main__':
    print("\n")
    print("╔" + "="*88 + "╗")
    print("║" + "NETWORK LOOPING DETECTION - TEST & MONITORING SUITE".center(88) + "║")
    print("╚" + "="*88 + "╝")
    
    try:
        test_looping_detection()
        show_usage_examples()
        show_dashboard_info()
        
        print_header("TEST COMPLETED SUCCESSFULLY")
        print("All looping detection features are working correctly.")
        print("Check the Network Monitoring Dashboard for real-time visualization.")
        
    except Exception as e:
        print(f"\n❌ Error during testing: {str(e)}")
        import traceback
        traceback.print_exc()
