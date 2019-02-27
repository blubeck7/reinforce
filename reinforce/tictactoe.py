"""
Tic Tac Toe Module.

This module contains all of the tic tac toe specifc objects for reinforcement
learning.

Classes:
    TicTacToeGame - Implmentation of tic tac toe as a finite Markov decision
        process.
    TicTacToeState -
    TicTacToeAction - 

Functions:
Constants:
Exceptions:
"""


#from reinforce import agent
from reinforce import fmdp


XAGENT = "x"
OAGENT = "o"
NROWS = 3
NCOLS = 3


class TicTacToeGame(fmdp.FMDPIF):
    """
    This class implements the game tic tac toe as a FMDP.
    """

    def __init__(self):
        """
        Initializes a new tic tac toe game.
        """
        # agents: dict - the agents or players for the game.
        # init_state: StateIF - the starting board for the game.
        # state: StateIF - the current board for the game.
        # history: list - a list of tuples, where each tuple records the state,
        #    action and reward for a given step.

        self._agents = {XAGENT: None, OAGENT: None} 
        self._init_state = TicTacToeState(XAGENT, [[0] * 3] * 3)
        self._state = self._init_state
        self._history = []
        self._step = 0

        return

    @property
    def agents(self):
        return self._agents

    def set_agent(self, key, agent):
        self._agents[key] = agent

    @property
    def state(self):
        return self._state

    def set_state(self, state):
        self._state = state

    def display(self):
        self._state.display()

        return

    def get_actions(self, state=None):
        if state:
            return self._get_actions(state)

        return self._get_actions(self._state)

    def _get_actions(self, state):
        actions = [] 
        for row in range(NROWS):
            for col in range(NCOLS):
                if state._board[row][col] == 0:
                    action = TicTacToeAction(state.agent_key, row, col)
                    actions.append(action)

        return actions

    def step(self):
        pass
    
    def reset(self):
        pass

    @property
    def history(self):
        pass

    def run(self):
        # for each agent in order do:
        #    get the agent's action
        #    do the environment
        #    update the state and reward
        #    record current state, action, next state and reward
        # do environment

        agent = self.agents[self.state.agent_key]
        action = agent.get_action(self.state)


class TicTacToeState(fmdp.StateIF):
    """
    This class implements a state in the game tic tac toe.

    A state in the game tic tac toe consists of a legal board position and the
    key of the agent whose turn it is.
    """

    def __init__(self, agent_key, board):
        """
        Initializes a tic tac toe state.

        Params:
            agent_key: hashable - the number of the agent whose turn it is.
            board: list - a 3x3 array of -1, 0, 1.  
        """

        self._agent_key = agent_key
        self._board = board

        return

    @property
    def agent_key(self):
        return self._agent_key

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return False

        for row in range(NROWS):
            for col in range(NCOLS):
                if other._board[row][col] != self._board[row][col]:
                    return False

        return True

    def display(self):
        print("Turn: {}".format(self._agent_key))

        for row in range(NROWS):
            print(" " + str(row), end="")
        print()

        for row in range(NROWS):
            print(row, end="")
            for col in range(NCOLS):
                if self._board[row][col] == 0:
                    print(" ", end="")
                elif self._board[row][col] == 1:
                    print("X", end="")
                else:
                    print("O", end="")
                if col != NCOLS - 1:
                    print("|", end="")
                else:
                    print()
            if row != NROWS - 1:
                print(" -----")

    def is_null(self):
        return False


class TicTacToeAction(fmdp.ActionIF):
    """
    This class defines an action in tic tac toe.
    """
    
    def __init__(self, agent_key, row, col):
        """
        Initializes a tic tac toe action.

        Params:
            agent_key: hashable - the key of the agent who chose the action.
            row: int - row number
            col: int - column number
        """

        self._agent_key = agent_key
        self._row = row
        self._col = col

    @property
    def agent_key(self):
        return self._agent_key

    @property
    def row(self):
        return self._row

    @property
    def col(self):
        return self._col

    def display(self):
        print("row: {} col: {}".format(self._row, self._col))
