"""
Finite Markov Decision Process (FMDP) Module.

This module contains the basic functionality of a finite Markov decision
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


class FMDPIF(abc.ABC):
    """
    Declares the methods a finite Markov decision process (FMDP) implements.
    """

    @property
    @abc.abstractmethod
    def agents(self):
        """
        Returns a dictionary of the registered agents for the FMDP.
        """

        pass

    @abc.abstractmethod
    def set_agent(self, key, agent):
        """
        Sets an agent.  

        Params:
            key: hashable - the agent's key.
            agent: AgentIF - an agent object
        """

        pass

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
    def display(self):
        """
        Displays the FMDP as a printable string.
        """

        pass

    @abc.abstractmethod
    def actions(self, state=None, *args, **kwargs):
        """
        Returns a list of the possible actions for a given state. 

        Params:
            state: StateIF - a state object. If None, then a list of the
                actions for the current state is returned.
            args: tuple - optional positional arguments that depend on the
                specifc FMDP.
            kwargs: dict - optional keyword arguments that depend on the
                specifc FMDP.

        Returns:
            list[ActionIF] - a list of the possible actions.
            
        """

        pass

    @abc.abstractmethod
    def do_action(self, action):
        """
        Updates the FMDP with the given action.

        Params:
            action: ActionIF - the action to do.
        """

        pass

    @abc.abstractmethod
    def do_env(self):
        """
        Simulates the environment one step based the current state, choosen
        action and environment dynamics.
        """

        pass

    @abc.abstractmethod
    def do_step(self):
        """
        Performs a single step
        """

        pass

    @abc.abstractmethod
    def run(self):
        """
        Runs the FMDP according to its specific environment and rules.
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


class StateIF(abc.ABC):
    """
    Wrapper class for a state object.

    This class functions as a data structure that stores all the information
    about a state. In addition, it declares a few basic methods that apply to
    any state object independent of the actual FMDP.
    """

    @property
    @abc.abstractmethod
    def agent_key(self):
        """
        Returns the key of the agent whose turn it is.
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
    def display(self):
        """
        Displays the state as printable string.
        """

        pass

    @abc.abstractmethod
    def actions(self, *args, **kwargs):
        """
        Returns a list of the possible actions. 

        Params:
            args: tuple - optional positional arguments that depend on the
                specifc FMDP.
            kwargs: dict - optional keyword arguments that depend on the
                specifc FMDP.

        Returns:
            list - a list of the possible actions.
            
        """

        pass


class ActionIF(abc.ABC):
    """
    Declares the methods that an action object implements.
    """

    @property
    def agent(self):
        """
        Returns the agent that choose the action.
        """

        pass


class NullState(StateIF):
    """
    Null state object.

    This class defines the null state, which is a state that always transitions
    to itself and rewards zero.
    """

    def __init__(self, agent_key):
        """
        Initializes the null state.

        Params:
            agent_key: hashable - the agent whose is in the null state.
        """

        self._agent_key = agent_key
        self._is_null = True

    @property
    def agent_key(self):
        return self._agent_key

    @abc.abstractmethod
    def __eq__(self, other):
        pass

    @abc.abstractmethod
    def display(self):
        pass

    @abc.abstractmethod
    def actions(self, *args, **kwargs):
        return []
