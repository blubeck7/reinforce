"""
Tic Tac Toe Module.

This module contains all of the tic tac toe specifc objects for reinforcement
learning.
"""


import fmdp


class TicTacToeState(fmdp.StateIF):
    """
    This class implements a state in the game tic tac toe.

    A state in the game tic tac toe is a legal board position.
    """

    NROWS = 3
    NCOLS = 3

    def __init__(self, uid, board):
        """
        Initializes a tic tac toe state.

        Params:
            uid: int - unique id
            board: list - a 3x3 array of -1, 0, 1.  
        """

        self._uid = uid        
        self._board = board

        return

    @property
    def uid(self):

        return self._uid

    def __eq__(self, other):
        pass

    def display(self):
        for row in range(self.NROWS):
            print(" " + str(row), end="")
        print()

        for row in range(self.NROWS):
            print(row, end="")
            for col in range(self.NCOLS):
                if self._board[row][col] == 0:
                    print(" ", end="")
                elif self._board[row][col] == 1:
                    print("X", end="")
                else:
                    print("O", end="")
                if col != self.NCOLS - 1:
                    print("|", end="")
                else:
                    print()
            if row != self.NROWS - 1:
                print(" -----")
        print() 

        return

    def actions(self, state=None, *args, **kwargs):
        actions = list()
        for row in range(self.NROWS):
            for col in range(self.NCOLS):
                if self._board[row][col] == 0:
                    actions.append((row, col))
        
        return actions


class TicTacToeAction(fmdp.ActionIF):
    """
    This class defines an action in tic tac toe.
    """

    

class TicTacToeGame(fmdp.FMDPIF):
    """
    This class implements the game tic tac toe as a FMDP.
    """

    def __init__(self):
        """
        Initializes a new tic tac toe game.
        """
        # state: StateIF - starts in the initial state

        self._state = TicTacToeState(0, [[0] * 3] * 3)

        return

    @property
    def state(self):
        
        return self._state

    def set_state(self, state):

        pass

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
