"""
Chess Example

Implements chess as a FMDP. One of the players is designated as the agent.
"""


import collections
import random
import chess
from reinforce import base


class ChessGame:

    def __init__(self):
        self._state = None
        self._agent = None
        self._agent_key = None
        self._comp = None
        self._comp_key = None
        self._history = []
        self._env_history = []

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

    def list_actions(self, key=None, state=None):
        if not key:
            key = self.agent[1]

        if not state:
            state = self.state

        if (state.player != key or state.is_terminal() or state.is_over()):
            return [ChessAction(key, None, True)]

        actions = []
        for move in state.list_moves():
            actions.append(ChessAction(key, move))

        return actions

    def respond(self, action, state=None):
        if not state:
            state = self.state

        if state.is_terminal():
            return [state, 0]

        if state.is_over():
            state._terminal = True
            return [state, state.winner * action.key]

        if state.player == action.key:
            state.push(action)
            return [state, 0]

        action = self.comp[0].select(state, self) 
        state.push(action)

        return [state, 0]

    def run(self):
        # Uses after states instead of states.
        # print("{} is {} and {} is {}".format(
            # self.agent[0].name, self.agent[1],
            # self.comp[0].name, self.comp[1]))

        state = self.state

        while not state.is_terminal():
            action = self.agent[0].select(state, self)
            state, reward = self.respond(action, state)
            if not action.is_null() or state.is_terminal():
                hist = ChessState(state.fen(), state.is_terminal())
                self.history.append([hist, action, reward])

    @property
    def history(self):
        return self._history

    def reset(self):
        self.history.clear()
        self._env_history.clear()
        self.set_state(ChessState())

    def save(self, filepath, num, append=True):
        """
        Saves the history to the file.

        Params:
            filepath: str - the full file path of where to save the history.
            num: int - episode number.
            append: bool - whether to append to the file or overwrite it.
        """

        mode = "a"
        if not append:
            mode = "w"

        with open(filepath, mode) as f:
            for state, action, reward in self.history:
                out_str = (str(num) + "," +
                    state.fen() + "," + str(state.is_terminal()) + "," +
                    str(action) + "," + str(reward)) + "\n"
                f.write(out_str)


class ChessState(chess.Board, base.StateIF):

    def __init__(self, fen=chess.STARTING_FEN, terminal=False):
        self._terminal = terminal
        chess.Board.__init__(self, fen)

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
        return list(self.legal_moves)

    @property
    def winner(self):
        result = self.result()

        if result == "1-0":
            return 1

        if result == "0-1":
            return -1

        return 0

    def display(self):
        if self.is_terminal():
            print("Terminal State")
        else:
            print(self)

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return False

        if self.is_terminal() and other.is_terminal():
            return True

        if self.is_terminal() or other.is_terminal():
            return False

        return chess.Board.__eq__(self, other)

    def to_vec(self):
        pass


class ChessAction(chess.Move, base.ActionIF):

    def __init__(self, key, move=None, null=False):
        self._key = key
        self._null = null

        if null:
            chess.Move.__init__(self, 0, 0)
        else:
            chess.Move.__init__(self, move.from_square, move.to_square,
                move.promotion, move.drop)

    def display(self):
        if self.is_null():
            print("Null Move")
        else:
            print(self)

    @property
    def key(self):
        return self._key

    def is_null(self):
        return self._null


class ChessAgent:

    def __init__(self, name):
        self._name = name
        self._key = None
        self._policy = None

    @property
    def name(self):
        return self._name

    @property
    def key(self):
        return self._key

    def set_key(self, key):
        self._key = key

    @property
    def policy(self):
        return self._policy

    def set_policy(self, policy):
        self._policy = policy

    def list_actions(self, state, fmdp):
        action_probs = self.policy.list_actions(self.key, state, fmdp)

        return action_probs

    def select(self, state, fmdp):
        action_probs = self.list_actions(state, fmdp)
        rand = random.random()
        cum_prob = 0
        for action, prob in action_probs:
            cum_prob += prob
            if rand < cum_prob:
                return action

        return action


class RandomPolicy:#base.PolicyIF

    def __init__(self, discount=1, seed=None):
        self._discount = discount
        random.seed(seed) 

    @property
    def discount(self):
        return self._discount

    def list_actions(self, key, state, fmdp):
        action_probs = []
        actions = fmdp.list_actions(key, state)
        for action in actions:
            action_probs.append([action, 1 / len(actions)])

        return action_probs


if __name__ == "__main__":
    fmdp = ChessGame()
    human = ChessAgent("Human")
    human.set_key(1)
    human.set_policy(RandomPolicy())
    comp = ChessAgent("Computer")
    comp.set_key(-1)
    comp.set_policy(RandomPolicy())
    fmdp.set_agent(human, 1)
    fmdp.set_comp(comp, -1)
    fmdp.reset()

    # s = ChessState(
    # "rnb1k1nr/pppp1ppp/8/2b1p3/4P3/3P3P/PPP1KqP1/RNBQ1BNR w kq - 0 5")
    # "r1bqkb1r/pppp1Qpp/2n2n2/4p3/2B1P3/8/PPPP1PPP/RNB1K1NR b KQkq - 0 4")
    # fmdp.set_state(s)

    fmdp.run()
    fmdp.save(r"/efs-dev/home/bmli/reinforce/data/games.csv", 1)
    # print(fmdp.history[len(fmdp.history)-1][0].winner)
    import pdb
    pdb.set_trace()
