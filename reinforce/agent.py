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
import uuid


class PolicyIF(abc.ABC):
    """
    Declares the methods that a policy object implements.
    """

    @property
    @abc.abstractmethod
    def fmdp(self):
        """
        Returns the FMDP that the policy is for.
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
    def uid(self):
        """
        Returns the agent's unique id.
        """

        pass

    @property
    def fmdp(self):
        """
        Returns the FMDP that the agent is for.
        """
        
        return self._fmdp

    @property
    @abc.abstractmethod
    def name(self):
        """
        Returns the agent's name.

        Returns:
            ActionIF - the choosen action.
        """

        pass

    @abc.abstractmethod
    def set_name(self, name):
        """
        Sets the agent's name.

        Params:
            name: str - the name to use.
        """

        pass

    @property
    @abc.abstractmethod
    def policy(self):
        """
        Returns the agent's policy.
        """

        pass

#    @abc.abstractmethod
#    def set_policy(self, policy):
#        """
#        Sets the agent's policy.
#
#        Params:
#            policy: PolicyIF - the policy to use.
#        """
#
#        pass


class RandomPolicy(PolicyIF):
    """
    Defines the random policy.

    This class defines the random policy. The random policy chooses each action
    with equal probability.
    """

    def __init__(self, fmdp):
        """
        Initializes the random policy.

        Params:
            fmdp: FMDPIF - the fmdp process to use.
        """

        self._fmdp = fmdp

        return

    @property
    def fmdp(self):
        
        return self._fmdp

    def choose_action(self):
        actions = self._fmdp.actions()

        return actions[random.randrange(len(actions))]


class RandomAgent(AgentIF):
    """
    Defines a random agent.

    A random agent is an agent that follows the random policy.
    """

    def __init__(self, name, fmdp):
        """
        Initializes a random agent.

        Params:
            name: str - the name to use.
            fmdp: FMDPIF - the FMDP that the random agent is for.
        """

        self._uid = uuid.uuid1().int
        self._fmdp = fmdp
        self._name = name
        self._policy = RandomPolicy(fmdp)

        return

    @property
    def uid(self):

        return self._uid

    @property
    def fmdp(self):

        return self._fmdp

    @property
    def name(self):

        return self._name

    @property
    def policy(self):

        return self._policy

    def set_name(self, name):
        self._name = name

        return
