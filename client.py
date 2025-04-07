import requests
import time
import json

SERVER_URL = "http://127.0.0.1:5000"

print("👟 Starting client.py...\n")

# Check if server is running
try:
    r = requests.get(SERVER_URL)
    r.raise_for_status()
    print(f"✅ GET / -> {r.status_code} 🚀 Search and Rescue Environment Ready\n")
except requests.exceptions.RequestException as e:
    print(f"❌ Failed to connect to server: {e}")
    exit(1)

# Step simulation
for step in range(50):  # simulate 50 steps
    try:
        r = requests.post(f"{SERVER_URL}/step")
        r.raise_for_status()
        data = r.json()

        print(f"✅ POST /step [{step}] -> {r.status_code}")
        print(json.dumps({
            "step_number": data.get("step_number"),
            "actions": data.get("actions"),
            "rewards": data.get("rewards"),
            "done": data.get("done")
        }, indent=2))

        # Show detailed agent state if available
        agent_states = data.get("agent_states", {})
        for state in agent_states:
            agent_id = state["agent_id"]
            print(f"\n🎯 Agent `{agent_id}` full state at Step {step}:")
            print(json.dumps(state, indent=2))

            if state.get("victim_found", False):
                print(f"🚨 Victim FOUND by {agent_id} at position {state.get('position')}!\n")

        print("—" * 60)
        if data.get("done"):
            print("🏁 Environment episode complete. Exiting client.")
            break

        time.sleep(0.5)

    except requests.exceptions.RequestException as e:
        print(f"❌ Error during POST /step [{step}]: {e}")
        break
