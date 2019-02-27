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

    @property
    @abc.abstractmethod
    def fmdp(self):
        """
        Returns the FMDP that the policy is for.
        """

        pass

    @abc.abstractmethod
    def set_fmdp(self, fmdp):
        """
        Sets the FMDP that the policy is for.

        Params:
            fmdp: FMDPIF - the FMDP to use.
        """
        
        pass

    @abc.abstractmethod
    def choose_action(self):
        """
        Chooses an available action from the current state.

        Returns:
            ActionIF - the choosen action.
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
    def choose_action(self, state):
        """
        Chooses an action from the given state based on the agent's policy.

        Params:
            state: StateIF - the state from which to choose an action.
        """

        pass


class RandomPolicy(PolicyIF):
    """
    Defines the random policy.

    This class defines the random policy. The random policy chooses each action
    with equal probability.
    """

    def __init__(self):
        """
        Initializes the random policy.
        """

        self._fmdp = None

        return

    @property
    def fmdp(self):
        return self._fmdp

    def set_fmdp(self, fmdp):
        self._fmdp = fmdp

    def choose_action(self):
        actions = self._fmdp.actions()

        return actions[random.randrange(len(actions))]


class Agent(AgentIF):
    """
    Defines an agent.

    An agent is a thing capable of taking actions. It does so acccording to a
    policy. Two important policies that are independent of the actual FMDP are
    the random policy and the optimal policy.
    """

    def __init__(self, name, fmdp=None):
        """
        Initializes the agent.

        Params:
            name: str - the name to use.
        """

        self._name = name
        self._fmdp = fmdp
        self._policy = None

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
