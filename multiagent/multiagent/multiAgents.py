# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"
        
        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        closestghost=None
        for ghost in newGhostStates:
            if closestghost==None:
                closestghost=manhattanDistance(newPos, ghost.getPosition())
            else:
                if closestghost>manhattanDistance(newPos, ghost.getPosition()):
                    closestghost=manhattanDistance(newPos, ghost.getPosition())
        if closestghost:
            ghost_dist = -10/closestghost
        else:
            ghost_dist = -1000

        foodList = newFood.asList()
        #print(foodList)
        #raw_input()
        if len(foodList)>0:
            closestfood=None
            for food in foodList:
                if closestfood==None:
                    closestfood = manhattanDistance(newPos, food)
                else:
                    if manhattanDistance(newPos, food)<closestfood:    
                        closestfood = manhattanDistance(newPos, food)
        else:
            closestfood = 0

        # large weight to number of food left
        return (-1 * closestfood) + ghost_dist - (100*len(foodList))
        #please change the return score as the score you want

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        def MinimaxSearch(state,agentIndex,depth):
            if agentIndex==state.getNumAgents():
                #finish pacman and each ghost
                if depth==self.depth:
                    return self.evaluationFunction(state)
                    #arrive leaf node
                else:
                    return MinimaxSearch(state,0,depth+1)
                    #next layer start from pacman
            else:
                choice=state.getLegalActions(agentIndex)
                #list of legal movement for agent with agentIndex
                if len(choice)==0:
                    #no other choice
                    return self.evaluationFunction(state)
                next_choice=[]
                for c in choice:
                    next_choice.append(MinimaxSearch(state.generateSuccessor(agentIndex, c),agentIndex+1,depth))
                    #return state after agentIndex take cth choice
                if agentIndex==0:
                    return max(next_choice)
                    #Pacman's turn
                else:
                    return min(next_choice)
                    #one of the ghosts' turn
        ans=None
        ans_move=None
        for x in gameState.getLegalActions(0):
            if MinimaxSearch(gameState.generateSuccessor(0, x),1,1)>ans:
                ans_move=x
                ans=MinimaxSearch(gameState.generateSuccessor(0, x),1,1)
        return ans_move
        #util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        def MinimaxSearch(state,agentIndex,depth,alpha,beta):
            if agentIndex==state.getNumAgents():
                #finish pacman and each ghost
                if depth==self.depth:
                    return self.evaluationFunction(state)
                    #arrive leaf node
            
                else:
                    return MinimaxSearch(state,0,depth+1,alpha,beta)
                    #next layer start from pacman
            else:
                choice=state.getLegalActions(agentIndex)
                #list of legal movement for agent with agentIndex
                if len(choice)==0:
                    #no other choice
                    return self.evaluationFunction(state)
                next_choice_max=None
                next_choice_min=None
                if agentIndex==0:
                    #Pacman's turn Max layer
                    for c in choice:
                        temp=MinimaxSearch(state.generateSuccessor(agentIndex, c),agentIndex+1,depth,alpha,beta)
                        next_choice_max=max(temp,next_choice_max)
                        if temp>beta and beta is not None:
                            return temp
                        #update alpha
                        alpha=max(alpha,temp)
                    return next_choice_max
                else:
                    #one of the ghosts' turn min layer
                    for c in choice:
                        temp=MinimaxSearch(state.generateSuccessor(agentIndex, c),agentIndex+1,depth,alpha,beta)
                        if next_choice_min==None:
                            next_choice_min=temp
                        else:
                            next_choice_min=min(temp,next_choice_min)
                        if temp<alpha and alpha is not None:
                            return temp
                        if beta==None:
                            beta=temp
                        else:
                            beta=min(beta,temp)
                    return next_choice_min
        state=gameState
        val=None
        best=None
        a=None
        b=None
        for move in state.getLegalActions(0):
            val = max(val,MinimaxSearch(state.generateSuccessor(0, move), 1, 1, a, b)) 
            if a is None:
                a = val
                best = move
            else:
                if val > a:
                    a=max(val, a)
                    best=move
        return best
        #util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        def ExpectiSearch(state,agentIndex,depth):
            if agentIndex==state.getNumAgents():
                #finish pacman and each ghost
                if depth==self.depth:
                    return self.evaluationFunction(state)
                    #arrive leaf node
                else:
                    return ExpectiSearch(state,0,depth+1)
                    #next layer start from pacman
            else:
                choice=state.getLegalActions(agentIndex)
                #list of legal movement for agent with agentIndex
                if len(choice)==0:
                    #no other choice
                    return self.evaluationFunction(state)
                next_choice=[]
                for c in choice:
                    next_choice.append(ExpectiSearch(state.generateSuccessor(agentIndex, c),agentIndex+1,depth))          
                #return state after agentIndex take cth choice
                if agentIndex==0:
                    return max(next_choice)
                    #Pacman's turn
                else:
                    return (sum(next_choice)/len(next_choice))
                    #return min(next_choice)
                    #one of the ghosts' turn
        ans=None
        ans_move=None
        for x in gameState.getLegalActions(0):
            if ExpectiSearch(gameState.generateSuccessor(0, x),1,1)>ans:
                ans=ExpectiSearch(gameState.generateSuccessor(0, x),1,1)
                ans_move=x
        return ans_move
        #util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

