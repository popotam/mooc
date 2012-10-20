# multiAgents.py
# --------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

import collections
from util import manhattanDistance
from game import Directions
import random
import util

from game import Agent

"""
In search.py, you will implement generic search algorithms which are called
by Pacman agents (in searchAgents.py).
"""


class SearchProblem:
    """
    This class outlines the structure of a search problem,
    but doesn't implement any of the methods
    (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must
        be composed of legal moves
        """
        util.raiseNotDefined()


def nullHeuristic(state, problem=None):
    """Trivial heuristic"""
    return 0


SearchNode = collections.namedtuple("SearchNode", "state path cost")

STORAGE_FACTORIES = {
    'dfs': lambda problem, heuristic: util.Stack(),
    'bfs': lambda problem, heuristic: util.Queue(),
    'ucs': lambda problem, heuristic:
            util.PriorityQueueWithFunction(lambda x: x.cost),
    'astar': lambda problem, heuristic:
            util.PriorityQueueWithFunction(
                    lambda x: x.cost + heuristic(x.state, problem)),
}


def pathfinder_factory(algorithm):
    storage_factory = STORAGE_FACTORIES[algorithm]

    def pathfinder(problem, heuristic=nullHeuristic):
        closed = set()
        queue = storage_factory(problem, heuristic)
        queue.push(SearchNode(problem.getStartState(), (), 0))
        while not queue.isEmpty():
            node = queue.pop()
            # print node
            if problem.isGoalState(node.state):
                # print node.path
                return list(node.path)
            if node.state in closed:
                continue
            closed.add(node.state)
            for raw_succesor in problem.getSuccessors(node.state):
                succesor = SearchNode(*raw_succesor)
                fringe_state = SearchNode(succesor.state,
                                          node.path + (succesor.path,),
                                          node.cost + succesor.cost)
                queue.push(fringe_state)

            if False and node.cost > 1010:
                break
    return pathfinder


depthFirstSearch = pathfinder_factory('dfs')
breadthFirstSearch = pathfinder_factory('bfs')
uniformCostSearch = pathfinder_factory('ucs')
aStarSearch = pathfinder_factory('astar')

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch


# searchAgents.py
# ---------------

from game import Actions
import time

import sys


class SearchAgent(Agent):
    """
    This very general search agent finds a path using a supplied search algorithm for a
    supplied search problem, then returns actions to follow that path.

    As a default, this agent runs DFS on a PositionSearchProblem to find location (1,1)

    Options for fn include:
      depthFirstSearch or dfs
      breadthFirstSearch or bfs


    Note: You should NOT change any code in SearchAgent
    """

    def __init__(self, fn='depthFirstSearch', prob='PositionSearchProblem',
                 heuristic='nullHeuristic'):
        # Warning: some advanced Python magic is employed below
        # to find the right functions and problems

        # Get the search function from the name and heuristic
        if fn not in dir(sys.modules[__name__]):
            raise AttributeError, fn + ' is not a search function in search.py.'
        func = getattr(sys.modules[__name__], fn)
        if 'heuristic' not in func.func_code.co_varnames:
            print('[SearchAgent] using function ' + fn)
            self.searchFunction = func
        else:
            if heuristic in globals().keys():
                heur = globals()[heuristic]
            elif heuristic in dir(sys.modules[__name__]):
                heur = getattr(sys.modules[__name__], heuristic)
            else:
                raise AttributeError, heuristic + ' is not a function in searchAgents.py or search.py.'
            print('[SearchAgent] using function %s and heuristic %s' % (fn, heuristic))
            # Note: this bit of Python trickery combines the search algorithm and the heuristic
            self.searchFunction = lambda x: func(x, heuristic=heur)

        # Get the search problem type from the name
        if prob not in globals().keys() or not prob.endswith('Problem'):
            raise AttributeError, prob + ' is not a search problem type in SearchAgents.py.'
        self.searchType = globals()[prob]
        print('[SearchAgent] using problem type ' + prob)

    def registerInitialState(self, state):
        """
        This is the first time that the agent sees the layout of the game board. Here, we
        choose a path to the goal.  In this phase, the agent should compute the path to the
        goal and store it in a local variable.  All of the work is done in this method!

        state: a GameState object (pacman.py)
        """
        if self.searchFunction == None: raise Exception, "No search function provided for SearchAgent"
        starttime = time.time()
        problem = self.searchType(state)  # Makes a new search problem
        self.actions = self.searchFunction(problem)  # Find a path
        totalCost = problem.getCostOfActions(self.actions)
        print('Path found with total cost of %d in %.1f seconds' % (totalCost, time.time() - starttime))
        if '_expanded' in dir(problem): print('Search nodes expanded: %d' % problem._expanded)

    def getAction(self, state):
        """
        Returns the next action in the path chosen earlier (in registerInitialState).  Return
        Directions.STOP if there is no further action to take.

        state: a GameState object (pacman.py)
        """
        if 'actionIndex' not in dir(self): self.actionIndex = 0
        i = self.actionIndex
        self.actionIndex += 1
        if i < len(self.actions):
            return self.actions[i]
        else:
            return Directions.STOP


