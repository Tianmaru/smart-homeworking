import collections
import heapq
import math
import sys

class Queue:
    def __init__(self):
        self.elements = collections.deque()
    
    def empty(self):
        return len(self.elements) == 0
    
    def put(self, x):
        self.elements.append(x)
    
    def get(self):
        return self.elements.popleft()

class Stack:
    def __init__(self):
        self.elements = []
    
    def empty(self):
        return len(self.elements) == 0
    
    def put(self, x):
        self.elements.append(x)
    
    def get(self):
        return self.elements.pop()


class PriorityQueue:
    def __init__(self):
        self.elements = []
    
    def empty(self):
        return len(self.elements) == 0
    
    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))
    
    def get(self):
        return heapq.heappop(self.elements)[1]


class SimpleGraph:
    def __init__(self,edges):
        self.edges = edges
    
    def neighbors(self, id):
        return self.edges[id]


def heuristic(a, b):
    #TODO


def a_star_search(graph, start, goal):
    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0
    
    while not frontier.empty():
        current = frontier.get()
        print("Visiting: ",end="")
        print(current,end="")
        print(" with cost: ",end="")
        print(cost_so_far[current])
        if current == goal:
            print("Goal found: ",end="")
            print(goal)
            break
        
        #calculate new cost for each neighbor
        nn = graph.neighbors(current)
        for nextkey in nn.keys():
            nextcost = nn[nextkey]
            new_cost = cost_so_far[current] + nextcost
            if nextkey not in cost_so_far or new_cost < cost_so_far[nextkey]:
                cost_so_far[nextkey] = new_cost
                #notice the change in the call to the heuristic function in the next line:
                priority = new_cost + heuristic(goal, nextkey)
                frontier.put(nextkey, priority)
                came_from[nextkey] = current
   
    return came_from, cost_so_far


def greedy_search(graph, start, goal):
   #TODO
   
    return came_from


class LabelledGraph:
    def __init__(self,edges):
        self.edges = edges
    
    def neighbors(self, id):
        return self.edges[id]


#TODO: Main