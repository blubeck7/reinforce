# TODO: Update documentation to be Algortihm or Learning Module
"""
Dynamic Programming Module.

This module implements the dynamic programming algorithms described in the book
Introduction to Reinforcement Learning 2nd ed. by Barto and Sutton.  

Classes:
Functions:
Constants:
Exceptions:
"""


_DEBUG = True


from reinforce import base


def value_iter(fmdp, discount=1, delta=10**-6, iters=500):
    """
    Finds an optimal policy for the FMDP using value iteration.

    This function uses value iteration to find the optimal policy for an
    enumerable FMDP. Value iteration combines in one loop over the state space,
    policy evaluation and policy improvement.

    Params:
        fmdp: EnumFMDPIF - an enumerable FMDP.
        discout: float - a number between 0 and 1 used to discount the future
            rewards.
        delta: float - this number determines when the algorithm is considered
            to have converged. The algorithm stops after a sweep of the state
            space if the maximum absolute value change is less than delta.
        iters: int - maximum number of iterations.
    """
    state_value_pairs = []
    for state in fmdp.states:
        state_value_pairs.append([state, 0])

    n = 0
    while True:
        diff = 0
        n += 1
        print(n)
        for state_value_pair in state_value_pairs:
            cur_state_value = state_value_pair[1]
            _, state_value_pair[1] = calc_best_action(
                state_value_pair[0], state_value_pairs, discount, fmdp)
            diff = max(diff, abs(cur_state_value - state_value_pair[1]))

        if diff < delta or n > iters:
            break

    state_actions = [] 
    for state in fmdp.states:
        state_action = [None, None]
        state_action[0] = state
        action, _ = calc_best_action(state, state_value_pairs, discount, fmdp)
        state_action[1] = [(action, 1)] 
        state_actions.append(state_action)

    return base.LookupPolicy(state_actions, discount) 


def calc_best_action(state, state_value_pairs, discount, fmdp):
    """
    Calculates the greedy action from a state.

    This function calculates the greedy action from a given state. 
    """

    actions = fmdp.list_actions(state)
    best_action = actions[0]
    best_value = calc_action_value(
        state, best_action, state_value_pairs, discount, fmdp) 
    for action in actions[1:]:
        value = calc_action_value(
            state, action, state_value_pairs, discount, fmdp)
        if value > best_value:
            best_action = action
            best_value = value

    return best_action, best_value


def calc_action_value(state, action, state_value_pairs, discount, fmdp):
    """
    Calculates the one-step ahead value of an action from a given state.
    """

    new_value = 0 
    responses = fmdp.list_responses(action, state)
    for next_state, reward, prob in responses:
        value = lookup_state_value(next_state, state_value_pairs) 
        new_value += prob * (reward + discount * value)

    return new_value


def lookup_state_value(state, state_value_pairs):
    for state_value in state_value_pairs:
        if state == state_value[0]:
            return state_value[1]


def eval_policy_mc(policy, fmdp, max_episodes=500):
    """
    Evaluates a policy for a FMDP using first-visit Monte Carlo prediction.
    
    Params:
        policy: PolicyIF - the policy to evaluate.
        fmdp: FMDPIF - a FMDP.
        max_episodes: int - maximum number of episodes to do.
    """

    pass
# def eval_policy(policy, fmdp, delta=10**-6, iters=500):
    # """
    # Evaluates a policy using iterative policy evaluation.

    # This function evaluates a policy using iterative policy evaluation. Like
    # other dynamic programming algorithms, it assumes that the FMDP's state
    # space is enumerable and that the FMDP's dynamics are known. 

    # Params:
        # policy: PolicyIF - the policy to evaluate.
        # fmdp: EnumFMDPIF - an enumerable FMDP.
        # delta: float - this number determines when the algorithm is considered
            # to have converged. The algorithm stops after a sweep of the state
            # space if the maximum absolute value change is less than delta.

    # Returns:
        # list - a list of lists where each element is a state, value pair.
    # """
    # state_values = []
    # for state in fmdp.states:
        # state_values.append([state, 0])

    # n = 0
    # while True:
        # diff = 0
        # n += 1
        # for state_value in state_values:
            # value = state_value[1]
            # state_value[1] = update_state_value(state_value[0], policy, fmdp,
                                                # state_values)
            # diff = max(diff, abs(value - state_value[1]))

        # if diff < delta or n > iters:
            # break

    # return state_values


# def update_state_value(state, policy, fmdp, state_values):
    # new_value = 0
    # action_probs = policy.list_actions(state, fmdp)
    # for action, aprob in action_probs:
        # responses = fmdp.list_responses(state, action)
        # for next_state, reward, prob in responses:
            # value = lookup_state_value(next_state, state_values) 
            # new_value += aprob * prob * (reward + policy.discount * value)

    # return new_value


