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
import time

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
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best
        #time.sleep(7)
        print("New Position")


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
        foodLeft = [sum(val) for val in newFood]
        foodPositions = [(i,j.index(True)) for i,j in enumerate(newFood) if True in j]
        foodDistances = [manhattanDistance(newPos, pos) for pos in foodPositions]
        foodDistances.append(-1 if currentGameState.hasFood(newPos[0],newPos[1]) else 1000)
        foodDistances = [-1] if not foodDistances else foodDistances
        totalFoodLeft = sum(foodLeft)
        newGhostPositions = successorGameState.getGhostPositions()
        #newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        evalValue = (1/(totalFoodLeft + 1)) + (1/(min(foodDistances) + 2)) 
        distanceFromGhost = [manhattanDistance(newPos, position) for position in newGhostPositions]
        evalValue = -1 if min(distanceFromGhost) == 1 else evalValue 
        evalValue = -2 if min(distanceFromGhost) < 1 else evalValue 
        
        print(newPos)
        print(foodDistances)
        print(evalValue)
        #print(newGhostPositions)
        #print(distanceFromGhost)
        #return successorGameState.getScore()
        return evalValue

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

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        numAgents = gameState.getNumAgents()
        print(numAgents)
        legalMoves = gameState.getLegalActions(0)
        nextPossibleStates = [gameState.generateSuccessor(0, action) for action in legalMoves]
        scores = [self.calculateScore(state, self.depth, 1, self.evaluationFunction, 1, numAgents) for state in nextPossibleStates]
        print('final scores', scores)
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices)
        #time.sleep(4)
        #util.raiseNotDefined()
        return legalMoves[chosenIndex]
        
    def calculateScore(self, currentState, depth, currentLevel, evaluationFunction, agent, numAgents):
        #print('depth', currentLevel, agent, numAgents)
        if currentLevel == depth:
            return evaluationFunction(currentState)
        elif (currentState.isWin() | currentState.isLose()):
            #print('Critical state')
            return -500
        else:
            newAgent = (agent + 1) % numAgents
            legalMoves = currentState.getLegalActions(agent)
            nextPossibleStates = [currentState.generateSuccessor(agent, action) for action in legalMoves]
            scores = [self.calculateScore(state, depth, currentLevel+1, evaluationFunction, newAgent, numAgents) for state in nextPossibleStates]
            #print('scores', agent, scores)
            #print(currentLevel, newAgent, len(nextPossibleStates), len(legalMoves))
            if agent == 0:
                return max(scores)
            else:
                return min(scores)
            

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

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
        util.raiseNotDefined()

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
