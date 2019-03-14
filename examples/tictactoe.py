"""
Tic Tac Toe Module.

This module contains all of the tic tac toe specifc objects for reinforcement
learning.

Classes:
    TicTacToeGame - Implmentation of tic tac toe as a finite Markov decision
        process.
    TicTacToeState -
    TicTacToeAction - 

Functions:
Constants:
Exceptions:
"""


import itertools
import random
from reinforce import base 


XPIECE = "X"
OPIECE = "O"
WINNING_SQUARES = [
    (0,1,2), (3,4,5), (6,7,8),
    (0,3,6), (1,4,7), (2,5,8),
    (0,4,8), (2,4,6)] 
SQUARES = [0, 1, 2, 3, 4, 5, 6, 7, 8]  

NROWS = 3
NCOLS = 3
WIN = 1
TIE = 0
LOSS = -1


class TicTacToeAllFMDP(base.EnumFMDPIF):
    """
    This class implements the game tic tac toe as an enumerable FMDP with all
    the states for X's and O's and the corresponding game logic.
    """

    def __init__(self):
        """
        Initializes a new tic tac toe game.
        """
        # agent_key: int - 1 for x's and -1 for o's
        # agent: AgentIF - the main agent
        # comp_key: int - 1 for x's and -1 for o's, opposite of agent key
        # comp: AgentIF - the environment agent, opposite of agent
        # state: TicTacToeState - the current state

        self._agent_key = 0
        self._agent = None 
        self._comp_key = 0
        self._comp = None 

        self._states = gen_state_space(False)
        # add the terminal state as the last state
        self._states.append(TicTacToeState(True))
        self._state = self._states[0] 
        self._history = []
        self._step = 0

    @property
    def agent(self):
        return self._agent_key, self._agent

    def set_agent(self, key, agent):
        self._agent_key = key
        self._agent = agent

    @property
    def comp(self):
        return self._comp_key, self._comp

    def set_comp(self, key, comp):
        self._comp_key = key
        self._comp = comp 

    @property
    def states(self):
        return self._states 

    @property
    def state(self):
        return self._state

    def set_state(self, state):
        self._state = state

    def list_actions(self, state=None, agent_key=None):
        if not state:
            state = self.state

        if not agent_key:
            agent_key = self.agent[0]

        if (state.player != agent_key or state.is_terminal() or
            state.winner in (-1, 0, 1)):
            return [TicTacToeAction(agent_key, None, True)]

        actions = []
        for move in state.list_empty_squares():
            actions.append(TicTacToeAction(agent_key, move, False))

        return actions

    def list_responses(self, action, state=None):
        if not state:
            state = self.state

        if state.is_terminal():
            return [[state, 0, 1]]
        
        if state.winner in (-1, 0, 1):
            terminal_state = TicTacToeState.from_action(state, action, True)
            return [[terminal_state, state.winner * action.agent_key, 1]]

        if state.player == action.agent_key:
            next_state = TicTacToeState.from_action(state, action)
            return [[next_state, 0, 1]]

        responses = []
        for action_prob in self._comp.list_actions(state, self):
            next_state = TicTacToeState.from_action(state, action_prob[0])
            responses.append([next_state, 0, action_prob[1]])

        return responses 

    def respond(self, action, state=None):
        responses = self.list_responses(action, state)  
        rand = random.random()
        cum_prob = 0
        for n in range(len(responses)): 
            cum_prob += responses[n][2]
            if rand < cum_prob:
                return [responses[n][0], responses[n][1]]

        return [responses[n - 1][0], responses[n - 1][1]]


    def run(self):
        print("{} is {} and {} is {}".format(
            self.agent[1].name, self.agent[0],
            self.comp[1].name, self.comp[0]))

        turn = 0
        self.history.append([self.state, None, None])
        while not self.state.is_terminal():
            turn += 1
            self.state.display()
            action = self.agent[1].select(self.state, self)
            action.display()
            next_state, reward = self.respond(action, self.state)
            self.set_state(next_state)
            self.history.append([next_state, None, reward])
            self.history[turn - 1][1] = action


        # players = dict()
        # players[self.agent[0]] = self.agent[1]
        # players[self.comp[0]] = self.comp[1]
        # print("{} is X's and {} is O's".format(
            # players[1].name, players[-1].name))

        # turn = 0
        # self.history.append([self.state, None, None])
        # while not self.state.is_terminal():
            # turn += 1
            # self.state.display()
            # action = players[self.state.player].select(self.state, self)
            # action.display()
            # next_state, reward = self.respond(action, self.state)
            # self.set_state(next_state)
            # self.history.append([next_state, None, reward])
            # self.history[turn - 1][1] = action

    @property
    def history(self):
        return self._history


