from reinforce import base

class LookupPolicy(base.PolicyIF):
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


class RandomPolicy(base.PolicyIF):

    def __init__(self, discount=1, seed=None):
        self._discount = discount
        random.seed(seed) 

    @property
    def discount(self):
        return self._discount

    def list_actions(self, agent_key, state, fmdp):
        action_probs = []
        actions = fmdp.list_actions(state, agent_key)
        for action in actions:
            action_probs.append([action, 1 / len(actions)])

        return action_probs


class FuncEnvGreedyPolicy(base.PolicyIF):
    """
    Defines a function, environment based greedy policy.

    This class defines a greedy policy that has knowledge of its environment
    and that uses a function to estimate the value of a particular state.
    """

    def __init__(self, discount=1):
        self._discount = discount
        self._func = None
        self._fmdp = None

    @property
    def discount(self):
        return self._discount

    def list_actions(self, agent_key, state, fmdp):
        actions = fmdp.list_action(state, agent_key)
        for action in actions:



    def list_actions(self, state=None, agent_key=None):
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
