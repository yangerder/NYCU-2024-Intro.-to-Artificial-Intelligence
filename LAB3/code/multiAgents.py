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
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and child states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        The evaluation function takes in the current and proposed child
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.
        """
        # Useful information you can extract from a GameState (pacman.py)
        childGameState = currentGameState.getPacmanNextState(action)
        newPos = childGameState.getPacmanPosition()
        newFood = childGameState.getFood()
        newGhostStates = childGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        minGhostDistance = min([manhattanDistance(newPos, state.getPosition()) for state in newGhostStates])

        scoreDiff = childGameState.getScore() - currentGameState.getScore()

        pos = currentGameState.getPacmanPosition()
        nearestFoodDistance = min([manhattanDistance(pos, food) for food in currentGameState.getFood().asList()])
        newFoodsDistances = [manhattanDistance(newPos, food) for food in newFood.asList()]
        newNearestFoodDistance = 0 if not newFoodsDistances else min(newFoodsDistances)
        isFoodNearer = nearestFoodDistance - newNearestFoodDistance

        direction = currentGameState.getPacmanState().getDirection()
        if minGhostDistance <= 1 or action == Directions.STOP:
            return 0
        if scoreDiff > 0:
            return 8
        elif isFoodNearer > 0:
            return 4
        elif action == direction:
            return 2
        else:
            return 1


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
    Your minimax agent (Part 1)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.getNextState(agentIndex, action):
        Returns the child game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        # Begin your code (Part 1)
        """
        1. check foe termination condition if the game is win or lose
        or if it reach the limit depth terminal
        2.Expand the node find all legal action for current agent and 
        remove the stop action(to make it faster) calculate the next state
        of game
        3. Recursive case handling if current agent is not the last one
        call minimax ,if it is last start a new depth level with first agent
        4. if the agent is pacman retrun the max or the action
        if is enemy return the min
        """
        def minimax(state, depth, agentIndex):
            isTerminal = state.isWin() or state.isLose()
            if isTerminal or depth == self.depth:
                return self.evaluationFunction(state)
            valnodes=[]
            actions=state.getLegalActions(agentIndex)
            if Directions.STOP in actions:
                actions.remove(Directions.STOP)
            for action in actions:
                nextstate=state.getNextState(agentIndex, action)
                if (agentIndex !=(gameState.getNumAgents()-1)):
                    valnodes.append(minimax(nextstate, depth, agentIndex+1))
                else:
                    valnodes.append(minimax(nextstate,depth+1,0))
            if agentIndex==0:
                if depth==0:
                    best_score = max(valnodes)
                    best_action_index = valnodes.index(best_score)
                    return actions[best_action_index]
                else:
                    return max(valnodes)
            else:
                return min(valnodes)
        return minimax(gameState, 0, 0)
        # End your code (Part 1)


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (Part 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        # Begin your code (Part 2)
        """
        1. Check for termination condition: if the game is won or lost, or if it reaches
          the limit depth, then return the evaluation of the current state.
        2. Expand the node: Find all legal actions for the current agent and remove the STOP 
        action to keep the game moving. Calculate the next state of the game.
        3. Recursive case handling: If the current agent is not the last one, call alphabeta 
        for the next agent. If it is the last agent, start a new depth level with the first agent.
        4. Apply alpha-beta pruning to cut off branches that cannot possibly affect the final decision:
        - If the agent is Pac-Man (maximizer), update alpha with the maximum value found and
          prune the remaining branches if alpha is greater than to beta.
        - If the agent is an enemy (minimizer), update beta with the minimum value found and
          prune the remaining branches if beta is less than to alpha.
        5. If the agent is Pac-Man, return the max value or the best action; if it is an enemy,
          return the min value.
        """
        def alphabeta(state, depth, agentIndex, alpha, beta):
            isTerminal = state.isWin() or state.isLose()
            if isTerminal or depth == self.depth:
                return self.evaluationFunction(state)
            actions = state.getLegalActions(agentIndex)
            if Directions.STOP in actions:
                actions.remove(Directions.STOP)
            if agentIndex == 0:
                bestValue = float("-inf")
                bestAction = None
                for action in actions:
                    nextState = state.getNextState(agentIndex, action)
                    value = alphabeta(nextState, depth, agentIndex + 1, alpha, beta)
                    if value > bestValue:
                        bestValue = value
                        bestAction = action
                    alpha = max(alpha, bestValue)
                    if beta < alpha:
                        break  
                if depth == 0:
                    return bestAction
                else:
                    return bestValue
            else:
                minValue = float("inf")
                for action in actions:
                    nextState = state.getNextState(agentIndex, action)
                    if (agentIndex ==(gameState.getNumAgents()-1)):
                        value = alphabeta(nextState, depth + 1, 0, alpha, beta)
                    else:
                        value = alphabeta(nextState, depth, agentIndex+1, alpha, beta)
                    minValue = min(minValue, value)
                    beta = min(beta, minValue)
                    if beta < alpha:
                        break  
                return minValue
        return alphabeta(gameState, 0, 0, float("-inf"), float("inf"))
        # End your code (Part 2)


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (Part 3)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        # Begin your code (Part 3)
        """
        1. check foe termination condition if the game is win or lose
        or if it reach the limit depth terminal
        2.Expand the node find all legal action for current agent and 
        remove the stop action(to make it faster) calculate the next state
        of game
        3. Recursive case handling if current agent is not the last one
        call minimax ,if it is last start a new depth level with first agent
        4. if the agent is pacman retrun the max or the action
        if is enemy return the expected value
        """
        def expectimax(state, depth, agentIndex):
            isTerminal = state.isWin() or state.isLose()
            if isTerminal or depth == self.depth:
                return self.evaluationFunction(state)
            valnodes=[]
            actions=state.getLegalActions(agentIndex)
            if Directions.STOP in actions:
                actions.remove(Directions.STOP)
            for action in actions:
                nextstate=state.getNextState(agentIndex, action)
                if (agentIndex !=(gameState.getNumAgents()-1)):
                    valnodes.append(expectimax(nextstate, depth, agentIndex+1))
                else:
                    valnodes.append(expectimax(nextstate,depth+1,0))
            if agentIndex==0:
                if depth==0:
                    best_score = max(valnodes)
                    best_action_index = valnodes.index(best_score)
                    return actions[best_action_index]
                else:
                    return max(valnodes)
            else:
                return sum(valnodes)/len(valnodes)
        return expectimax(gameState, 0, 0)
        # End your code (Part 3)


def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (Part 4).
    """
    # Begin your code (Part 4)
    """
    1. Calculate the basic score from the current game state.
    2. Determine the Pac-Man's current position, list of remaining food, and capsules.
    3. Calculate distances to the nearest food item, nearest capsule, and scared ghosts.
    4. Calculate additional scores based on these distances and the number of remaining food items to prioritize food 
    collection, capsule collection, and chasing scared ghosts.
    5. Return the total score which includes the base game score and bonuses from food, capsules, and scared ghosts.
    """
    score = currentGameState.getScore()
    pos = currentGameState.getPacmanPosition()
    foodList = currentGameState.getFood().asList()
    capsuleList = currentGameState.getCapsules()
    ghostStates = currentGameState.getGhostStates()
    
    minFoodDist = float('inf')
    minCapsuleDist = float('inf')
    scaredGhostDist = float('inf')

    for food in foodList:
        minFoodDist=min(minFoodDist,manhattanDistance(pos,food))
    for capsule in capsuleList:
        minCapsuleDist=min(minCapsuleDist,manhattanDistance(pos,capsule))
    for ghost in ghostStates:
        if ghost.scaredTimer>0:
            scaredGhostDist=min(scaredGhostDist,manhattanDistance(pos, ghost.getPosition()))
    foodRemainingScore =len(foodList)
    return score+(30/(minFoodDist+foodRemainingScore))+(45/(minCapsuleDist))+(500/(scaredGhostDist))
    # End your code (Part 4)

# Abbreviation
better = betterEvaluationFunction
