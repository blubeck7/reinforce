"""
Finite Markov Decision Process (FMDP) Module.

This module contains the basic functionality of a finite Markov decision
process. The basic components are a set of states, a set of actions and a set
of rewards. A FMDP process starts in an initial state, usually the same state
each time. An agent chooses an action, and the environment responds with a new
state and a reward according to a conditional probability function
p(S_t+1 = s', R_t+1 =r | S_t = s, A_t = a). This sequence of an action by the
agent followed by a response from the environment can terminate after a finite
number of times or continue indefinitely depending on the application. In this
library, a FMDP is implemented as a bundling of states, actions, rewards and an
environment. The environment is everything that can not be arbitrarily changed
by an agent. The purporse of the environment is to calculate rewards and state
transitions based on the current state and a given action.

Classes:
    FMDPIF
    EnvironmentIF
    StateIF
    ActionIF

Functions:

Constants:

Exceptions:
"""


import abc


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
        """

        pass

    @abc.abstractmethod
    def is_terminal(self):
        """
        Returns True if the current state is the terminal state.
        """

        pass

    @abc.abstractmethod
    def get_actions(self, state=None):
        """
        Returns a list of the possible actions for a given state. 

        Params:
            state: StateIF - a state object. If None, then a list of the
                actions for the current state is returned.

        Returns:
            list[ActionIF] - a list of the possible actions.
            
        """

        pass

    @abc.abstractmethod
    def next(self, action):
        """
        Updates the FMDP.

        This method transitions the FMDP to a new state and gives a reward
        based on the environment's dynamics.

        Params:
            action: ActionIF - the chosen action.
        """

        pass

    @property
    @abc.abstractmethod
    def env(self):
        """
        The FMDP's environment.

        Returns:
            EnvIF - the environemnt object.
        """

        oass

    @abc.abstractmethod
    def set_env(self, env):
        """
        Sets the environment.  

        Params:
            env: EnvIF - a environment object. 
        """

        pass

    @property
    @abc.abstractmethod
    def history(self):
        """
        Returns the history of the FMDP's states, actions and rewards.

        Returns:
            list - a list of tuples. Each tuple has three elements. The first
                element is the state, the second element is the action and the
                third element is the reward. The tuples are in order of the
                time they were encountered from earliest to latest.
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

    @abc.abstractmethod
    def display(self):
        """
        Displays the FMDP as a printable string.
        """

        pass





    # deprecated
    @property
    @abc.abstractmethod
    def agents(self):
        """
        Returns a dictionary of the registered agents for the FMDP.
        """

        pass

    @abc.abstractmethod
    def run(self):
        """
        Runs the FMDP according to its specific environment and rules.
        """

        pass

#    @abc.abstractmethod
#    def do_action(self, action):
#        """
#        Updates the FMDP with the given action.
#
#        Params:
#            action: ActionIF - the action to do.
#        """
#
#        pass
#
#    @abc.abstractmethod
#    def do_env(self):
#        """
#        Simulates the environment one step based the current state, choosen
#        action and environment dynamics.
#        """
#
#        pass
#
    @abc.abstractmethod
    def step(self):
        """
        Performs a single step of the FMDP.
        """

        pass


class EnvIF(abc.ABC):
    """
    Declares the methods that an environment object implements.
    """

    @abc.abstractmethod
    def next(self, state, action):
        """
        Returns the next state and a reward.

        This method takes a state and action and then according to its dynamics
        p(s',r|s,a), the environment returns the next state and a reward.

        Params:
            state: StateIF - the current state.
            action: ActionIF - the chosen action.

        Returns:
            StateIF, float - the next state and reward tuple.
        """

        pass


class StateIF(abc.ABC):
    """
    Wrapper class for a state object.

    This class functions as a data structure that stores all the information
    about a state needed to implement the environment's dynamics. In addition,
    it declares a few basic methods that apply to any state object independent
    of the actual application.
    """

    @abc.abstractmethod
    def display(self):
        """
        Displays the state as a printable string.
        """

        pass

    @abc.abstractmethod
    def is_terminal(self):
        """
        Returns True if the terminal state.

        The terminal state is the state that transitions to itself and rewards
        zero.
        """

        pass


class ActionIF(abc.ABC):
    """
    Declares the methods that an action object implements.
    """

    @property
    @abc.abstractmethod
    def agent_key(self):
        """
        Returns the key of the agent who chose the action.
        """

        pass

    @abc.abstractmethod
    def display(self):
        """
        Displays the action as a printable string.
        """

        pass

    @abc.abstractmethod
    def is_null(self):
        """
        Returns true if the null action.
        """

        pass


class NullAction(ActionIF):
    """
    Defines the null action object.

    The null action is the action that represents inability to take any normal
    action. For example, it may not be the action's turn to act according to
    the state and dynamics of the FMDP.
    """

    def __init__(self, agent_key):
        """
        Initializes the null action. 

        Params:
            agent_key: int|str - the key of the agent who chose the null
                action.
        """

        self._agent_key = agent_key

    @property
    def agent_key(self):
        return self._agent_key

    def display(self):
        print("null action")

    def is_null(self):
        return True


#class TurnGame(FMDP):
    #"""
    #Defines base class for turn based games
    #"""
#
    #pass


