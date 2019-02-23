"""
Finite Markov Decision Process (FMDP) Module.

This module contains the most basic functionality for a finite Markov decision
process. The basic components are a set of states, a set of actions and a set
of rewards. A FMDP process starts in an initial state, usually the same state
each time. An agent chooses an action, and the environment responds with a new
state and a reward according to a conditional probability function
p(S_t+1 = s', R_t+1 =r | S_t = s, A_t = a). This sequence of an action by the
agent followed by a response from the environment can terminate after a finite
number of times or continue indefinitely depending on the application.
Different applications will provide different implementations of a FMDP. The
environment's dynamics and an agent's policy are implemented as higher level
classes that use the classes in this module.

Classes:
    StateIF
    FMDPIF

Functions:

Constants:

Exceptions:
"""


import abc


class StateIF(abc.ABC):
    """
    Declares the methods that a state object implements.
    """

    @property
    @abc.abstractmethod
    def id(self):
        """
        Returns a state's unique id.
        """

        pass

    @abc.abstractmethod
    def __eq__(self, other):
        """
        Returns True if self and other are the same; False otherwise.

        Params:
            other: StateIF - another state object.
        """

        pass

    @abc.abstractmethod
    def __str__(self):
        """
        Returns a printable string representing the state.
        """

        pass

    @abc.abstractmethod
    def actions(self):
        """
        Returns a list of the possible actions. 

        Returns:
            list - a list of the possible actions.
            
        """

        pass


class ActionIF(abc.ABC):
    """
    Declares the methods that an action object implements.
    """

    pass


class FMDPIF(abc.ABC):
    """
    Declares the methods a finite Markov decision process (FMDP) implements.
    """

    @property
    @abc.abstractmethod
    def state(self):
        """
        Returns the current state of the FMDP.
        """

        pass

    @abc.abstractmethod
    def set_state(self, state):
        """
        Sets the current state of the FMDP. 

        Params:
            state: StateIF - a state object

        Returns:
            
        """

        pass

    @abc.abstractmethod
    def actions(self, state=None):
        """
        Returns a list of the possible actions for a given state. 

        Params:
            state: StateIF - a state object. If None, then a list of the
                actions for the current state is returned.

        Returns:
            list - a list of the possible actions.
            
        """

        pass

    @abc.abstractmethod
    def reset(self):
        """
        Resets the FMDP.

        This method resets the FMDP by returning it to its initial state and
        clears the FMDP's history.
        """

        pass


class TicTacToeState(StateIF):
    """
    This class implements a state in the game tic tac toe.

    A state in the game tic tac toe is a legal board position.
    """

    def __init__(self, board):
        """
        Initializes a tic tac toe state.

        Params:
            board: list - a 3x3 array of -1, 0, 1.  
        """

        self._board = board

        return


class TicTacToeGame(FMDPIF):
    """
    This class implements the game tic tac toe as a FMDP.
    """

    def __init__


