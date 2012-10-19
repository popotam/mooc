# multiAgents.py
# --------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

from util import manhattanDistance
from game import Directions
import random
import util

from game import Agent


class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.    You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """

    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to
        the evaluation function.

        Just like in the previous project, getAction takes a GameState
        and returns some Directions.X for some X in the set
        {North, South, West, East, Stop}

        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action)
                  for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores))
                       if scores[index] == bestScore]
        # Pick randomly among the best
        chosenIndex = random.choice(bestIndices)

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number,
        where higher numbers are better.

        The code below extracts some useful information from the state,
        like the remaining food (newFood) and Pacman position
        after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting,
        then combine them to create a masterful evaluation function.

        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer
                          for ghostState in newGhostStates]
        food_distances = [float(manhattanDistance(newPos, food))
                          for food in newFood.asList()]
        nearest_food = min(food_distances) if food_distances else 0
        ghost_distance = min(manhattanDistance(newPos, ghost.getPosition())
                             for ghost in newGhostStates)
        penalty = {
            0: 1000,
            1: 500,
        }.get(ghost_distance, 0)
        score = successorGameState.getScore()
        "*** YOUR CODE HERE ***"
        evaluation = score - 30 * len(food_distances) - nearest_food - penalty
        # suicide if score too low
        if score < -20 and ghost_distance > 0:
            print "*", score, sum(food_distances), len(food_distances), \
                nearest_food, ghost_distance, penalty, evaluation
            return -ghost_distance
        # print score, sum(food_distances), len(food_distances), nearest_food,
        # print ghost_distance, penalty, evaluation
        return evaluation


def scoreEvaluationFunction(currentGameState):
    """
        This default evaluation function just returns the score of the state.
        The score is the same one displayed in the Pacman GUI.

        This evaluation function is meant for use with adversarial
        search agents (not reflex agents).
    """
    return currentGameState.getScore()


class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.    Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent
    & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.
    Please do not remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.
    It's only partially specified, and designed to be extended.
    Agent (game.py) is another abstract class.
    """

    def __init__(self, evalFn='scoreEvaluationFunction', depth='2'):
        self.index = 0  # Pacman is always agent index 0
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

        Here are some method calls that might be useful
        when implementing minimax.

        gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

        Directions.STOP:
            The stop direction, which is always legal

        gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        num_agents = gameState.getNumAgents()
        maxdepth = self.depth

        def next_depth_and_agent(depth, agent):
            agent += 1
            if agent >= num_agents:
                return depth + 1, 0
            return depth, agent

        def minmax(state, depth, agent):
            if depth >= maxdepth:
                leaf_score = self.evaluationFunction(state)
                # print "leaf", depth, agent, leaf_score
                return [], leaf_score

            legal_actions = state.getLegalActions(agent)
            if not legal_actions:
                return [], self.evaluationFunction(state)

            if agent == 0:
                compare = lambda score, best_score: score > best_score
                best_score = -1000000
            else:
                compare = lambda score, best_score: score < best_score
                best_score = 1000000

            best_path = []
            for action in legal_actions:
                if action == Directions.STOP:
                    continue
                successor = state.generateSuccessor(agent, action)
                path, score = minmax(successor,
                                     *next_depth_and_agent(depth, agent))
                if compare(score, best_score):
                    best_path = [action] + path
                    best_score = score

            # print "node", depth, agent, best_score, best_path
            return best_path, best_score

        return minmax(gameState, 0, 0)[0][0]


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
        Returns the expectimax action using self.depth
        and self.evaluationFunction

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


class ContestAgent(MultiAgentSearchAgent):
    """
        Your agent for the mini-contest
    """

    def getAction(self, gameState):
        """Returns an action.

        You can use any method you want and search to any depth you want.
        Just remember that the mini-contest is timed, so you have to
        trade off speed and computation.

        Ghosts don't behave randomly anymore, but they aren't perfect either
        -- they'll usually just make a beeline straight towards Pacman
        (or away from him if they're scared!)

        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()
