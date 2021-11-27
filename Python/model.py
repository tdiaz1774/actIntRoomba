from mesa import Model
from mesa.time import RandomActivation
from mesa.space import Grid
from mesa.datacollection import DataCollector

from agent import Roomba, BorderAgent, Box, Trashcan

class RandomModel(Model):
    """ 
    Creates a new model with random agents.
    Args:
        N: Number of agents in the simulation
        height, width: The size of the grid to model
    """
    def __init__(self, N, width, height, density, maxSteps, nBoxes):
        self.numAgents = N
        self.numBoxes = nBoxes
        self.grid = Grid(width,height,torus = False) 
        self.schedule = RandomActivation(self)
        self.running = True 
        self.steps = 0
        self.maxSteps = maxSteps
        #self.gridSize = (width-2)*(height-2)
        #self.trashCan = (0,0)
        #self.forbiddenCoords = []

        

        # self.datacollector = DataCollector(
        #     {
        #         "Cant. Movimientos": lambda m: self.countMovs(m),
        #         "Cajas": lambda m: self.countBoxes(m),
        #     }
        # )

        # Crea borde
        border = [(x,y) for y in range(height) for x in range(width) if y in [0, height-1] or x in [0, width - 1]]

        for pos in border:
            obs = BorderAgent(pos, self)
            self.schedule.add(obs)
            self.grid.place_agent(obs, pos)

        #-Agregar rumbas
        for i in range(self.numAgents):
            a = Roomba(i+1000, self) 
            x= self.random.randint(1,width-2)
            y= self.random.randint(1,height-2)
            while not self.grid.is_cell_empty((x, y)):
                x= self.random.randint(1,width-2)
                y= self.random.randint(1,height-2)
                print("dentro del while-----------------")
                
            self.grid.place_agent(a, (x, y))
            self.schedule.add(a)
            print("x: ", x ," y: ",y)
                    
            #pos = (1,1)
            #self.grid.place_agent(a, pos)

        # #nBoxes = 0

        # Agregar cajas
        for i in range(self.numBoxes):
            while True:
                x= self.random.randint(1,width-2)
                y= self.random.randint(1,height-2)
                if self.grid.is_cell_empty((x, y)):
                    caja = Box((x, y), self)
                    self.grid.place_agent(caja, (x, y))
                    self.schedule.add(caja)
                    break
        
        # #self.nBoxes = nBoxes

        # self.datacollector.collect(self) 
    
    def step(self):
        '''Advance the model by one step.'''
        self.schedule.step()

        #self.datacollector.collect(self)

        print("Agent moves = %d" % self.countMovs(self))
        
        self.steps += 1

        if self.steps >= self.maxSteps-1:
            self.running = False

        # if self.countBoxes(self) == self.numBoxes:
        #     self.running = False

    
    @staticmethod
    def countMovs(model):
        count = 0
        for agent in model.schedule.agents:
            if isinstance(agent, Roomba):
                    count += agent.moves
        return count

    @staticmethod
    def countBoxes(model):
        count  = 0
        for agent in model.schedule.agents:
            if isinstance(agent, Box):
                count+1
        return (count)
