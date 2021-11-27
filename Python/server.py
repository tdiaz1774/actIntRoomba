from mesa.visualization.modules import CanvasGrid, ChartModule, PieChartModule
from agent import Roomba, BorderAgent, Trashcan, Box
from model import RandomModel
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter
from flask import Flask, request, jsonify

cellColors = {"Empty": "#FFFFFF", "Box": "#89250D"}
robotColors = {"WithBox": "red", "Free": "green"}
def agent_portrayal(agent):
    if agent is None: return
    
    if (isinstance(agent, Roomba)):
        portrayal = {
            "Shape": "circle",
            "w": 1,
            "h": 1,
            "Filled": "true",
            "Layer": 0, 
            "Color": "red",
            "r": 1
        }

        #(x, y) = agent.pos

        # portrayal["x"] = x
        # portrayal["y"] = y
        # portrayal["Color"] = robotColors[agent.condition]
        # portrayal["Color"] = "red"

    if (isinstance(agent, Box)):
        portrayal = {"Shape": "rect",
                    "Filled": "true",
                    "Layer": 1,
                    "Color": "brown",
                    "w": 1,
                    "h": 1}

    if (isinstance(agent, BorderAgent)):
        portrayal = {"Shape": "circle",
                    "Filled": "true",
                    "Layer": 2,
                    "Color": "grey",
                    "r": 0.2}

    if (isinstance(agent, Trashcan)):
        portrayal = {"Shape": "rect",
                    "Filled": "true",
                    "Layer": 3,
                    "Color": "blue",
                    "r": 1}
        # if len(agent.boxesStack)==5:
        #     portrayal["Color"] = "red"

    return portrayal

def RobotPortrayal(agent):
    if agent is None:
        return

    if (isinstance(agent, Box)):
        portrayal = {"Shape": "rect",
                    "Filled": "true",
                    "Layer": 1,
                    "Color": "brown",
                    "w": 1,
                    "h": 1}
        
            
    if (isinstance(agent, Roomba)):
        portrayal = {
            "Shape": "circle",
            "Filled": "true",
            "r": 0.5
        }
        if agent.condition == "Free":
            portrayal["Color"] = "green"
            portrayal["Layer"] = 0
        else:
            portrayal["Color"] = "red"
            portrayal["Layer"] = 1

    if (isinstance(agent, BorderAgent)):
        portrayal = {
            "Shape": "circle",
            "Color": "grey",
            "Layer": 0,
            "Filled": "true",
            "r": 0.2
        }
    
    if (isinstance(agent, Trashcan)):
        portrayal = {
            "Shape": "rect",
            "w": 0.7,
            "h": 0.7,
            "Layer": 0,
            "Filled": "true"
        }
        if len(agent.boxesStack)==2:
            portrayal["Color"] = "yellow"
        elif len(agent.boxesStack)==3:
            portrayal["Color"] = "orange"
        elif len(agent.boxesStack)==4:
            portrayal["Color"] = "red"
        else:
            portrayal["Color"] = "purple"
        
            
    return portrayal


# tree_chart = ChartModule(
#     [{"Label": label, "Color": color} for (label, color) in cellColors.items()]
# )
# pie_chart = PieChartModule(
#     [{"Label": label, "Color": color} for (label, color) in cellColors.items()]
# )
#( N, width, height, density, maxSteps, nBoxes):
model_params = {
    "N": UserSettableParameter("slider", "Number of rumbas", 2, 1, 10, 1),
    "width": UserSettableParameter("slider", "Width", 15, 6, 15, 1),
    "height": UserSettableParameter("slider", "Height", 15, 6, 15, 1),
    "density": UserSettableParameter("slider", "Dirty cells density", 0.1, 0.01, 1.0, 0.1),
    "maxSteps": UserSettableParameter("slider", "Maximum steps", 40, 20, 100, 5),
    "nBoxes": UserSettableParameter("slider", "Number of boxes", 2, 1, 10, 1)
}

#grid = CanvasGrid(agent_portrayal, 15, 15, 500, 500)
grid = CanvasGrid(RobotPortrayal, 15, 15, 500, 500)
#[grid, tree_chart, pie_chart]
server = ModularServer(RandomModel, [grid], "Esperanzita", model_params)


server.port = 8590 # The default
server.launch()

# app = Flask("Traffic example")
# @app.route('/init', methods=['POST', 'GET'])
# def initModel():
#     global currentStep, trafficModel, number_agents, width, height

#     if request.method == 'POST':
#         number_agents = int(request.form.get('NAgents'))
#         width = int(request.form.get('width'))
#         height = int(request.form.get('height'))
#         currentStep = 0

#         print(request.form)
#         print(number_agents, width, height)
#         #(N, width, height, density, maxSteps, nBoxes)
#         trafficModel = RandomModel(model_params["N"], model_params["width"], height)

#         return jsonify({"message":"Parameters recieved, model initiated."})

# @app.route('/getAgents', methods=['GET'])
# def getAgents():
#     global trafficModel

#     if request.method == 'GET':
#         carPositions = [{"x": x, "y":1, "z":z} for (a, x, z) in trafficModel.grid.coord_iter() if isinstance(a, RandomAgent)]

#         return jsonify({'positions':carPositions})

# @app.route('/getObstacles', methods=['GET'])
# def getObstacles():
#     global trafficModel

#     if request.method == 'GET':
#         carPositions = [{"x": x, "y":1, "z":z} for (a, x, z) in trafficModel.grid.coord_iter() if isinstance(a, ObstacleAgent)]

#         return jsonify({'positions':carPositions})

# @app.route('/update', methods=['GET'])
# def updateModel():
#     global currentStep, trafficModel
#     if request.method == 'GET':
#         trafficModel.step()
#         currentStep += 1
#         return jsonify({'message':f'Model updated to step {currentStep}.', 'currentStep':currentStep})