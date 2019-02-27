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

        self._agents = {XAGENT: None, OAGENT: None} 
        self._init_state = TicTacToeState(XAGENT, [[0] * 3] * 3)
        self._state = self._init_state

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

    def actions(self, state=None, *args, **kwargs):
        if state:
            return state.actions(*args, **kwargs)

        return self._state.actions(*args, **kwargs)
    
    def do_action(self, action):
        
        pass

    def do_env(self):

        pass

    def reset(self):

        pass

    @property
    def history(self):
        pass

    def do_turn(self):
        # for each agent in order do:
        #    get the agent's action
        #    do the environment
        #    update the state and reward
        #    record current state, action, next state and reward
        # do environment

        xagent = self.agents[tictactoe.XAGENT]
        xagent.choose


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
        pass

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

    def actions(self, state=None, *args, **kwargs):
        actions = list()
        for row in range(NROWS):
            for col in range(NCOLS):
                if self._board[row][col] == 0:
                    actions.append((row, col))
        
        return actions


class TicTacToeAction(fmdp.ActionIF):
    """
    This class defines an action in tic tac toe.
    """
    
    def __init__(self, 
