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
    policy evaluation and policy improvement. Value iteration has high
    requirements though. It requires a FMDP that has an enumerable state space
    and a FMDP whose dynamics are explicitly known.

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


def mc_control(epsilon):
        """
        On-policy first-visit MC control.

        This function implement on-policy first visit Monte Carlo control to
        estimate the optimal episilon-greedy policy. See pg. 101 of
        Introduction to Reinforcement Learning by Barto and Sutton.

        Params:
            episilon: float - a real number strictly greater than 0, which
                determines how often the e-greedy policy takes the greedy
                action or takes another action at random.
        """
        # Note that under the optimal policy, v(s) = max_{a in A(s)} q(s,a)
        pass


def mc_pred(policy, fmdp, max_episodes=500):
    """
    First-visit Monte Carlo prediction.

    This function implements first-visit Monte Carlo prediction to estimate the
    state value function under a given policy. See pg. 92 of Introduction to
    Reinforcement Learning by Barto and Sutton.
    
    Params:
        policy: PolicyIF - the policy to evaluate.
        fmdp: FMDPIF - a FMDP.
        max_episodes: int - maximum number of episodes to do.
    """
    # state_returns: {StateIF: [float, float, float]} - the key is the state,
    # which must be hashable and for each state a list of the cumulative return
    # across all episodes, the num of episodes and the average is kept.

    fmdp.agent[0].set_policy(policy)
    state_returns = dict() 

    episode = 0
    while episode < max_episodes:
        episode += 1
        print(episode)
        fmdp.reset()
        fmdp.run()
        add_returns(fmdp.history, policy.discount, state_returns)

    return state_returns


def add_returns(history, discount, state_returns):
    cum_ret = 0
    for i in range(len(history) - 2, -1, -1): 
        state = history[i][0]
        reward = history[i + 1][2]
        cum_ret = cum_ret * discount + reward
        if _first_time(state, history, i): 
            if state in state_returns:
                stats = state_returns[state]
            else:
                state_returns[state] = [0, 0, 0]
                stats = state_returns[state]

            stats[0] = stats[0] + cum_ret
            stats[1] = stats[1] + 1
            stats[2] = stats[0] / stats[1]


def _first_time(state, history, i):
    """
    Returns true if this is the first time the state has occurred.

    Params:
        state: StateIF - the state to check.
        history: [[StateIF, ActionIF, float], ...] - a sequence of state,
            action, reward tuples.
    """

    return not any(map(lambda tup: tup[0] == state, history[:i-1]))


# def append_returns(episode_returns, state_returns):
    # for state, ret in episode_returns:
        # new = True
        # for state_return in state_returns:
            # if state == state_return[0]:
                # state_return[1].append(ret)
                # new = False
        # if new_state:
            # state_returns.append([state, [ret]])

    # return state_returns


# def average_returns(state_returns):
    # state_values = []
    # for state_return in state_returns:
        # ave = sum(state_return[1]) / len(state_return[1])
        # state_values.append([state_return[0], ave])

    # return state_values


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
