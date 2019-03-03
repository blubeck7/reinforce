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
from reinforce import fmdp


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


class TicTacToeGame(fmdp.FMDPIF):
    """
    This class implements the game tic tac toe as a FMDP.
    """

    def __init__(self):
        """
        Initializes a new tic tac toe game.
        """
        # agents: dict - the agents or players for the game.
        # init_state: StateIF - the starting board for the game.
        # state: StateIF - the current board for the game.
        # history: list - a list that records the sequence of state, action,
        #    and reward tuples.
        # step: int - the current step.

        #self._agents = {XAGENT: None, OAGENT: None} 
        self._env = TicTacToeEnv()
        self._init_state = TicTacToeState(
            XAGENT, [[EMPTY]*3, [EMPTY]*3, [EMPTY]*3])
        self._state = self._init_state
        self._history = []
        self._step = 0

        return

    @property
    def state(self):
        return self._state

    def set_state(self, state):
        self._state = state

    def is_terminal(self):
        return self.state.is_terminal()

    def get_actions(self, state=None):
        if state:
            return self._get_actions(state)

        return self._get_actions(self._state)

    def _get_actions(self, state):
        # TODO: Move this logic to TicTacToeEnv since that object is the object
        # that knows the rules.
        actions = [] 
        for row in range(NROWS):
            for col in range(NCOLS):
                if state._board[row][col] == 0:
                    action = TicTacToeAction(state.agent_key, row, col)
                    actions.append(action)

        return actions

    def next(self, action):
        next_state, reward = self.env.next(self.state, action)
        self._history.append((self.state, action, reward))
        self.set_state(next_state)

    @property
    def env(self):
        return self._env

    def set_env(self, env):
        self._env = env

    # deprecated
    @property
    def agents(self):
        return self._agents

    def set_agent(self, key, agent):
        self._agents[key] = agent

    def display(self):
        print("Game Step: {}".format(self._step))
        self._state.display()

        return

    def step(self):
        pass
    
    def reset(self):
        pass

    @property
    def history(self):
        pass

    def run(self):
        # for each agent in order do:
        #    get the agent's action
        #    do the environment
        #    update the state and reward
        #    record current state, action, next state and reward
        # do environment

        self.display()
        agent = self.agents[self.state.agent_key]
        action = agent.get_action(self.state)

        return action


class TicTacToeEnv(fmdp.EnvIF):
    """
    Implements an environment for tic tac toe.

    The environemnt is the object that knows the rules of tic tac toe.
    """

    def __init__(self):
        self._other_agents = None

        return

    def next(self, state, action):
        assert state.agent_key == action.agent_key

        if state.is_terminal():
            return state, 0

        import pdb
        pdb.set_trace()
        winner = self._is_game_over(state)
        if winner is not None:
            if winner == stage.agent_key:
                return fmdp.TerminalState(state.agent_key), WIN
            elif winner == TIE:
                return fmdp.TerminalState(state.agent_key), TIE
            else:
                return fmdp.TerminalState(state.agent_key), LOSS

        next_state = state.copy()
        next_state.update(action)

        #next_state, reward = self.env.next(self.state, action)
        #TicTacToeState()
        #if state.agent

        return

    def _is_game_over(self, state):
        """
        Checks if the game is over and returns the winner.
        """
        for row in range(NROWS):
            tot = 0
            for col in range(NCOLS):
                tot += state[(row, col)]
            if tot == XAGENTW:
                return XAGENT
            elif tot == OAGENTW:
                return OAGENT

        for col in range(NCOLS):
            tot = 0
            for row in range(NROWS):
                tot += state[(row, col)]
            if tot == XAGENTW:
                return XAGENT
            elif tot == OAGENTW:
                return OAGENT

        tot = 0
        for row in range(NROWS):
            tot += state[(row, row)]
        if tot == XAGENTW:
            return XAGENT
        elif tot == OAGENTW:
            return OAGENT
        
        tot = 0
        for row in range(NROWS):
            tot += state[(row, NROWS - row - 1)]
        if tot == XAGENTW:
            return XAGENT
        elif tot == OAGENTW:
            return OAGENT

        tot = 0
        for row in range(NROWS):
            for col in range(NCOLS):
                if state[(row, col)] != EMPTY:
                    tot += 1

        if tot == 9:
            return TIE
           

class TicTacToeState(fmdp.StateIF):
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


class TicTacToeAction(fmdp.ActionIF):
    """
    This class defines an action in tic tac toe.
    """
    
    def __init__(self, agent_key, row, col):
        """
        Initializes a tic tac toe action.

        Params:
            agent_key: int|str - the key of the agent who chose the action.
            row: int - row number
            col: int - column number
        """

        self._agent_key = agent_key
        self._row = row
        self._col = col

    @property
    def agent_key(self):
        return self._agent_key

    @property
    def row(self):
        return self._row

    @property
    def col(self):
        return self._col

    def display(self):
        print("row: {} col: {}".format(self._row, self._col))

    def is_null(self):
        return False


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
    if moves // 2 == 0:
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
