from flask import Flask, request, jsonify
from finalenva import CustomSearchAndRescueEnv  # Replace with your module if needed
import random
import json

app = Flask(__name__)

# Config for your environment
config = {
    "grid_size": 10,
    "num_agents": 2,
    "num_targets": 2,
    "observation_size": 3,
    "max_steps": 50,
    "output_file": "output.json"
}

# Load environment
env = CustomSearchAndRescueEnv(config)
observations = env.reset()
done = {"__all__": False}


@app.route('/', methods=['GET'])
def home():
    return "Search & Rescue Environment is Running. Use POST /step to interact."


@app.route('/step', methods=['POST'])
def step():
    global observations, done

    if done["__all__"]:
        return jsonify({"message": "Episode finished. Resetting environment."}), 200

    actions = {agent: env.action_space.sample() for agent in env.agents}  # random actions
    observations, rewards, done, info = env.step(actions)

    # Latest state for all agents
    latest_data = env.data_to_log[-len(env.agents):]

    if done["__all__"]:
        env.close()

    return jsonify(latest_data), 200


@app.route('/reset', methods=['POST'])
def reset():
    global observations, done
    observations = env.reset()
    done = {"__all__": False}
    return jsonify({"message": "Environment reset!"}), 200


@app.route('/run_until_found', methods=['POST'])
def run_until_found():
    global env
    obs = env.reset()
    done = {"__all__": False}
    victim_found = False
    final_info = None

    while not done["__all__"] and not victim_found:
        actions = {agent: env.action_space.sample() for agent in env.agents}
        obs, rewards, done, infos = env.step(actions)

        for agent in env.agents:
            # Check if victim was found in the recent log
            recent_state = env.data_to_log[-len(env.agents):]
            for state in recent_state:
                if state["agent_id"] == agent and state.get("victim_found"):
                    final_info = state
                    final_info["path_taken"] = env.agent_paths[agent]
                    victim_found = True
                    break
            if victim_found:
                break

    if final_info:
        return jsonify(final_info), 200
    else:
        return jsonify({"message": "Victim not found within max steps."}), 404


if __name__ == '__main__':
    app.run(debug=True)
