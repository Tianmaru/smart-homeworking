"""
@Author Martin Hoffmann
@Author Stefan Luedtke
@License CC BY
"""

import random
from tkinter import *

loc_A, loc_B = (0, 0), (1, 0) 

tk_master = Tk()
tk_master.resizable(False, False)
img_dirt = PhotoImage(file='dirt.png')
img_agent = PhotoImage(file='vacuum.png')

class Thing:
    """This represents any physical object that can appear in an Environment.
    You subclass Thing to get the things you want. Each thing can have a
    .__name__  slot (used for output only)."""

    def __repr__(self):
        return '<{}>'.format(getattr(self, '__name__', self.__class__.__name__))

    def is_alive(self):
        """Things that are 'alive' should return true."""
        return hasattr(self, 'alive') and self.alive

    def show_state(self):
        """Display the agent's internal state. Subclasses should override."""
        print("I don't know how to show_state.")

    def display(self, canvas, x, y, width, height):
        """Display an image of this Thing on the canvas."""
        pass



class Agent(Thing):
    """An Agent is a subclass of Thing with one required slot,
    .program, which should hold a function that takes one argument, the
    percept, and returns an action. (What counts as a percept or action
    will depend on the specific environment in which the agent exists.)
    Note that 'program' is a slot, not a method. If it were a method,
    then the program could 'cheat' and look at aspects of the agent.
    It's not supposed to do that: the program can only look at the
    percepts. An agent program that needs a model of the world (and of
    the agent itself) will have to build and maintain its own model.
    There is an optional slot, .performance, which is a number giving
    the performance measure of the agent in its environment."""
    def __init__(self, program):
        self.program = program
        
    def display(self, canvas, x, y, width, height):
        """Display an image of this Thing on the canvas."""
        canvas.create_image(x, y, image=img_agent, anchor=NW)

def TraceAgent(agent):
    """Wrap the agent's program to print its input and output. This will let
    you see what the agent is doing in the environment."""
    old_program = agent.program

    def new_program(percept):
        action = old_program(percept)
        print('{} perceives {} and does {}'.format(agent, percept, action))
        return action
    agent.program = new_program
    return agent


def ReflexVacuumAgent():
    def program(percept):
        #TODO
        if(percept[1]=="Dirty"):
            return "Suck"
        else:
            return random.choice(['Right', 'Left','Up','Down'])
    return Agent(program)


def ModelBasedVacuumAgent():
    """An agent that keeps track of what locations are clean or dirty."""
    model = {}
    direction = {(-1,0): 'Left', (1,0): 'Right', (0,-1): 'Up', (0,1): 'Down'}
    last_location = None
    last_move = None
    moves = None
    # destination = None
    
    def program(percept):
        nonlocal last_location
        nonlocal last_move
        nonlocal moves
        (x, y), status = percept
        model[(x, y)] = status

        if not ((x, y) == last_location):
            #  new location: check for unknown neighbors
            moves = [direction[(i, j)] for (i, j) in direction.keys() if not (x + i, y + j) in model]
            last_location = (x, y)
        else:
            #  last move had no effect: remove last_move
            if last_move in moves:
                moves.remove(last_move)

        if status == 'Dirty':
            #  Clean if location is dirty
            return 'Suck'
        elif len(moves) > 0:
            #  Into the unknown!
            last_move = random.choice(moves)
            return last_move
        else:
            return random.choice(['Right', 'Left', 'Up', 'Down'])
        
    return Agent(program)


