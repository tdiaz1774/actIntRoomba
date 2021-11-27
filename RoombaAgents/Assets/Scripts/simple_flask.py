
# Coordinate server using Flask


from flask import Flask, request, jsonify
from random import uniform
num_agents = 0
limit = 10
app = Flask("Coordinate server")
def random_point():
    """ Generate a new 3D coordinate """
    return {"x": uniform(-limit, limit),
            "y": uniform(-limit, limit),
            "z": uniform(-limit, limit)}


@app.route("/")

def default():
    #  Test Function for flask
    print("Recieved request at /")
    return "This is working!!!"

@app.route("/config", methods={'POST'})
def configure():
    """ Set up the simulation """
    global num_agents
    num_agents = int(request.form.get("numAgents"))
    print(f"Recieved num agentes = {num_agents}")
    return jsonify({"OK": num_agents})

@app.route("/update", methods=['GET'])
def update_positions():
    # Create a list of 3D points
    points = [random_point() for _ in range(num_agents)]
    print(f"Positions: {points}")
    return jsonify({"positions": points})


app.run()
