#!/usr/bin/env python3
"""
Simple test to check which packages are available
"""

print("🧪 Testing package imports...")
print("=" * 40)

# Test core packages
packages = [
    ("flask", "Flask web framework"),
    ("flask_cors", "Flask CORS"),
    ("flask_jwt_extended", "JWT authentication"),
    ("requests", "HTTP requests"),
    ("bcrypt", "Password hashing"),
    ("dotenv", "Environment variables"),
    ("PIL", "Pillow image processing"),
    ("numpy", "NumPy"),
    ("cv2", "OpenCV"),
    ("geopy", "Location services"),
    ("pymongo", "MongoDB"),
    ("ultralytics", "YOLOv8"),
    ("twilio", "SMS service"),
    ("firebase_admin", "Firebase")
]

working = []
missing = []

for package, description in packages:
    try:
        __import__(package)
        print(f"✅ {package} - {description}")
        working.append(package)
    except ImportError:
        print(f"❌ {package} - {description}")
        missing.append(package)

print("\n" + "=" * 40)
print(f"📊 Working packages: {len(working)}/{len(packages)}")
print(f"✅ Working: {', '.join(working)}")
print(f"❌ Missing: {', '.join(missing)}")

if len(working) >= 5:
    print("\n🎉 Enough packages are working! You can run the application.")
    print("💡 Missing packages will use demo mode.")
else:
    print("\n⚠️ Not enough packages working. Try installing more packages.")

print("\n🚀 To start the app, run: python app.py")