# def print_state_values(state_values):
    # for n, state_value in enumerate(state_values):
        # print(n, state_value[1])
    

# def impr_policy(state_values, policy, fmdp):
    # """
    # Constructs a one-step ahead greedy policy based on the state values.

    # This function constructs a one-step ahead greedy policy based on the
    # state values for the policy. Note that there may be more than one action
    # that is optimal from a given state.
    # """
    
    # state_actions = []
    # for state_value in state_values:
        # state_action = [None, None]   
        # state_action[0] = state_value[0]
        # state_action[1] = calc_best_action(
            # state_action[0], state_values, policy.discount, fmdp)
        # state_actions.append(state_action)

    # return base.LookupPolicy(state_actions, policy.discount) 
        

# def iter_policy(self, fmdp):
    # """
    # Determines the optimal policy using policy iteration.

    # This function determines the optimal policy for an enumerbale FMDP
    # using policy iteration.

    # Params:
        # fmdp: EnumFMDPIF - an enumerable FMDP object. 
    # """

    # # Note that a state always has at least one action, the null action 
    # state_values = []
    # state_actions = []
    # for state in fmdp.states:
        # state_values.append([state, 0])
        # state_actions.append([state, fmdp.list_actions(state)[0]])

    # # There can be two or more optimal policies because two or more different
    # stable = False
    # while not stable:
        # stable = self._do_policy_eval(fmdp)
        # self._do_policy_impr(fmdp)









# class DPSolver:
    # """
    # Defines dynamic programming algorithms to determine an optimal policy.

    # This class implements the dynamic programming algorithms in the book
    # Introduction to Reinforcement Learning 2nd ed to find an optimal policy for
    # a given FMDP. A dynamic programming algorithm assumes that the dynamics of
    # the FMDP are completely known, and it operates on the entire state space of
    # the FMDP. Thus, these algorithms should be used only when it is feasible to
    # enumerate FMDP's state space.
    # """

    # def __init__(self):
        # """
        # Initializes the enumerable dynamic programming solver object.
        # """
        # # The length of values is the number of states
        # # The length of actions is the number of states
        # self._values = [] 
        # self._actions = [] 
        # self._tol = 0.001

    # def do_policy_iter(self, fmdp):
        # """
        # Determines the optimal policy using policy iteration.

        # This function determines the optimal policy for an enumerbale FMDP
        # using policy iteration.

        # Params:
            # fmdp: EnumFMDPIF - an enumerable FMDP object. 
        # """

        # self._init_policy(fmdp)
        # stable = False
        # while not stable:
            # stable = self._do_policy_eval(fmdp)
            # self._do_policy_impr(fmdp)

    # def _init_policy(self, fmdp):
        # for state in fmdp.states:
            # self._values.append([state, 0])
            # self._actions.append([state, fmdp.list_actions(state)[0]])

    # def _do_policy_eval(self, fmdp):
        # """
        # Calculates the value of each state under the policy.
        # """

        # import pdb
        # pdb.set_trace()
        # n_iter = 0
        # while True:
            # delta = 0
            # n_iter += 1
            # for state_value, state_action in zip(self._values, self._actions):
                # state = state_value[0]
                # assert state == state_action[0]
                # value = state_value[1]
                # action = state_action[1]
                # state_value[1] = self._calc_value(state, action, fmdp)
                # delta = max(delta, abs(value - state_value[1]))
            # if delta < self._tol:
                # break

        # if n_iter == 1:
            # return True

        # return False

    # def _calc_value(self, state, action, fmdp):
        # value = 0
        # responses = fmdp.list_responses(state, action)
        # import pdb
        # pdb.set_trace()
        # for next_state, reward, prob in responses:
            # # TODO: Change 1 to a discount factor
            # # TODO: Add logic for terminal state
            # for s, v in self._values:
                # if next_state == s:
                    # break
            # value += prob * (reward + 1 * v)

        # return value

    # def _do_policy_impr(self, fmdp):
        # for state_action in self._actions:
            # action = state_ction[1]
            # state_action[0] = self._calc_action(state, fmdp)

        # return stable

    # def _calc_action(self, state, fmdp):
        # actions = fmdp.list_actions(state)
        # best_action = actions[0]
        # best_value = self._calc_value(state, best_action, fmdp) 
        # for action in actions[1:]:
            # if self._calc_value(state, action, fmdp) > best_value:
                # best_action = action

        # return best_action

