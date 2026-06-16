import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cn_project.settings')
django.setup()

from django.contrib.auth.models import User
from network_sim.ai_congestion_predictor import AICongestionPredictor

print("=" * 70)
print("TESTING AI ANALYSIS IMPLEMENTATION")
print("=" * 70)

# Test 1: Extract features
print("\n1. Testing AICongestionPredictor.extract_features()...")
try:
    features = AICongestionPredictor.extract_features(time_window_seconds=300)
    print("✅ Features extracted successfully:")
    for key, value in features.items():
        print(f"   - {key}: {value}")
except Exception as e:
    print(f"❌ Error: {e}")

# Test 2: Get prediction
print("\n2. Testing AICongestionPredictor.predict_congestion()...")
try:
    prediction = AICongestionPredictor.predict_congestion()
    print("✅ Prediction generated successfully:")
    for key, value in prediction.items():
        print(f"   - {key}: {value}")
except Exception as e:
    print(f"❌ Error: {e}")

# Test 3: Check if admin user exists
print("\n3. Checking admin user...")
try:
    admin = User.objects.get(username='admin')
    print(f"✅ Admin user found: {admin.username} (is_staff={admin.is_staff})")
except User.DoesNotExist:
    print("❌ Admin user not found")

# Test 4: URL configuration
print("\n4. Checking URL configuration...")
from django.urls import reverse
try:
    url = reverse('admin_panel:api_explainable_ai_analysis')
    print(f"✅ URL configured: {url}")
except Exception as e:
    print(f"❌ Error: {e}")

# Test 5: Test the API function directly
print("\n5. Testing api_explainable_ai_analysis() directly...")
try:
    from admin_panel.network_api_views import api_explainable_ai_analysis
    from django.test import RequestFactory
    from django.contrib.auth.models import User
    
    # Create a test request
    factory = RequestFactory()
    request = factory.get('/admin/api/explainable-ai-analysis/')
    request.user = User.objects.get(username='admin')
    
    response = api_explainable_ai_analysis(request)
    print(f"✅ API function executed successfully")
    print(f"   Response status: {response.status_code}")
    
    import json
    data = json.loads(response.content)
    print(f"   Success: {data.get('success')}")
    print(f"   Risk Level: {data.get('prediction', {}).get('risk_level')}")
    print(f"   Confidence: {data.get('prediction', {}).get('confidence')}%")
    print(f"   Contributing Factors: {data.get('factor_count')}")
    
except Exception as e:
    import traceback
    print(f"❌ Error: {e}")
    traceback.print_exc()

print("\n" + "=" * 70)
print("API ENDPOINT DETAILS:")
print("=" * 70)
print("URL: http://localhost:8000/admin/api/explainable-ai-analysis/")
print("Panel URL: http://localhost:8000/admin/ai-analysis/")
print("Login: Admin credentials required")
print("=" * 70)
