  
from mesa import Agent


# class Cell(Agent):
    
#     def __init__(self, pos, model):

#         super().__init__(pos, model)
#         self.pos = pos
#         # Estado de la celda: Empty, Box
#         self.condition = "Empty"
#         self.nextCondition = ""
    
#     def step(self):
#         if self.nextCondition != "":
#             self.condition = self.nextCondition

class Roomba(Agent):
    """
    Agent that moves randomly.
    Attributes:
        unique_id: Agent's ID 
        direction: Randomly chosen direction chosen from one of eight directions
    """
    def __init__(self, unique_id, model):
        """
        Creates a new random agent.
        Args:
            unique_id: The agent's ID
            model: Model reference for the agent
        """
        super().__init__(unique_id, model)
        self.direction = 3
        self.can_move = True
        self.moves = 0
        # Self.conditon: Free, WithBox.
        self.condition = "Free"
        self.box = None

    def move(self):
        """ 
        Determines if the agent can move in the direction that was chosen
        """
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            #asi solo obtendra arriba,abajo,izq, der
            moore=False, # Boolean for whether to use Moore neighborhood (including diagonals) or Von Neumann (only up/down/left/right).
            include_center=True) 
        
        self.direction = self.random.randint(0,4)
        # Checks which grid cells are empty
        freeSpaces = []
        for pos in possible_steps:
            #cuando es otra roomba : obs
            canAppend = True
            for agent in self.model.grid.get_cell_list_contents(pos):
                #si es cualqui
                if (isinstance(agent, BorderAgent) or isinstance(agent,Roomba) or isinstance(agent,Trashcan)) or isinstance(agent,Box):
                    #si encuentra un agente agrega false a la lista disponible 
                        
                    canAppend = False
            
            freeSpaces.append(canAppend)

        print("Possible steps: %d" % len(possible_steps))

        #si la posicion a la que desea moverse es true
        if freeSpaces[self.direction]:
            #mueve el agente
            self.model.grid.move_agent(self, possible_steps[self.direction])
            print(f"Se mueve de {self.pos} a {possible_steps[self.direction]}; direction {self.direction}")
            self.moves += 1
            self.pos = possible_steps[self.direction]

    
    #metodo para agarrar la caja
    def clean(self):
        #obtener posibles posiciones
        print("SELF POS: ", self.pos)
        possible_steps = self.model.grid.get_neighborhood(self.pos,moore=False,include_center=True)
        self.direction = self.random.randint(0,4)

        for pos in possible_steps:
            #iterar alrededor de las posiciones para buscar una caja
            for agent in self.model.grid.get_cell_list_contents(pos):
                #si encuentra una caja y NO ESTA CARGANDO NINGUNA CAJA 
                if (self.condition == "Free" and isinstance(agent,Box)):
                    #guarda el agente encontrado y lo quita del grid
                    self.box= agent
                    self.model.grid.remove_agent(agent)
                    self.model.schedule.remove(agent)
                    #cambia su condicion de cargar la caja
                    self.condition = "WithBox"
                    print("CAJA ENCONTRADA----------------------------------------------------")
        #si no trae caja sigue buscando
        if self.condition == "Free":
            self.move()
            


   

    #metodo para crear o apilar cjas al boxesStack de cajas
    def findTrashcan(self):
        possible_steps = self.model.grid.get_neighborhood(self.pos,moore=True,include_center=True)

        #buscara en las posiciones disponibles el boxesStack de cajas
        for pos in possible_steps:
            for agent in self.model.grid.get_cell_list_contents(pos):
                #si encuentra el boxesStack y tiene menos de 5 cajas el boxesStack agrega la caja que trae al boxesStack
                if (self.condition == "WithBox" and isinstance(agent,Trashcan)):
                    if len(agent.boxesStack)<5:
                        #agrega la caja que tiene
                        agent.boxesStack.append(self.box)
                        #se cambia el estado a disponible para seguir buscando 
                        self.condition == "Free"
                        self.box= Box
                
                #SI SE ENCUENTRA CON OTRA CAJA Y YA ESTA CARGANDO UNA -> para que no se borre si encuentra una porque en mesa se borran
                elif (self.condition == "WithBox" and isinstance(agent,Box)):
                    #crea un obejto Trashcan
                    newTrashcan = Trashcan(agent.pos, self.model)

                    position = agent.pos

                    newTrashcan.boxesStack.append(agent)
                    self.model.grid.remove_agent(agent)
                    self.model.schedule.remove(agent)
                    self.model.schedule.add(newTrashcan)

                    #agrega la caja encontrada
                    newTrashcan.boxesStack.append(self.box)
                    self.model.grid.place_agent(newTrashcan,position)

                    self.condition = "Free"
                    self.box = Box
                    
        if self.condition == "WithBox":
            self.move()    
    #-----------------------------
    def step(self):
        """ 
        Determines the new direction it will take, and then moves
        """
        if self.condition == "Free":
            self.clean()
        else:
            self.findTrashcan()
            self.move()
            print("MOVING WITH BOX---------------------------------------------------------------")
        
        print(f"Agente: {self.unique_id} movimiento {self.direction}")
        

class BorderAgent(Agent):
    """
    Obstacle agent. Just to add obstacles to the grid.
    """
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        pass  

class Trashcan(Agent):
    def __init__(self, pos, model):
        super().__init__(pos,model)
        self.pos = pos
        self.boxesStack =[]  

class Box(Agent):
    def __init__(self, pos, model):
        super().__init__(pos,model)
        self.pos = pos
        