class TicTacToeState:#(base.EnumStateIF):
    """
    This class implements a state in the game tic tac toe.

    This class stores the information necessary to play tic tac toe. In
    addition, it defines some methods that calculate basic information about
    the game.
    """

    def __init__(self, terminal=False):
        """
        Initializes a tic tac toe state.

        Params:
            terminal: bool - if the terminal state

        Attrs:
            player: int - the player whose turn it is, 1 is X and -1 is O.
            board: list - a 3x3 array of -1, 0, 1. 
                1 is X, 0 is empty and -1 is O.
            row_tots: list - the row totals.
            col_tots: list - the columns totals.
            diag_tots: list - the diagonal totals.
            num_empty: int - number of empty spaces.
            full: bool - if the board is full or not.
            winner: int - 1 if X, -1 if O and 0 if a tie.
        """
        self.player = 1
        self.board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.row_tots = [0, 0, 0]
        self.col_tots = [0, 0, 0]
        self.diag_tots = [0, 0]
        self.num_empty = 9
        self.full = False
        self.winner = None
        self._terminal = terminal

    @classmethod
    def from_action(cls, state, action, terminal=False):
        """
        Returns a new state object from the given state and action.
        """
        if terminal:
            return cls(True)

        next_state = cls()
        next_state.copy_other(state)
        row = action._move[0]
        col = action._move[1]
        next_state.board[row][col] = action._agent_key
        next_state.calc_all_tots()
        next_state.calc_winner()
        next_state.flip_player()

        return next_state

    def __eq__(self, other):
        eq = False
        if isinstance(other, type(self)):
            cnt = 0
            if self.player == other.player:
                cnt += 1
            if self.board == other.board:
                cnt += 1
            if self.row_tots == other.row_tots:
                cnt += 1
            if self.col_tots == other.col_tots:
                cnt += 1
            if self.diag_tots == other.diag_tots:
                cnt += 1
            if self.num_empty == other.num_empty:
                cnt += 1
            if self.full == other.full:
                cnt += 1
            if self.winner == other.winner:
                cnt += 1
            if self._terminal == other._terminal:
                cnt += 1
            if cnt == 9:
                eq = True
        
        return eq

    def display(self):
        if self.is_terminal():
            print("Terminal State")
            return

        print("Board")
        print(" ", end="")
        for row in range(NROWS):
            print(" " + str(row), end="")
        print()

        for row in range(NROWS):
            print(row, end="")
            print(" ", end="")
            for col in range(NCOLS):
                if self.board[row][col] == 0:
                    print(" ", end="")
                elif self.board[row][col] == 1:
                    print(XPIECE, end="")
                else:
                    print(OPIECE, end="")
                if col != NCOLS - 1:
                    print("|", end="")
                else:
                    print()
            if row != NROWS - 1:
                print("  -----")

        if self.player == 1:
            print("{}'s turn to move".format(XPIECE))
        else:
            print("{}'s turn to move".format(OPIECE))

    def is_terminal(self):
        return self._terminal

    def calc_row_tots(self):
        """
        Calculates the row totals based on the current board.
        """
        for row in range(NROWS):
            tot = 0
            for col in range(NCOLS):
                tot += self.board[row][col]
            self.row_tots[row] = tot 

        return

    def calc_col_tots(self):
        """
        Calculates the column totals based on the current board.
        """
        for col in range(NCOLS):
            tot = 0
            for row in range(NROWS):
                tot += self.board[row][col]
            self.col_tots[col] = tot 

        return

    def calc_diag_tots(self):
        """
        Calculates the diagonal totals based on the current board.
        """
        tot = 0
        for row in range(NROWS):
            tot += self.board[row][row]
        self.diag_tots[0] = tot 

        tot = 0
        for row in range(NROWS):
            tot += self.board[NROWS - row - 1][row]
        self.diag_tots[1] = tot 

        return

    def calc_full(self):
        """
        Checks if the board is full.
        """
        n_empty = 0
        for row in range(NROWS):
            for col in range(NCOLS):
                if self.board[row][col] == 0:
                    n_empty += 1
        if n_empty == 0:
            self.full = True
        self.num_empty = n_empty

        return

    def copy_other(self, other):
        """
        Copies the information from another state object to this one.
        """
        self.player = other.player

        for row in range(NROWS):
            for col in range(NCOLS):
                self.board[row][col] = other.board[row][col]

        for row in range(NROWS):
            self.row_tots[row] = other.row_tots[row]

        for col in range(NCOLS):
            self.col_tots[col] = other.col_tots[col]

        for i in range(len(self.diag_tots)):
            self.diag_tots[i] = other.diag_tots[i]

        self.num_empty = other.num_empty
        self.full = other.full
        self.winner = other.winner
        self._terminal = self._terminal

        return

    def flip_player(self):
        """
        Changes the player from X to O and from O to X.
        """
        self.player = -1 * self.player

        return

    def add_piece(self, row, col):
        """
        Adds a player's piece to the board.
        """
        self.board[row][col] = self.player

        return

    def calc_all_tots(self):
        """
        Updates the row, col, diag totals and whether the board is full.
        """
        self.calc_row_tots()
        self.calc_col_tots()
        self.calc_diag_tots()
        self.calc_full()

        return

    def list_empty_squares(self):
        """
        Returns a list of the empty squares as row, col tuples.
        """
        squares = []
        for row in range(NROWS):
            for col in range(NCOLS):
                if self.board[row][col] == 0:
                    squares.append((row, col))

        return squares

    def calc_winner(self):
        """
        Calculates the winner.
        """
        for tot in self.row_tots:
            if tot == 3:
                self.winner = 1
                return
            elif tot == -3:
                self.winner = -1
                return

        for tot in self.col_tots:
            if tot == 3:
                self.winner = 1
                return
            elif tot == -3:
                self.winner = -1
                return

        for tot in self.diag_tots:
            if tot == 3:
                self.winner = 1
                return
            elif tot == -3:
                self.winner = -1
                return

        if self.full:
            self.winner = 0

        return


