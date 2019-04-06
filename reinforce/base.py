#TODO: For now keep all the abstract reinforcement learning code in this file.
#TODO: May break it out into multiple files later.
#TODO: Break FMDPIF class into known and unknown dynamics
"""
Base Module

This module contains the interfaces to create classes that are specific to a
given application and can be used by the various reinforcement learning
algorithms.

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
import random


class FMDPIF(abc.ABC):
    """
    Declares the methods a finite Markov decision process (FMDP) implements.

    A known FMDP is one in which the environment's dynamics are explicity
    known. In other words, the function p(s',r|s,a) is specified.
    """
    @property
    @abc.abstractmethod
    def agent(self):
        """
        Returns the agent for the FMDP and the agent's key.

        Returns:
            (AgentIF, int) - a tuple containing the agent and its key. 
        """

        pass

    @abc.abstractmethod
    def set_agent(self, agent, key):
        """
        Sets the agent for the FMDP.

        Params:
            agent: AgentIF - an agent object to use.
            key: int - the agent's identifier for the FMDP.
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
    def list_actions(self, state=None, key=None):
        """
        Lists the possible actions from a given state.

        Params:
            key: int - the key of the agent for whom to list the possible
                actions.
            state: StateIF - a state object, if None then the current state is
                used.

        Returns:
            list[ActionIF] - a list where each element is a possible action.
        """

        pass

    @abc.abstractmethod
    def list_responses(self, action, state=None):
        """
        Lists the possible responses for an action from a given state.

        Params:
            action: ActionIF - the chosen action.
            state: StateIF - a state object, if None then the current state is
                used.

        Returns:
            list[(StateIF, float, float)] - a list where each element is a
            tuple containing a possible next state, a possible reward and the
            corresponding probability.
        """

        pass

    @abc.abstractmethod
    def respond(self, action, state=None):
        """
        Returns a single next state and reward.

        This method takes a state and action and then according to its dynamics
        p(s',r|s,a), the FMDP returns a next state and reward.

        Params:
            action: ActionIF - the chosen action.
            state: StateIF - a state object, if None then the current state is
                used.

        Returns:
            [StateIF, float] - a list with the next state and reward.
        """

        pass

    @abc.abstractmethod
    def run(self, turns=None):
        """
        Runs the FMDP. 

        Params:
            turns: int - the number of turns to do for a continual FMDP.
        
        This method runs an episode of the FMDP or in the case of a continual
        FMDP, this method runs the FMDP for the specified number of turns. It
        saves the sequence of state, action and reward tuples as the FMDP runs.
        """

        pass

    @property
    @abc.abstractmethod
    def history(self):
        """
        Returns the history of the FMDP's states, actions and rewards for the
        latest run.

        Returns:
            [[StateIF, ActionIF, float], ...] - a list of tuples. Each tuple
            has three elements. The first element is the state, the second
            element is the action and the third element is the reward. The
            tuples are in order of the time they were encountered from earliest
            to latest.
        """

        pass


    # @abc.abstractmethod
    # def is_terminal(self):
        # """
        # Returns True if the current state is the terminal state.
        # """

        # pass

    # Scratch space
    # @property
    # @abc.abstractmethod
    # def env(self):
        # """
        # The FMDP's environment.

        # Returns:
            # EnvIF - the environemnt object.
        # """

        # oass

    # @abc.abstractmethod
    # def set_env(self, env):
        # """
        # Sets the environment.  

        # Params:
            # env: EnvIF - a environment object. 
        # """

        # pass

    # @abc.abstractmethod
    # def reset(self):
        # """
        # Resets the FMDP.

        # This method resets the FMDP by returning it to its initial state and
        # clears the FMDP's history.
        # """

        # pass

    # @abc.abstractmethod
    # def display(self):
        # """
        # Displays the FMDP as a printable string.
        # """

        # pass





    # # deprecated
    # @property
    # @abc.abstractmethod
    # def agents(self):
        # """
        # Returns a dictionary of the registered agents for the FMDP.
        # """

        # pass

# #    @abc.abstractmethod
# #    def do_action(self, action):
# #        """
# #        Updates the FMDP with the given action.
# #
# #        Params:
# #            action: ActionIF - the action to do.
# #        """
# #
# #        pass
# #
# #    @abc.abstractmethod
# #    def do_env(self):
# #        """
# #        Simulates the environment one step based the current state, choosen
# #        action and environment dynamics.
# #        """
# #
# #        pass
# #
    # @abc.abstractmethod
    # def step(self):
        # """
        # Performs a single step of the FMDP.
        # """

        # pass


class EnumFMDPIF(FMDPIF):
    """
    Defines an enumerable FMDP.

    An enumerable FMDP is a FMDP such that it is feasible to enumerate the
    entire state space.
    """

    @property
    @abc.abstractmethod
    def states(self):
        """
        Returns a list of all the possible states including the terminal state.
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
    def __eq__(self, other):
        pass


class ActionIF(abc.ABC):
    """
    Declares the methods that an action object implements.
    """

    @abc.abstractmethod
    def display(self):
        """
        Displays the action as a printable string.
        """

        pass

    @property
    @abc.abstractmethod
    def key(self):
        """
        Returns the key of the agent who selected the action.
        """

        pass


class AgentIF(abc.ABC):
    """
    Declares the methods that an agent object implements.
    """

    @property
    @abc.abstractmethod
    def name(self):
        """
        Returns the agent's name.

        Returns:
            ActionIF - the choosen action.
        """

        pass

    @property
    @abc.abstractmethod
    def key(self):
        """
        Returns the agent's key.
        """

        pass

    @abc.abstractmethod
    def set_key(self, key):
        """
        Sets the agent's key.

        Params:
            key: int - the agent's identifier for the FMDP.
        """

        pass

    @property
    @abc.abstractmethod
    def policy(self):
        """
        Returns the agent's policy.
        """

        pass

    @abc.abstractmethod
    def set_policy(self, policy):
        """
        Sets the agent's policy.
        
        Params:
            policy: PolicyIF - the policy to use.
        """
        
        pass

    @abc.abstractmethod
    def list_actions(self, state, fmdp):
        """
        Lists the possible actions with nonzero probability from a given state.

        Params:
            state: StateIF - a state object.
            fmdp: FMDPIF - the FMDP from which the state object is.

        Returns:
            list[(ActionIF, float)] - a list where each element is an action,
            probability pair for those actions with nonzero probability.
        """

        pass

    @abc.abstractmethod
    def select(self, state, fmdp):
        """
        Selects a possible action from a given state.

        Params:
            state: StateIF - a state object.
            fmdp: FMDPIF - the FMDP from which the state object is.

        Returns:
            ActionIF - the selected action.
        """

        pass


class PolicyIF(abc.ABC):
    """
    Declares the methods a policy object implements.

    A policy is a function that assigns a state to a conditional probability
    function over the possible actions from the state.
    """

    # @property
    # @abc.abstractmethod
    # def discount(self):
        # """
        # Returns the discount factor for the policy.

        # The discount factor is any real number between 0 and 1. For continual
        # FMDP that can possibly never terminate, the discount factor must be
        # strictly less than 1.
        # """
        
        # pass
    
    @abc.abstractmethod
    def list_actions(self, agent_key, state, fmdp):
        """
        Lists the possible actions with nonzero probability from a given state.

        Params:
            agent_key: int - the agent's key for the fmdp.
            state: StateIF - a state object.
            fmdp: FMDPIF - the FMDP from which the state object is.

        Returns:
            list[(ActionIF, float)] - a list where each element is an action,
            probability pair for those actions with nonzero probability.
        """

        pass


class DiscountPolicyIF(abc.ABC):
    """
    Declares the methods a discount policy object implements.

    A discount policy is a policy that utilizes a di
    function over the possible actions from the state.
    """

    # @property
    # @abc.abstractmethod
    # def discount(self):
        # """
        # Returns the discount factor for the policy.

        # The discount factor is any real number between 0 and 1. For continual
        # FMDP that can possibly never terminate, the discount factor must be
        # strictly less than 1.
        # """
        
        # pass
    
    @abc.abstractmethod
    def list_actions(self, agent_key, state, fmdp):
        """
        Lists the possible actions with nonzero probability from a given state.

        Params:
            agent_key: int - the agent's key for the fmdp.
            state: StateIF - a state object.
            fmdp: FMDPIF - the FMDP from which the state object is.

        Returns:
            list[(ActionIF, float)] - a list where each element is an action,
            probability pair for those actions with nonzero probability.
        """

        pass

class LookupPolicy(PolicyIF):
    """
    Defines a lookup policy.

    A lookup policy is a policy that uses a lookup table to determine the
    action to take from a state. The lookup up table is an exhaustive
    enumeration of all the possible states.
    """

    def __init__(self, state_actions, discount=1):
        """
        Initializes the lookup policy.

        Params:
            state_actions: list[StateIF, list[(ActionIF, float)] - a list where
                the first element is a state and the second element is a list
                of all the possible actions with nonzero probability.
        """

        self._state_actions = state_actions
        self._discount = discount

    @property
    def discount(self):
        return self._discount

    def list_actions(self, agent_key, state, fmdp):
        for state_action in self._state_actions:
            if state == state_action[0]:
                return state_action[1]
