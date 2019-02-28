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


XAGENT = "X"
XAGENTN = 1
XAGENTW = 3
OAGENT = "O"
OAGENTN = -1
OAGENTW = -3
EMPTY = 0
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

    A state in the game tic tac toe consists of a legal board position and the
    key of the agent whose turn it is.
    """

    def __init__(self, agent_key, board):
        """
        Initializes a tic tac toe state.

        Params:
            agent_key: int|str - the key of the agent whose turn it is.
            board: list - a 3x3 array of -1, 0, 1.  
        """

        self._agent_key = agent_key
        self._board = board

        return

    @property
    def agent_key(self):
        return self._agent_key

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return False

        for row in range(NROWS):
            for col in range(NCOLS):
                if other._board[row][col] != self._board[row][col]:
                    return False

        return True

    def display(self):
        print("Turn: {}".format(self._agent_key))

        print(" ", end="")
        for row in range(NROWS):
            print(" " + str(row), end="")
        print()

        for row in range(NROWS):
            print(row, end="")
            print(" ", end="")
            for col in range(NCOLS):
                if self._board[row][col] == EMPTY:
                    print(" ", end="")
                elif self._board[row][col] == XAGENTN:
                    print(XAGENT, end="")
                else:
                    print(OAGENT, end="")
                if col != NCOLS - 1:
                    print("|", end="")
                else:
                    print()
            if row != NROWS - 1:
                print("  -----")

    def is_terminal(self):
        return False

    def copy(self):
        board = [[EMPTY] * 3, [EMPTY] * 3, [EMPTY] * 3] 
        for row in range(NROWS):
            for col in range(NCOLS):
                board[row][col] = self._board[row][col]

        return TicTacToeState(self.agent_key, board)

    def update(self, action):
        if action.agent_key == XAGENT:
            self._board[action.row][action.col] = XAGENTN
        else:
            self._board[action.row][action.col] = OAGENTN

    def __getitem__(self, key):
        row, col = key

        return self._board[row][col]


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