class TicTacToeAction:#(base.EnumActionIF):
    """
    This class defines an action in tic tac toe.
    """
    
    def __init__(self, agent_key=None, move=None, null=False):
        """
        Initializes a tic tac toe action.
        """
        # agent_key: int - 1 for x, -1 for o.
        # move: tuple - (row, col)
        # null: bool - if the null action, i.e. no action

        self._agent_key = agent_key
        self._move = move 
        self._null = null

    @property
    def agent_key(self):
        return self._agent_key

    def display(self):
        print("Move is: {}".format(self._move))

    def is_null(self):
        return self._null


def gen_state_space(sort_by_move=True):
    """
    Generates all the possible states in tic tac toe.

    Including the empty board, there are 5,478 board combinations, which can be
    proven using a combinatorial argument. This method generates all of the
    possible states and returns them as a list.

    Params:
        sort_by_move: bool - whether to sort the states by the number of moves.

    Returns:
        list - if the sort_by_move is true, then a list of length 10 is
        returned where each element is a list of the states after that many
        moves. If sort_by_move is false, then list of length 5,478 is returned.
    """

    states = []
    for moves in range(10):
        states_per_moves = _gen_state_space(moves)
        if sort_by_move:
            states.append(states_per_moves)
        else:
            states.extend(states_per_moves)

    return states


def _gen_state_space(moves):
    # handle zero moves as a special case
    if moves == 0:
        return [_create_state((), ())]

    all_states = _gen_all_states(moves)

    if moves % 2 == 0:
        illegal_states = _gen_x_winning_states(moves)
    else:
        illegal_states = _gen_o_winning_states(moves)
    legal_states = _remove_states(all_states, illegal_states)

    return legal_states


def _gen_all_states(moves):
    states = [] 
    num_x_sqs = moves // 2 + moves % 2
    num_o_sqs = moves // 2

    for x_sqs in itertools.combinations(set(SQUARES), num_x_sqs):
        rem_sqs = set(SQUARES) - set(x_sqs)
        for o_sqs in itertools.combinations(rem_sqs, num_o_sqs):
            state = _create_state(x_sqs, o_sqs)
            states.append(state)

    return states


