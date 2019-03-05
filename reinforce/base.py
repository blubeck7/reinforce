#TODO: For now keep all the abstract reinforcement learning code in this file.
#TODO: May break it out into multiple files later.
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


class FMDPIF(abc.ABC):
    """
    Declares the methods a finite Markov decision process (FMDP) implements.
    """

    # @property
    # @abc.abstractmethod
    # def agent(self):
        # """
        # The agent configured for the FMDP.

        # Returns:
            # AgentIF - the agent configured for the FMDP.
        # """


    # Scratch space
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

    # @abc.abstractmethod
    # def is_terminal(self):
        # """
        # Returns True if the current state is the terminal state.
        # """

        # pass

    # @abc.abstractmethod
    # def get_actions(self, state=None):
        # """
        # Returns a list of the possible actions for a given state. 

        # Params:
            # state: StateIF - a state object. If None, then a list of the
                # actions for the current state is returned.

        # Returns:
            # list[ActionIF] - a list of the possible actions.
            
        # """

        # pass

    # @abc.abstractmethod
    # def next(self, action):
        # """
        # Updates the FMDP.

        # This method transitions the FMDP to a new state and gives a reward
        # based on the environment's dynamics.

        # Params:
            # action: ActionIF - the chosen action.
        # """

        # pass

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

    # @property
    # @abc.abstractmethod
    # def history(self):
        # """
        # Returns the history of the FMDP's states, actions and rewards.

        # Returns:
            # list - a list of tuples. Each tuple has three elements. The first
                # element is the state, the second element is the action and the
                # third element is the reward. The tuples are in order of the
                # time they were encountered from earliest to latest.
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

    # @abc.abstractmethod
    # def run(self):
        # """
        # Runs the FMDP according to its specific environment and rules.
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

    @abc.abstractmethod
    def list_responses(self, state, action):
        """
        Lists the possible responses for an action from a given state.

        Returns:
            list - a list where each element is a list containing a possible
            next state, a possible reward and the corresponding probability.
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

    @abc.abstractmethod
    def __eq__(self, other):
        pass


class ActionIF(abc.ABC):
    """
    Declares the methods that an action object implements.
    """
    pass

    @property
    @abc.abstractmethod
    def agent(self):
        """
        Returns the agent who chose the action.
        """

        pass

    # @abc.abstractmethod
    # def display(self):
        # """
        # Displays the action as a printable string.
        # """

        # pass

    # @abc.abstractmethod
    # def is_null(self):
        # """
        # Returns true if the null action.
        # """

        # pass


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
#

    # scratch space
    #@property
    #@abc.abstractmethod
    #def fmdp(self):
        #"""
        #Returns the FMDP that the agent is for.
        #"""
        #
        #pass
#
    #@abc.abstractmethod
    #def set_fmdp(self, fmdp):
        #"""
        #Sets the FMDP that the agent is for.
#
        #Params:
            #fmdp: FMDPIF - the FMDP to use.
        #"""
        #
        #pass
#

    #@abc.abstractmethod
    #def get_action(self, state):
        #"""
        #Selects an action from the given state based on the agent's policy.
#
        #Params:
            #state: StateIF - the state from which to choose an action.
#
        #Returns:
            #ActionIF - the agent's selected action.
        #"""
#
        #pass
#
    #@abc.abstractmethod
    #def run(self):
        #"""
        #Runs the agent.
#
        #This method starts the iterative sequence of the agent taking an action
        #followed by the environment responding with a new state and reward.
        #"""
#
        #pass


class Agent(AgentIF):
    """
    Defines an agent.

    An agent is a thing capable of taking actions. It does so acccording to a
    policy. Three important policies independent of the actual FMDP are the
    random policy, the greedy policy and the optimal policy.
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


class PolicyIF(abc.ABC):
    """
    Declares the methods a policy object implements.

    A policy is a function that assigns a state to a conditional probability
    function over the possible actions from the state.
    """

    @abc.abstractmethod
    def list_actions(self, state, fmdp):
        """
        Lists the possible actions from a given state with nonzero probability.

        Params:
            state: StateIF - a state object.
            fmdp: FMDPIF - the FMDP from which the state object is.

        Returns:
            list[list[ActionIF, float]] - a list where each element is a list
            containing an action and its corresponding nonzero probability.
        """

        pass

    @property
    @abc.abstractmethod
    def discount(self):
        """
        Returns the policy's discount factor.
        """
        
        pass
    
    @abc.abstractmethod
    def set_discount(self):
        """
        Sets the policy's discount factor.
        """

        pass


class GreedyPolicy(PolicyIF):
    """
    Sets the greedy policy.

    The greedy policy is the policy that selects the action that maximizes
    the expected value of the sum of the next reward and the value of the
    next state based on an existing policy.
    """

    def __init__(self, policy, discount=1):
        """
        Initializes the greedy policy.

        Params:
            policy: PolicyIF - an existing policy.
            discount: float - the discount factor to use. For episodic tasks,
                the discount factor can be 1. For indefinite tasks, the
                discount factor must be strictly less than 1.
        """
            
        self._discount = discount
        self._policy = policy

    @property
    def discount(self):
        return self._discount

    def set_discount(self, discount):
        self._discount = discount

    def select_action(self, state, fmdp):
        values = []
        actions = fmdp.list_actions(state)
        for action in actions:
            responses = fmdp.list_responses(action)
            for response in responses:
                next_state, reward, prob = response
                value = prob*(reward + self.discount)
                #values.append(
                


class LookupPolicy:#(refmdp.PolicyIF):
    """
    Defines a lookup policy.

    A lookup policy is a policy that uses a lookup table to determine the
    action to take from a state. The lookup up table is an exhaustive
    enumeration of all the possible states.
    """

    def __init__(self):
        self._state_action_map = dict()
        return

    def select_action(self, state, fmdp):
        pass


