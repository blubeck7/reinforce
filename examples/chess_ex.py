"""
Chess Example

Implements chess as a FMDP. One of the players is designated as the agent.
"""


import chess
from reinforce import base


class ChessGame:

    def __init__(self):
        self._state = None
        self._agent = None
        self._agent_key = None
        self._comp = None
        self._comp_key = None
        self._history = None

    @property
    def agent(self):
        return self._agent, self._agent_key 

    def set_agent(self, agent, key):
        self._agent = agent
        self._agent_key = key

    @property
    def comp(self):
        return self._comp, self._comp_key 

    def set_comp(self, comp, key):
        self._comp = comp
        self._comp_key = key

    @property
    def state(self):
        return self._state

    def set_state(self, state):
        self._state = state

    def display(self):
        print(self.state)

    def list_actions(self, state=None, key=None):
        if not state:
            state = self.state

        if not key:
            key = self.agent[1]

        if (state.player != key or state.is_terminal() or state.is_over()):
            return [ChessAction(key, None, True)]

        actions = []
        import pdb
        pdb.set_trace()
        for move in self.state.list_moves():
            actions.append(ChessAction(key, move))

        return actions

    def respond(self, action, state=None):
        pass

    def run(self):
        pass
        # self._board = chess.Board()

        # print("{} is {} and {} is {}".format(
            # self.agent[0].name, self.agent[1],
            # self.comp[0].name, self.comp[1]))

        # self.history.append([ChessState(self._board.copy(False)), None, None])
        # while not self._board.is_game_over():
            # self.display()
            # action = self.agent[0].select(self.state, self)
            # action.display()
            # next_state, reward = self.respond(action, self.state)
            # self.set_state(next_state)
            # self.history.append([next_state, None, reward])
            # self.history[turn - 1][1] = action
        # turn = 0
        # self.history.append([self.state, None, None])
        # while not self.state.is_terminal():
            # turn += 1
            # self.state.display()
            # action = self.agent[1].select(self.state, self)
            # action.display()
            # next_state, reward = self.respond(action, self.state)
            # self.set_state(next_state)
            # self.history.append([next_state, None, reward])
            # self.history[turn - 1][1] = action

    def history(self):
        return self._history


class ChessState(chess.Board, base.StateIF):

    def __init__(self, terminal=False):
        self._terminal = terminal
        chess.Board.__init__(self)

    @property
    def player(self):
        if self.turn:
            return 1
        return -1

    def is_terminal(self):
        return self._terminal

    def is_over(self):
        return self.is_game_over()

    def list_moves(self):
        return self.legal_moves

    def display(self):
        print(self)

    def __eq__(self, other):
        if self.is_terminal() and other.is_terminal():
            return True

        if self.is_terminal() or other.is_terminal():
            return False

        return chess.Board.__eq__(self, other)

    def to_vec(self):
        pass


class ChessAction(chess.Move, base.ActionIF):

    def __init__(self, key, move, null=False):
        self._key = key
        self._null = null
        if move:
            fs = move.from_square
            ts = move.to_square
            p = move.promotion
            d = move.drop
            chess.Move.__init__(self, fs, ts, p, d)

    def display(self):
        pass

    @property
    def key(self):
        return self._key

    def is_null(self):
        return self._null
