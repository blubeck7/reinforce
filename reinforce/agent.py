"""
Agent Module

This module declares the interface for an agent's policy function defined as
conditional probability of selecting a possible action given a particular
state. This module also defines two important policies that do not depend on
the type of agent. They are the random policy that assigns the same probability
to each action and the optimal policy, which selects the action that maximizes
the value of current state. Policies that depend on a concrete agent of FMDP
should be implemented in client-provided modules.

Classes:
    PolicyIF
    RandomPolicy
    OptimalPolicy

Functions:

Constants:

Exceptions:
"""


import abc
import random


class PolicyIF(abc.ABC):
    """
    Declares the methods that a policy object implements.

    A policy is a function that assigns a state to a conditional probability
    over the possible actions from that state.
    """

    @abc.abstractmethod
    def get_action(self, state, fmdp):
        """
        Selects an available action from the current state.

        Params:
            state: StateIF - the current state object.
            fmdp: FMDPIF - a FMDP that the current state comes from.

        Returns:
            ActionIF - the selected action.
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
    def fmdp(self):
        """
        Returns the FMDP that the agent is for.
        """
        
        pass

    @abc.abstractmethod
    def set_fmdp(self, fmdp):
        """
        Sets the FMDP that the agent is for.

        Params:
            fmdp: FMDPIF - the FMDP to use.
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
    def get_action(self, state):
        """
        Selects an action from the given state based on the agent's policy.

        Params:
            state: StateIF - the state from which to choose an action.

        Returns:
            ActionIF - the agent's selected action.
        """

        pass

    @abc.abstractmethod
    def run(self):
        """
        Runs the agent.

        This method starts the iterative sequence of the agent taking an action
        followed by the environment responding with a new state and reward.
        """

        pass


class RandomPolicy(PolicyIF):
    """
    Defines the random policy.

    This class defines the random policy. The random policy chooses each action
    with equal probability.
    """

    def __init__(self, seed=None):
        """
        Initializes the random policy.

        Params:
            seed: int - the seed to use for the random number generator.
        """

        self._seed = seed
        random.seed(seed) 

        return

    def get_action(self, state, fmdp):
        actions = fmdp.get_actions(state)

        return actions[random.randrange(len(actions))]


class OptimalPolicy(PolicyIF):
    """
    Defines the optimal policy.

    The optimal policy is selecting at each state the action that maximizes the
    expected value of the reward and the discounted value of the next state.
    """

    pass


class Agent(AgentIF):
    """
    Defines an agent.

    An agent is a thing capable of taking actions. It does so acccording to a
    policy. Two important policies that are independent of the actual FMDP are
    the random policy and the optimal policy.
    """

    def __init__(self, name):
        """
        Initializes the agent.

        Params:
            name: str - the name to use.
        """
        # fmdp: FMDPIF - the fmdp configured with the true environment.
        # policy: PolicyIF - the agent's policy.
        # act_env - the true environment's dynamics.
        # est_env - the agent's estimate of the environment's dynamics.

        self._name = name
        self._fmdp = None
        self._policy = None
        self._act_env = None
        self._est_env = None

        return

    @property
    def name(self):
        return self._name

    @property
    def fmdp(self):
        return self._fmdp

    def set_fmdp(self, fmdp):
        self._fmdp = fmdp

    @property
    def policy(self):
        return self._policy

    def set_policy(self, policy):
        self._policy = policy

    def get_action(self, state):
        return self._policy.get_action(state, self.fmdp)

    def run(self):
        while not self.fmdp.is_terminal():
            action = self.get_action(self.fmdp.state)
            self.fmdp.next(action)
