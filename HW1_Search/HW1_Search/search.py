# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"

    node = problem.getStartState()
    frontier = util.Stack()
    path={}
    frontier.push(node)
    path[node]=[]
    
    visited = set()
    while not frontier.isEmpty():
        node = frontier.pop()
        visited.add(node)
        if problem.isGoalState(node):
            return path[node]
        mysuccess=problem.getSuccessors(node)
        for child in mysuccess:
            if child[0] not in visited:
                #print(child[0])
                frontier.push(child[0])
                path[child[0]]=path[node]+[child[1]]
            
    return []

    """
    util.raiseNotDefined()
    """

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"

    node = problem.getStartState()
    frontier = util.Queue()
    path={}
    frontier.push(node)
    path[node]=[]
    
    visited = set()
    while not frontier.isEmpty():
        node = frontier.pop()
        visited.add(node)
        if problem.isGoalState(node):
            return path[node]
        mysuccess=problem.getSuccessors(node)
        for child in mysuccess:
            if (child[0] not in visited) and (child[0] not in frontier.list):
                #print(child[0])
                frontier.push(child[0])
                path[child[0]]=path[node]+[child[1]]
            
    return []
    
    """
    util.raiseNotDefined()
    """

def uniformCostSearch(problem):
    """
    Search the node of least total cost first.
    "*** YOUR CODE HERE ***"
    """   
    node = problem.getStartState()
    path={}
    cost={}
    path[node]=[]
    cost[node]=0
    
    frontier = util.PriorityQueue()
    visited = set()
    
    frontier.push(node,0)
    visited.add(node)
    if problem.isGoalState(node):
        return path[node]
    
    while not frontier.isEmpty():
        node = frontier.pop()
        #print(node)
        #print(cost[node])
        if problem.isGoalState(node):
            return path[node]
        
        mysuccess=problem.getSuccessors(node)
        for child in mysuccess:
            if (child[0] not in visited)and(child[0] not in frontier.heap):
                #in heap still need update
                cost[child[0]]=cost[node]+child[2]
                path[child[0]]=path[node]+[child[1]]
                visited.add(child[0])
                frontier.update(child[0],cost[child[0]])
            else:
                if(cost[node]+child[2]<cost[child[0]]):
                    cost[child[0]]=cost[node]+child[2]
                    path[child[0]]=path[node]+[child[1]]
                    frontier.update(child[0],cost[child[0]])
    
    """
    util.raiseNotDefined()
    """
    
def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    node = problem.getStartState()
    path={}
    g={}
    f={}
    path[node]=[]
    g[node]=0
    f[node]=g[node]+heuristic(node, problem)
    
    frontier = util.PriorityQueue()
    visited = set()
    
    frontier.push(node,f[node])
    visited.add(node)
    if problem.isGoalState(node):
        return path[node]
    
    while not frontier.isEmpty():
        node = frontier.pop()
        #print(node)
        #print(cost[node])
        if problem.isGoalState(node):
            return path[node]
        
        mysuccess=problem.getSuccessors(node)
        for child in mysuccess:
            if (child[0] not in visited)and(child[0] not in frontier.heap):
                #in heap still need update
                g[child[0]]=g[node]+child[2]
                f[child[0]]=g[child[0]]+heuristic(child[0], problem)
                path[child[0]]=path[node]+[child[1]]
                visited.add(child[0])
                frontier.update(child[0],f[child[0]])
            else:
                if(g[node]+child[2]<g[child[0]]):
                    g[child[0]]=g[node]+child[2]
                    f[child[0]]=g[child[0]]+heuristic(child[0], problem)
                    path[child[0]]=path[node]+[child[1]]
                    visited.add(child[0])
                    frontier.update(child[0],f[child[0]])
                    
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
