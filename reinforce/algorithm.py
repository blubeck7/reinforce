"""
Algorithm Module.

This module implements the algorithms described in the book Introduction to
Reinforcement Learning 2nd ed. by Barto and Sutton.  

Classes:
Functions:
Constants:
Exceptions:
"""


class DPSolver:
    """
    Defines dynamic programming algorithms to determine an optimal policy.

    This class implements the dynamic programming algorithms in the book
    Introduction to Reinforcement Learning 2nd ed to find an optimal policy for
    a given FMDP. A dynamic programming algorithm assumes that the dynamics of
    the FMDP are completely known, and it operates on the entire state space of
    the FMDP. Thus, these algorithms should be used only when it is feasible to
    enumerate FMDP's state space.
    """

    def __init__(self):
        """
        Initializes the enumerable dynamic programming solver object.
        """
        # The length of values is the number of states
        # The length of actions is the number of states
        self._values = [] 
        self._actions = [] 
        self._tol = 0.001

    def do_policy_iter(self, fmdp):
        """
        Determines the optimal policy using policy iteration.

        This function determines the optimal policy for an enumerbale FMDP
        using policy iteration.

        Params:
            fmdp: EnumFMDPIF - an enumerable FMDP object. 
        """

        self._init_policy(fmdp)
        stable = False
        while not stable:
            stable = self._do_policy_eval(fmdp)
            self._do_policy_impr(fmdp)

    def _init_policy(self, fmdp):
        for state in fmdp.states:
            self._values.append([state, 0])
            self._actions.append([state, fmdp.list_actions(state)[0]])

    def _do_policy_eval(self, fmdp):
        """
        Calculates the value of each state under the policy.
        """

        import pdb
        pdb.set_trace()
        n_iter = 0
        while True:
            delta = 0
            n_iter += 1
            for state_value, state_action in zip(self._values, self._actions):
                state = state_value[0]
                assert state == state_action[0]
                value = state_value[1]
                action = state_action[1]
                state_value[1] = self._calc_value(state, action, fmdp)
                delta = max(delta, abs(value - state_value[1]))
            if delta < self._tol:
                break

        if n_iter == 1:
            return True

        return False

    def _calc_value(self, state, action, fmdp):
        value = 0
        responses = fmdp.list_responses(state, action)
        import pdb
        pdb.set_trace()
        for next_state, reward, prob in responses:
            # TODO: Change 1 to a discount factor
            # TODO: Add logic for terminal state
            for s, v in self._values:
                if next_state == s:
                    break
            value += prob * (reward + 1 * v)

        return value

    def _do_policy_impr(self, fmdp):
        for state_action in self._actions:
            action = state_ction[1]
            state_action[0] = self._calc_action(state, fmdp)

        return stable

    def _calc_action(self, state, fmdp):
        actions = fmdp.list_actions(state)
        best_action = actions[0]
        best_value = self._calc_value(state, best_action, fmdp) 
        for action in actions[1:]:
            if self._calc_value(state, action, fmdp) > best_value:
                best_action = action

        return best_action

