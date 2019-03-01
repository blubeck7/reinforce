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


from reinforce import fmdp


XPIECE = "X"
OPIECE = "O"

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
        self.player = None
        self.board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.row_tots = [0, 0, 0]
        self.col_tots = [0, 0, 0]
        self.diag_tots = [0, 0]
        self.num_empty = 9
        self.full = False
        self.winner = None
        self._terminal = terminal

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

        self.full = other.full
        self.winner = other.winner

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

    def _to_std_board(self):
        # for generating the state space
        for row in range(NROWS):
            for col in range(NCOLS):
                if self._board[row][col] in [1, 2, 3, 4, 5]:
                    self.board[row][col] = 1
                elif self._board[row][col] in [6, 7, 8, 9]:
                    self.board[row][col] = -1

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


def gen_state_space():
    states = []
    init_state = TicTacToeState()
    init_state.player = 1

    return _gen_state_space(init_state, states)


def _gen_state_space(state, states):
    states.append(state) 
    next_states = _get_next_states(state)
    for next_state in next_states:
        _gen_state_space(next_state, states)

    return states


def _get_next_states(state):
    if not state.winner is None:
        return []

    next_states = []

    if state.player == 1:
        moves = _get_x_moves(state)
    else:
        moves = _get_o_moves(state)

    for move in moves:
        next_state = TicTacToeState()
        next_state.copy_other(state) 
        next_state.add_piece(*move)
        next_state.calc_all_tots()
        next_state.calc_winner()
        next_state.flip_player()
        next_states.append(next_state)
    
    return next_states
        

def _get_x_moves(state):
    # Find right most x if the board were unraveled.
    moves = []
    start_row, start_col = 0, -1
    for row in range(3):
        for col in range(3):
            if state.board[row][col] == 1:
                start_row, start_col = row, col

    for row in range(start_row, 3):
        if row == start_row:
            for col in range(start_col + 1, 3):
                if state.board[row][col] == 0:
                    moves.append((row, col))
        else:
            for col in range(3):
                if state.board[row][col] == 0:
                    moves.append((row, col))

    return moves

def _get_o_moves(state):
    # Find right most o if the board were unraveled.
    moves = []
    start_row, start_col = 0, -1
    for row in range(3):
        for col in range(3):
            if state.board[row][col] == -1:
                start_row, start_col = row, col

    for row in range(start_row, 3):
        if row == start_row:
            for col in range(start_col + 1, 3):
                if state.board[row][col] == 0:
                    moves.append((row, col))
        else:
            for col in range(3):
                if state.board[row][col] == 0:
                    moves.append((row, col))

    return moves
