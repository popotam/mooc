# search.py
# ---------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

"""
In search.py, you will implement generic search algorithms which are called
by Pacman agents (in searchAgents.py).
"""

import collections
import util


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


def tinyMazeSearch(problem):
    """Returns a sequence of moves that solves tinyMaze.

    For any other maze, the sequence of moves will be incorrect,
    so only use this for tinyMaze

    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]


def nullHeuristic(state, problem=None):
    """Trivial heuristic"""
    return 0


State = collections.namedtuple("State", "node path cost")

STORAGE_FACTORIES = {
    'dfs': lambda problem, heuristic: util.Stack(),
    'bfs': lambda problem, heuristic: util.Queue(),
    'ucs': lambda problem, heuristic:
            util.PriorityQueueWithFunction(lambda x: x.cost),
    'astar': lambda problem, heuristic:
            util.PriorityQueueWithFunction(
                    lambda x: x.cost + heuristic(x.node, problem)),
}


def pathfinder_factory(algorithm):
    storage_factory = STORAGE_FACTORIES[algorithm]

    def pathfinder(problem, heuristic=nullHeuristic):
        closed = set()
        queue = storage_factory(problem, heuristic)
        queue.push(State(problem.getStartState(), (), 0))
        while not queue.isEmpty():
            state = queue.pop()
            # print state
            if problem.isGoalState(state.node):
                return list(state.path)
            if state.node in closed:
                continue
            closed.add(state.node)
            for raw_succesor in problem.getSuccessors(state.node):
                succesor = State(*raw_succesor)
                fringe_state = State(succesor.node,
                                     state.path + (succesor.path,),
                                     state.cost + succesor.cost)
                queue.push(fringe_state)

            if False and state.cost > 1010:
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