class Environment:
    """Abstract class representing an Environment. 'Real' Environment classes
    inherit from this. Your Environment will typically need to implement:
        percept:           Define the percept that an agent sees.
        execute_action:    Define the effects of executing an action.
                           Also update the agent.performance slot.
    The environment keeps a list of .things and .agents (which is a subset
    of .things). Each agent has a .performance slot, initialized to 0.
    Each thing has a .location slot, even though some environments may not
    need this."""

    def __init__(self,size=(10,10)):
        self.things = []
        self.agents = []
        self.size=size
        
    def thing_classes(self):
        return []  # List of classes that can go into environment

    def percept(self, agent):
        """Return the percept that the agent sees at this point. (Implement this.)"""
        raise NotImplementedError

    def execute_action(self, agent, action):
        """Change the world to reflect this action. (Implement this.)"""
        raise NotImplementedError

    def default_location(self, thing):
        """Default location to place a new thing with unspecified location."""
        return None

    def exogenous_change(self):
        """If there is spontaneous change in the world, override this."""
        pass

    def step(self, canvas = None):
        """Run the environment for one time step. If the
        actions and exogenous changes are independent, this method will
        do. If there are interactions between them, you'll need to
        override this method."""
        actions = []
        for agent in self.agents:
            actions.append(agent.program(self.percept(agent)))
        for (agent, action) in zip(self.agents, actions):
            self.execute_action(agent, action)
        self.exogenous_change()
        if canvas!=None:
            canvas.delete("all")
            self.display(canvas)

    def run(self, steps=1000):
        """Run the Environment for given number of time steps."""
        for step in range(steps):
            self.step()

    def list_things_at(self, location, tclass=Thing):
        """Return all things exactly at a given location."""
        return [thing for thing in self.things
                if thing.location == location and isinstance(thing, tclass)]

    def some_things_at(self, location, tclass=Thing):
        """Return true if at least one of the things at location
        is an instance of class tclass (or a subclass)."""
        return self.list_things_at(location, tclass) != []

    def add_thing(self, thing, location=None):
        """Add a thing to the environment, setting its location. For
        convenience, if thing is an agent program we make a new agent
        for it. (Shouldn't need to override this.)"""
        if not isinstance(thing, Thing):
            thing = Agent(thing)
        if thing in self.things:
            print("Can't add the same thing twice")
        else:
            thing.location = location if location is not None else self.default_location(thing)
            self.things.append(thing)
            if isinstance(thing, Agent):
                thing.performance = 0
                self.agents.append(thing)

    def delete_thing(self, thing):
        """Remove a thing from the environment."""
        try:
            self.things.remove(thing)
        except ValueError as e:
            print(e)
            print("  in Environment delete_thing")
            print("  Thing to be removed: {} at {}".format(thing, thing.location))
            print("  from list: {}".format([(thing, thing.location) for thing in self.things]))
        if thing in self.agents:
            self.agents.remove(thing)

    def display(self, canvas):
        """Display the environment on the canvas, including all things (walls, agents)
        Further the state of each location is displayed, this needs to be implemented by subclasses."""
        width=int(canvas['width'])
        height=int(canvas['height'])
        for thing in self.things:
            x=thing.location[0]*100
            y=thing.location[1]*100
            thing.display(canvas, x, y, 100, 100)
        for x in range(self.size[0]+1):
            canvas.create_line(x*100,0,x*100,self.size[1]*100)
        for y in range(self.size[1]+1):
            canvas.create_line(0,y*100,self.size[0]*100,y*100)
        canvas.update()
        

    
class VacuumEnvironment2D(Environment):

    def __init__(self,size=(10,10)):
        super().__init__(size)
        self.status = {}
        for x in range(size[0]):
            for y in range(size[1]):
                self.status[(x,y)]=random.choice(['Clean', 'Dirty'])
        
    def thing_classes(self):
        return [Wall, Dirt, ReflexVacuumAgent, RandomVacuumAgent,
                TableDrivenVacuumAgent, ModelBasedVacuumAgent]

    def percept(self, agent):
        """Returns the agent's location, and the location status (Dirty/Clean)."""
        return (agent.location, self.status[agent.location])

    def execute_action(self, agent, action):
        """Change agent's location and/or location's status; track performance.
        Score 10 for each dirt cleaned; -1 for each move."""
        if action == 'Right':
            if(agent.location[0]<self.size[0]-1 
            and not (agent.location[0]+1,agent.location[1]) in
            map(lambda t: t.location,self.things)):
                agent.location = (agent.location[0]+1,agent.location[1])
            agent.performance -= 1
        elif action == 'Left':
            if(agent.location[0]>0 
            and not (agent.location[0]-1,agent.location[1]) in
            map(lambda t: t.location,self.things)):
                agent.location = (agent.location[0]-1,agent.location[1])
            agent.performance -= 1
        elif action == 'Up':
            if(agent.location[1]>0
            and not (agent.location[0],agent.location[1]-1) in
            map(lambda t: t.location,self.things)):
                agent.location = (agent.location[0],agent.location[1]-1)
            agent.performance -= 1
        elif action == 'Down':
            if(agent.location[1]<self.size[1]-1
            and not (agent.location[0],agent.location[1]+1) in
            map(lambda t: t.location,self.things)):
                agent.location = (agent.location[0],agent.location[1]+1)
            agent.performance -= 1
        elif action == 'Suck':
            if self.status[agent.location] == 'Dirty':
                agent.performance += 10
            self.status[agent.location] = 'Clean'

    def default_location(self, thing):
        """Agents start in either location at random."""
        return (random.randrange(self.size[0]),random.randrange(self.size[1]))
        
    def display(self, canvas):
        """Display the state of each location."""
        super().display(canvas)
        for x in range(self.size[0]):
            for y in range(self.size[1]):
                if(self.status[(x,y)]=='Dirty'):
                    canvas.create_image(x*100+1,y*100+50, image=img_dirt, anchor=NW)
        canvas.update()


def performance(environment):
    performance = []
    for thing in environment.things:
        if hasattr(thing, 'performance'):
            performance.append(thing.performance)
    return performance

e = VacuumEnvironment2D((8,6))
e.add_thing(TraceAgent(ModelBasedVacuumAgent()))
e.add_thing(TraceAgent(ModelBasedVacuumAgent()))
e.add_thing(TraceAgent(ReflexVacuumAgent()))
c=Canvas(tk_master,width=800,height=600, background='white')
c.pack();
tk_master.bind("<space>",lambda event: e.step(c))
tk_master.bind("<p>",lambda event: print('Performance: '+str(performance(e))))
tk_master.after(0,lambda: e.display(c))
mainloop()