class PositionSearchProblem(SearchProblem):
    """
    A search problem defines the state space, start state, goal test,
    successor function and cost function.  This search problem can be
    used to find paths to a particular point on the pacman board.

    The state space consists of (x,y) positions in a pacman game.

    Note: this search problem is fully specified; you should NOT change it.
    """

    def __init__(self, gameState, costFn=lambda x: 1,
                 goal=(1, 1), start=None, warn=True):
        """
        Stores the start and goal.

        gameState: A GameState object (pacman.py)
        costFn: A function from a search state (tuple) to a non-negative number
        goal: A position in the gameState
        """
        self.walls = gameState.getWalls()
        self.startState = gameState.getPacmanPosition()
        if start != None:
            self.startState = start
        self.goal = goal
        self.costFn = costFn
        if warn and (gameState.getNumFood() != 1 or not gameState.hasFood(*goal)):
            print 'Warning: this does not look like a regular search maze'

        # For display purposes
        self._visited, self._visitedlist, self._expanded = {}, [], 0

    def getStartState(self):
        return self.startState

    def isGoalState(self, state):
        isGoal = state == self.goal

        # For display purposes only
        if isGoal:
            self._visitedlist.append(state)
            import __main__
            if '_display' in dir(__main__):
                if 'drawExpandedCells' in dir(__main__._display):  # @UndefinedVariable
                    __main__._display.drawExpandedCells(self._visitedlist)  # @UndefinedVariable

        return isGoal

    def getSuccessors(self, state):
        """
        Returns successor states, the actions they require, and a cost of 1.

         As noted in search.py:
             For a given state, this should return a list of triples,
         (successor, action, stepCost), where 'successor' is a
         successor to the current state, 'action' is the action
         required to get there, and 'stepCost' is the incremental
         cost of expanding to that successor
        """

        successors = []
        for action in [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]:
            x, y = state
            dx, dy = Actions.directionToVector(action)
            nextx, nexty = int(x + dx), int(y + dy)
            if not self.walls[nextx][nexty]:
                nextState = (nextx, nexty)
                cost = self.costFn(nextState)
                successors.append((nextState, action, cost))

        # Bookkeeping for display purposes
        self._expanded += 1
        if state not in self._visited:
            self._visited[state] = True
            self._visitedlist.append(state)

        return successors

    def getCostOfActions(self, actions):
        """
        Returns the cost of a particular sequence of actions.  If those actions
        include an illegal move, return 999999
        """
        if actions == None: return 999999
        x, y = self.getStartState()
        cost = 0
        for action in actions:
            # Check figure out the next state and see whether its' legal
            dx, dy = Actions.directionToVector(action)
            x, y = int(x + dx), int(y + dy)
            if self.walls[x][y]: return 999999
            cost += self.costFn((x, y))
        return cost


class FarthestFoodSearchProblem(PositionSearchProblem):
    def __init__(self, food, gameState, costFn=lambda x: 1,
                 goal=(1, 1), start=None, warn=True):
        self.walls = gameState.getWalls()
        self.startState = gameState.getPacmanPosition()
        if start != None:
            self.startState = start
        self.goal = goal
        self.costFn = costFn
        if warn and (gameState.getNumFood() != 1 or not gameState.hasFood(*goal)):
            print 'Warning: this does not look like a regular search maze'

        # For display purposes
        self._visited, self._visitedlist, self._expanded = {}, [], 0
        self.food = food.copy()

    def isGoalState(self, state):
        x, y = state
        self.food[x][y] = False
        if self.food.count() == 0:
            return True
        return False


def manhattanHeuristic(position, problem, info={}):
    "The Manhattan distance heuristic for a PositionSearchProblem"
    xy1 = position
    xy2 = problem.goal
    return abs(xy1[0] - xy2[0]) + abs(xy1[1] - xy2[1])


def euclideanHeuristic(position, problem, info={}):
    "The Euclidean distance heuristic for a PositionSearchProblem"
    xy1 = position
    xy2 = problem.goal
    return ((xy1[0] - xy2[0]) ** 2 + (xy1[1] - xy2[1]) ** 2) ** 0.5


# ####################################################
# This portion is incomplete.  Time to write code!  #
# ####################################################


class AnyFoodSearchProblem(PositionSearchProblem):
    """
      A search problem for finding a path to any food.

      This search problem is just like the PositionSearchProblem, but
      has a different goal test, which you need to fill in below.  The
      state space and successor function do not need to be changed.

      The class definition above, AnyFoodSearchProblem(PositionSearchProblem),
      inherits the methods of the PositionSearchProblem.

      You can use this search problem to help you fill in
      the findPathToClosestDot method.
    """

    def __init__(self, gameState):
        "Stores information from the gameState.  You don't need to change this."
        # Store the food for later reference
        self.food = gameState.getFood()

        # Store info for the PositionSearchProblem (no need to change this)
        self.walls = gameState.getWalls()
        self.startState = gameState.getPacmanPosition()
        self.costFn = lambda x: 1
        self._visited, self._visitedlist, self._expanded = {}, [], 0

    def isGoalState(self, state):
        """
        The state is Pacman's position. Fill this in with a goal test
        that will complete the problem definition.
        """
        x, y = state
        return self.food[x][y]


def mazeDistance(point1, point2, gameState):
    """
    Returns the maze distance between any two points, using the search functions
    you have already built.  The gameState can be any game state -- Pacman's position
    in that state is ignored.

    Example usage: mazeDistance( (2,4), (5,6), gameState)

    This might be a useful helper function for your ApproximateSearchAgent.
    """
    x1, y1 = point1
    x2, y2 = point2
    walls = gameState.getWalls()
    assert not walls[x1][y1], 'point1 is a wall: ' + point1
    assert not walls[x2][y2], 'point2 is a wall: ' + str(point2)
    prob = PositionSearchProblem(gameState, start=point1, goal=point2, warn=False)
    return len(bfs(prob))


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
     * penalty for bfs distance to nearest food - weight is 1,
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
    if foods.count():
        nearest_food = len(bfs(AnyFoodSearchProblem(state)))
    else:
        nearest_food = 0

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
        return expectimax(gameState, self.depth, 0, betterEvaluationFunction)[0][0]
