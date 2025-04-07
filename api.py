from flask import Flask, jsonify, request
from finalenva import CustomSearchAndRescueEnv

app = Flask(__name__)

# Initialize once — GLOBAL ENV!
config = {
    "grid_size": 10,
    "num_agents": 1,
    "num_targets": 2,
    "observation_size": 3,
    "max_steps": 50,
    "output_file": "output.json"
}

env = CustomSearchAndRescueEnv(config)
obs = env.reset()
done = {"__all__": False}

@app.route("/", methods=["GET"])
def home():
    return "🚀 Search and Rescue Environment Ready"

@app.route("/step", methods=["POST"])
def step():
    global obs, done

    if done["__all__"]:
        env.close()
        return jsonify({"message": "Episode finished. Resetting environment."}), 200

    # Random actions or get from user
    actions = {agent: env.action_space.sample() for agent in env.agents}
    
    obs, rewards, done, info, agent_states = env.step(actions)

    step_info = {
        "step_number": env.time,
        "actions": actions,
        "rewards": rewards,
        "done": done["__all__"],
        "agent_states": agent_states
    }

    return jsonify(step_info), 200

@app.route("/reset", methods=["POST"])
def reset():
    global obs, done
    obs = env.reset()
    done = {"__all__": False}
    return jsonify({"message": "Environment reset"}), 200

if __name__ == "__main__":
    app.run(debug=True)
