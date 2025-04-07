import requests
import time

SERVER_URL = "http://127.0.0.1:5000"

print("👟 Starting client.py...")

# Check environment is live
r = requests.get(SERVER_URL)
print(f"✅ GET / -> {r.status_code} {r.text}")

for i in range(20):  # simulate 20 steps
    r = requests.post(f"{SERVER_URL}/step")
    print(f"✅ POST /step [{i}] -> {r.status_code}")
    print(r.json())
    time.sleep(1)  # optional pause between steps
