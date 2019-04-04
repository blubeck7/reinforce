"""
Chess Example

Implements chess as a FMDP. One of the players is designated as the agent.
"""


import collections
import random
import os
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
        self._board = fen.split()[0]

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

        return self._board == other._board
        #chess.Board.__eq__(self, other)

    def __hash__(self):
        if self.is_terminal():
            return hash("Terminal State")

        return hash(self._board)

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


def gen_state_values(policy, num):
    from reinforce import dp

    fmdp = ChessGame()
    human = ChessAgent("Human")
    human.set_key(1)
    comp = ChessAgent("Computer")
    comp.set_key(-1)
    comp.set_policy(RandomPolicy())
    fmdp.set_agent(human, 1)
    fmdp.set_comp(comp, -1)
    fmdp.reset()

    state_returns = dp.mc_pred(policy, fmdp, num)

    return state_returns 


def save_state_values(state_values, filepath, append=True):
    """
    Saves the state values to a file.

    Params:
        state_values: dict - a dictionary in the form {state: [cum_ret,
        num_episodes, average], ...} with the raw state values to save.
        filepath: str - the full file path of where to save the state values.
        append: bool - whether to append to the file or overwrite it.
    """

    mode = "a"
    if not append:
        mode = "w"

    with open(filepath, mode) as f:
        for state, stats in state_values.items():
            cum_ret = stats[0]
            n = stats[1]
            ave = stats[2]
            if isinstance(state, str):
                out_str = (state + "," + str(cum_ret) + "," +
                    str(n) + "," + str(ave)) + "\n"
            else:
                out_str = (str(state.fen()) + "," + str(cum_ret) + "," +
                    str(n) + "," + str(ave)) + "\n"
            f.write(out_str)
        f.flush()


def load_state_values(filepath):
    state_values = dict()
    with open(filepath, "r") as f:
        for line in f:
            line = line[:len(line) - 1] # removes the '\n' at the end
            state, tot, cnt, ave = line.split(",")
            state_values[state] = [0, 0, 0] 
            state_values[state][0] = int(tot)
            state_values[state][1] = int(cnt)
            state_values[state][2] = float(ave)

    return state_values


def estimate(filepath, policy, num):
    print(multiprocessing.current_process().name)
    state_values = gen_state_values(policy, num)
    save_state_values(state_values, filepath)


def combine(in_dir, out_dir, out_file):
    """
    Combines the state value data into one file.
    """
    state_values = dict()

    # merge the separate files into one dictionary
    for in_file in os.listdir(in_dir):
        print("Merging {}".format(in_file))
        with open(os.path.join(in_dir, in_file), "r") as f:
            for line in f:
                line = line[:len(line) - 1]
                state, tot, cnt, ave = line.split(",")
                tot = int(tot)
                cnt = int(cnt)
                state = state.split()[0]
                if state in state_values:
                    cur_tot = state_values[state][0]
                    new_tot = cur_tot + tot
                    state_values[state][0] = new_tot 
                    cur_cnt = state_values[state][1]
                    new_cnt = cur_cnt + cnt
                    state_values[state][1] = new_cnt 
                    state_values[state][2] = new_tot / new_cnt
                else:
                    state_values[state] = [0, 0, 0] 
                    state_values[state][0] = tot 
                    state_values[state][1] = cnt 
                    state_values[state][2] = tot / cnt 

    # output as one file
    save_state_values(state_values, os.path.join(out_dir, out_file))


if __name__ == "__main__":
    # import multiprocessing

    # filepath = "/efs-dev/home/bmli/reinforce/data/state_values{}.csv"
    # policy = RandomPolicy()
    # num = 20000 

    # jobs = []
    # for i in range(16):
        # job = multiprocessing.Process(
            # target=estimate, args=(filepath.format(i), policy, num))
        # jobs.append(job)
        # job.start()

    dirpath = "/efs-dev/home/bmli/reinforce/data/"
    combine(dirpath, dirpath, "state_values_all.csv")
