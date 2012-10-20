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

    def evaluationFunction(self, state, action):
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
        state = state.generatePacmanSuccessor(action)
        pos = state.getPacmanPosition()
        foods = state.getFood()
        ghosts = state.getGhostStates()
        food_distances = [float(manhattanDistance(pos, food))
                          for food in foods.asList()]
        nearest_food = min(food_distances) if food_distances else 0
        ghost_distance = min(manhattanDistance(pos, ghost.getPosition())
                             for ghost in ghosts)
        penalty = {
            0: 1000,
            1: 500,
        }.get(ghost_distance, 0)
        score = state.getScore()
        evaluation = score - 30 * len(food_distances) - nearest_food - penalty
        # suicide if score too low
        if score < -20 and ghost_distance > 0:
            print "*", score, sum(food_distances), len(food_distances), \
                nearest_food, ghost_distance, penalty, evaluation
            return -ghost_distance
        # print score, sum(food_distances), len(food_distances), nearest_food,
        # print ghost_distance, penalty, evaluation
        return evaluation


def scoreEvaluationFunction(state):
    """
        This default evaluation function just returns the score of the state.
        The score is the same one displayed in the Pacman GUI.

        This evaluation function is meant for use with adversarial
        search agents (not reflex agents).
    """
    return state.getScore()


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


def minmax(state, depth, agent, evaluate):
    if depth == 0:
        leaf_score = evaluate(state)
        # print "leaf", depth, agent, leaf_score
        return [], leaf_score

    legal_actions = state.getLegalActions(agent)
    if not legal_actions:
        return [], evaluate(state)

    # handle depth and agent
    next_agent = agent + 1
    next_depth = depth
    if next_agent >= state.getNumAgents():
        next_agent = 0
        next_depth -= 1

    # max or min
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

        # recurse
        path, score = minmax(successor, next_depth, next_agent, evaluate)

        # compare
        if compare(score, best_score):
            best_path = [action] + path
            best_score = score

    # print "node", depth, agent, best_score, best_path
    return best_path, best_score


def alphabeta(state, depth, agent, evaluate, alpha=(-1000000), beta=1000000):
    if depth == 0:
        leaf_score = evaluate(state)
        # print "leaf", depth, agent, leaf_score
        return [], leaf_score

    legal_actions = state.getLegalActions(agent)
    if not legal_actions:
        return [], evaluate(state)

    # handle depth and agent
    next_agent = agent + 1
    next_depth = depth
    if next_agent >= state.getNumAgents():
        next_agent = 0
        next_depth -= 1

    best_path = []
    for action in legal_actions:
        if action == Directions.STOP:
            continue
        successor = state.generateSuccessor(agent, action)

        # recurse
        path, score = alphabeta(successor, next_depth, next_agent, evaluate,
                                alpha, beta)

        # do alphabeta stuff
        if agent == 0:
            if alpha < score:
                alpha = score
                best_path = [action] + path
        else:
            if beta > score:
                beta = score
                best_path = [action] + path
        if beta <= alpha:
            break

    # print "node", depth, agent, alpha, beta, best_path
    return best_path, alpha if agent == 0 else beta


def expectimax(state, depth, agent, evaluate):
    if depth == 0:
        leaf_score = evaluate(state)
        # print "leaf", depth, agent, leaf_score
        return [], leaf_score

    legal_actions = state.getLegalActions(agent)
    if not legal_actions:
        return [], evaluate(state)

    # handle depth and agent
    next_agent = agent + 1
    next_depth = depth
    if next_agent >= state.getNumAgents():
        next_agent = 0
        next_depth -= 1

    scores = [
        (expectimax(state.generateSuccessor(agent, action),
                    next_depth, next_agent, evaluate),
         action)
        for action in legal_actions if action != Directions.STOP
    ]
    scores = [(score, index, path, action)
              for index, ((path, score), action) in enumerate(scores)]
    if agent == 0:
        best_score, _, path, action = max(scores)
        best_path = [action] + path
    else:
        best_score = sum([score[0] for score in scores]) / len(scores)
        best_path = ['random_ghost']

    # print "node", depth, agent, best_score, best_path
    return best_path, best_score


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
        return minmax(gameState, self.depth, 0, self.evaluationFunction)[0][0]


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
        Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        return alphabeta(gameState, self.depth, 0,
                         self.evaluationFunction)[0][0]


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
        return expectimax(gameState, self.depth, 0,
                          self.evaluationFunction)[0][0]


def betterEvaluationFunction(state):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION:
    It's really very simple, those are the factors I've used:
     * gameState score
     * penalty for manhatan distance to nearest food - weight is 1,
       just to push pacman in the correct direction (to break ties)
     * 30 points of penalty for every dot not eaten - 30 is enough to
       compensate for previous factor increasing due to eaten dot -
       this way pacman would not hesitate to eat a dot
     * 1000 penalty for walking on ghost or 500 for walking to a tile
       near a ghost - simple evasion
     * 1000 bonus for eating a scared ghost or 500 for walking to a tile
       near a scared ghost - this bonus is enabled only if previous
       penalty is not occuring (if there are no non-scared ghosts
       protecting their brethren)
     * 100 penalty for every capsule not eaten - simple way to make sure
       pacman eats a capsule, whenever he walks by it. On this layout
       pacman doesn't need to be proactive in hunting, he would walk near
       a capsule anyway.

    """
    GHOST_DISTANCE_FACTOR = {
        0: 1000,
        1: 500,
    }
    pos = state.getPacmanPosition()
    foods = state.getFood()
    ghosts = state.getGhostStates()
    not_eaten_capsules = len(state.getCapsules())

    # penalty for distance to nearest food
    food_distances = [float(manhattanDistance(pos, food))
                      for food in foods.asList()]
    nearest_food = min(food_distances) if food_distances else 0

    # ghost penalty
    ghost_distances = [manhattanDistance(pos, ghost.getPosition())
                       for ghost in ghosts if ghost.scaredTimer < 2]
    if ghost_distances:
        ghost_penalty = GHOST_DISTANCE_FACTOR.get(min(ghost_distances), 0)
    else:
        ghost_penalty = 0

    # ghost bonus
    scared_ghosts = [manhattanDistance(pos, ghost.getPosition())
                     for ghost in ghosts if ghost.scaredTimer >= 2]
    if not ghost_penalty and scared_ghosts:
        ghost_bonus = GHOST_DISTANCE_FACTOR.get(min(scared_ghosts), 0)
    else:
        ghost_bonus = 0

    # evaluate
    evaluation = (
        state.getScore()
        - 30 * foods.count()
        - nearest_food
        - ghost_penalty
        + ghost_bonus
        - 100 * not_eaten_capsules
    )
    return evaluation

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