def _gen_o_winning_states(moves):
    if moves < 6:
        return []

    states = []
    num_x_sqs = moves // 2 + moves % 2
    num_o_sqs = moves // 2
    num_rem_o_sqs = max(0, num_o_sqs - 3)

    for win_sqs in WINNING_SQUARES:
        rem_sqs = set(SQUARES) - set(win_sqs)
        for x_sqs in itertools.combinations(rem_sqs, num_x_sqs):
            o_rem_sqs = rem_sqs - set(x_sqs)
            for o_sqs in itertools.combinations(o_rem_sqs, num_rem_o_sqs):
                state = _create_state(x_sqs, o_sqs + win_sqs)
                states.append(state)

    return states


def _gen_x_winning_states(moves):
    if moves < 6:
        return []

    states = []
    num_x_sqs = moves // 2 + moves % 2
    num_o_sqs = moves // 2
    num_rem_x_sqs = max(0, num_x_sqs - 3)

    for win_sqs in WINNING_SQUARES:
        rem_sqs = set(SQUARES) - set(win_sqs)
        for o_sqs in itertools.combinations(rem_sqs, num_o_sqs):
            x_rem_sqs = rem_sqs - set(o_sqs)
            for x_sqs in itertools.combinations(x_rem_sqs, num_rem_x_sqs):
                state = _create_state(x_sqs + win_sqs, o_sqs)
                states.append(state)

    return states


def _remove_states(all_states, illegal_states):
    for illegal_state in illegal_states:
        # all_states is a list and the remove method uses the class's __eq__
        # method to test for equality
        all_states.remove(illegal_state) 
    
    return all_states


def _create_state(x_sqs, o_sqs):
    if not x_sqs and not o_sqs:
        return TicTacToeState()

    state = TicTacToeState()

    for x_sq in x_sqs:
        state.board[x_sq // NROWS][x_sq % NCOLS] = 1      
    for o_sq in o_sqs:
        state.board[o_sq // NROWS][o_sq % NCOLS] = -1      
    state.calc_all_tots()
    state.calc_winner()
    if state.num_empty % 2 == 1:
        state.player = 1
    else:
        state.player = -1

    return state


class TicTacToeAgent(base.AgentIF):

    def __init__(self, name):
        self._name = name
        self._agent_key = None
        self._policy = None
        self._act_env = None
        self._est_env = None

        return

    @property
    def name(self):
        return self._name

    @property
    def agent_key(self):
        return self._agent_key

    def set_agent_key(self, key):
        self._agent_key = key

    @property
    def policy(self):
        return self._policy

    def set_policy(self, policy):
        self._policy = policy

    def select(self, state, fmdp):
        action_probs = self.list_actions(state, fmdp)
        rand = random.random()
        cum_prob = 0
        for action, prob in action_probs:
            cum_prob += prob
            if rand < cum_prob:
                return action

        return action

    def list_actions(self, state, fmdp):
        action_probs = self._policy.list_actions(
            self.agent_key, state, fmdp)

        return action_probs


class RandomPolicy:#base.PolicyIF

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


if __name__ == "__main__":
    from reinforce import dp
    fmdp = TicTacToeAllFMDP()

    human = TicTacToeAgent("Human")
    human.set_agent_key(1)
    human.set_policy(RandomPolicy())

    comp = TicTacToeAgent("Computer")
    comp.set_agent_key(-1)
    comp.set_policy(RandomPolicy())

    fmdp.set_agent(1, human)
    fmdp.set_comp(-1, comp)
    opt_pol = dp.value_iter(fmdp, iters=100)

    import pdb
    pdb.set_trace()
    human.set_policy(opt_pol)

    fmdp.run()

    pdb.set_trace()
    #opt_pol = dp.value_iter(fmdp, iters=100)
    #agent = base.Agent("Human") 
    #agent.set_discount(1)
    #comp = base.Agent("Computer")
    #comp.set_discount(1)
    #fmdp = TicTacToeGame()
    #fmdp.set_agent(1, agent)
    #fmdp.set_comp(-1, comp)
    #fmdp.run()



