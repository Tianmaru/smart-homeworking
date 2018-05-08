"""
@Maintainer Tom Schmidt
@Maintainer Stefan Poggenberg
@Maintainer Samuel Schöpa
@Maintainer Bjarne Hiller (216203851)
"""

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


# (b)
heuristics = {
    'Start': 304,
    '1': 272,
    '2': 219,
    '3': 189,
    '4': 253,
    '5': 318,
    '6': 150,
    '7': 383,
    '8': 57,
    'Ziel': 0
}


def heuristic(a, b):
    if a == 'Ziel':
        return heuristics[b]
    raise NotImplementedError


def a_star_search(graph, start, goal):
    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0
    
    while not frontier.empty():
        current = frontier.get()
        print("Visiting: %s with cost: %s" % (current, str(cost_so_far[current])))
        if current == goal:
            print("Goal found: %s" % str(goal))
            break
        
        # calculate new cost for each neighbor
        nn = graph.neighbors(current)
        for nextkey in nn.keys():
            nextcost = nn[nextkey]
            new_cost = cost_so_far[current] + nextcost
            if nextkey not in cost_so_far or new_cost < cost_so_far[nextkey]:
                cost_so_far[nextkey] = new_cost
                # notice the change in the call to the heuristic function in the next line:
                priority = new_cost + heuristic(goal, nextkey)
                frontier.put(nextkey, priority)
                came_from[nextkey] = current
    return came_from, cost_so_far


# (c)
def greedy_search(graph, start, goal):
    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0

    while not frontier.empty():
        current = frontier.get()
        print("Visiting: %s with cost: %s" % (current, str(cost_so_far[current])))
        if current == goal:
            print("Goal found: %s" % str(goal))
            break

        # calculate new cost for each neighbor
        nn = graph.neighbors(current)
        for nextkey in nn.keys():
            nextcost = nn[nextkey]
            new_cost = cost_so_far[current] + nextcost
            if nextkey not in cost_so_far or new_cost < cost_so_far[nextkey]:
                cost_so_far[nextkey] = new_cost
                # notice the change in the call to the heuristic function in the next line:
                priority = heuristic(goal, nextkey)
                frontier.put(nextkey, priority)
                came_from[nextkey] = current
    return came_from


class LabelledGraph:
    def __init__(self,edges):
        self.edges = edges
    
    def neighbors(self, id):
        return self.edges[id]


# (a)
edges = {
    'Start': {'1': 85, '2': 217, '7': 173},
    '1': {'Start': 85, '4': 80},
    '2': {'Start': 217, '5': 186, '6': 103},
    '3': {'6': 183},
    '4': {'1': 80, '8': 250},
    '5': {'2': 186},
    '6': {'2': 103, '3': 183, 'Ziel': 167},
    '7': {'Start': 173, 'Ziel' : 502},
    '8': {'4': 250, 'Ziel': 84},
    'Ziel': {'6': 167, '7': 502, '8': 84}
}

graph = LabelledGraph(edges)


# (d)
def reconstruct_path(came_from, start, goal):
    path = [goal]
    while not path[0] == start:
        path = [came_from[path[0]]] + path
    return path


if __name__ == '__main__':
    GREEDY = 'greedy'
    A_STAR = 'a*'
    algorithm = None
    while not (algorithm in [GREEDY, A_STAR]):
        algorithm = input('Give the search algorithm (%s / %s): ' % (GREEDY, A_STAR))
    if algorithm == GREEDY:
        came_from = greedy_search(graph, 'Start', 'Ziel')
    elif algorithm == A_STAR:
        came_from, cost_so_far = a_star_search(graph, 'Start', 'Ziel')
    print('Path: %s' % str(reconstruct_path(came_from, 'Start', 'Ziel')))
