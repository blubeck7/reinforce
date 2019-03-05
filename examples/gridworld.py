"""
Gridworld example.
"""


import random
from reinforce import base


class GridWorldFMDP(base.EnumFMDPIF):
    def __init__(self):
        self._states = []
        for row in range(4):
            for col in range(4):
                state = GridWorldState()
                state._row = row
                state._col = col
                state._size = 4
                state._end_sqs = [(0,0), (3,3)]
                if (row == 0 and col == 0) or (row == 3 and col == 3):
                    state._end = True
                self._states.append(state)
        state = GridWorldState()
        state._terminal = True
        self._states.append(state)

        self._actions = []
        action = GridWorldAction() 
        action._rowd = 1
        self._actions.append(action)
        action = GridWorldAction() 
        action._rowd = -1
        self._actions.append(action)
        action = GridWorldAction() 
        action._cold = 1
        self._actions.append(action)
        action = GridWorldAction() 
        action._cold = -1
        self._actions.append(action)
        action = GridWorldAction() 
        action._null = True
        self._actions.append(action)

    @property
    def state(self):
        return self._state

    def set_state(self, state):
        self._state = state

    @property
    def states(self):
        return self._states

    def list_responses(self, state, action):
        if state.is_terminal() or state._end:
            next_state = self._states[len(self._states) - 1]
            reward = 0
            prob = 1
            return [[next_state, reward, prob]]

        responses = []
        row = state._row + action._rowd
        col = state._col + action._cold
        if row < 0 or row > 3 or col < 0 or col > 3:
            return [[state, -1, 1]]
        
        for next_state in self._states:
            if next_state._row == row and next_state._col == col:
                return [[next_state, -1, 1]]

    def list_actions(self, state):
        # if the state is the terminal state return the null action else return
        # all four possible actions
        if state.is_terminal() or state._end:
            return [self._actions[len(self._actions) - 1]]

        return self._actions[:-1]


class GridWorldAction(base.ActionIF):
    def __init__(self):
        self._agent = None
        self._rowd = 0
        self._cold = 0
        self._null = False

    @property
    def agent(self):
        return self._agent

    def set_agent(self):
        self._agent = set_agent

    def display(self):
        if self.is_null():
            print("Null Action")
        elif self._rowd == 1:
            print("Down")
        elif self._rowd == -1:
            print("Up")
        elif self._cold == 1:
            print("Right")
        elif self._cold == -1:
            print("Left")

    def is_null(self):
        return self._null


class GridWorldState(base.StateIF):
    def __init__(self):
        self._row = 0 
        self._col = 0 
        self._size = 0
        self._end = False 
        self._end_sqs = []
        self._terminal = False

    def display(self):
        if self.is_terminal():
            print("Terminal State")
        else:
            self._display()

    def _display(self):
        print("  ", end="")
        for row in range(self._size - 1):
            print(str(row) + " ", end="")
        print(str(self._size - 1))

        for row in range(self._size):
            print(str(row) + " ", end="")
            for col in range(self._size):
                if (row, col) in self._end_sqs:
                    print("E", end="")
                elif row == self._row and col == self._col:
                    print("x", end="")
                else: 
                    print(" ", end="")

                if col != self._size - 1:
                    print(" ", end="")
                else:
                    print()

    def is_terminal(self):
        return self._terminal

    def __eq__(self, other):
        if self.__class__ != other.__class__:
            return False

        if self.is_terminal() and other.is_terminal():
            return True
        elif not self.is_terminal() and not other.is_terminal():
            cnt = 0
            if self._row == other._row:
                cnt += 1
            if self._col == other._col:
                cnt += 1
            if self._size == other._size:
                cnt += 1
            if self._end == other._end:
                cnt += 1
            if self._end_sqs == other._end_sqs:
                cnt += 1
            if cnt == 5:
                return True
        
        return False


class EqualProbPolicy(base.PolicyIF):
    def __init__(self, seed=None):
        self._discount = 1
        random.seed(seed) 

    @property
    def discount(self):
        return self._discount

    def set_discount(self, discount):
        self._discount = discount

    def list_actions(self, state, fmdp):
        action_probs = []
        actions = fmdp.list_actions(state)
        for action in actions:
            action_probs.append([action, 1 / len(actions)])

        return action_probs

