"""
TicTacToe Environment
"""

import numpy as np
import Environment.Environment
import Agent

PLAYER_X = -1
PLAYER_N = 0
PLAYER_O = 1

# Load an agent
def load(agent, agent_args):
    """Load an agent"""
    try:
        mod = __import__("Agent.%s"%(agent), fromlist=[Agent])
        assert( hasattr(mod, agent) )
        agent = getattr(mod, agent)
        agent = agent(*agent_args)
    except (ImportError, AssertionError):
        raise ValueError("Agent '%s' could not be found"%(agent))
    return agent

class TicTacToe(Environment.Environment):
    """
    TicTacToe Environment
    Expects starting position and opponent Agent to be given
    """
    opponent = None
    opponent_starts = True

    # State represented by a 3-value 3x3 board (X, O, -)
    board = None

    # Environment Interface
    def __init__(self, opponent_starts, opponent, opponent_args):
        """
        @opponent_starts - Does the opponent start the game?
        @opponent - string name of the opponent
        @opponent_args - string args for the opponent
        """
        Environment.Environment.__init__(self)
        self.opponent = load(opponent, opponent_args)
        self.opponent_starts = opponent_starts

        self.board = self.__init_board()

    def __str__(self):
        val = ""
        val += "[TicTacToe]\n"
        for row in self.board:
            for col in row:
                if col == PLAYER_X: 
                    val += 'X '
                elif col == PLAYER_N: 
                    val += '  '
                elif col == PLAYER_O: 
                    val += 'O '
            val[-1] = '\n'
        return val
    
    def __repr__(self):
        return "[TicTacToe %d]" % (id(self))

    def start(self):
        # Play a round with the opponent
        if self.opponent_starts:
            action = self.opponent.act(self.board, self.__get_actions(), 0)
            self.__apply_action(action, self.__opponent_mark())
        return self.board, self.__get_actions(), 0

    def react(self, action):
        # Check action
        if action not in self.__get_actions():
            raise ValueError( "%s not a valid action"%(action) )

        # Play a turn
        self.__apply_action(action, self.__player_mark())
        action = self.opponent.act(self.board, self.__get_actions(), 0)
        self.__apply_action(action, self.__opponent_mark())

        # Check win
        winner = self.__check_winner()
        if winner == self.__player_mark():
            self.board = self.__init_board()
            reward = 1
        elif winner == self.__player_mark():
            self.board = self.__init_board()
            reward = -1
        else:
            reward = 0

        return self.board, self.__get_actions(), reward

    def __init_board(self):
        """Return the empty board - all PLAYER_N"""
        return np.array([ [ PLAYER_N for i in xrange(3) ] for j in xrange(3) ])
    
    def __get_actions(self):
        """Get all valid actions for board state"""
        def get_actions_(board):
            """Enumerate valid actions"""
            for row in xrange(len(board)):
                for col in xrange(len(row)):
                    if self.board[row][col] == 0:
                        yield (row, col)
        return [ x for x in get_actions_(self.board) ]

    def __opponent_mark(self):
        """Get the mark of the opponent"""
        if self.opponent_starts: 
            return PLAYER_X
        else:
            return PLAYER_O

    def __player_mark(self):
        """Get the mark of the player"""
        if self.opponent_starts: 
            return PLAYER_O
        else:
            return PLAYER_X

    def __apply_action(self, action, player):
        """Modify state, given the action"""
        self.board[action[0]][action[1]] = player

    def __check_winner(self):
        """Find if there is a winner, and return it"""
        # Check all rows, columns and diagonals 
        board = self.board
        board_ = np.fliplr(board)

        # Rows and Columns
        for row, col in zip(board, board.transpose()):
            if row.sum() == 3 * PLAYER_X or col.sum() == 3*PLAYER_X:
                return PLAYER_X
            elif row.sum() == 3 * PLAYER_O or col.sum() == 3*PLAYER_O:
                return PLAYER_O

        # Diagonals
        if board.trace() == 3 * PLAYER_X or board_.trace() == 3 * PLAYER_X:
            return PLAYER_X
        elif board.trace() == 3 * PLAYER_O or board_.trace() == 3 * PLAYER_O:
            return PLAYER_O

        return PLAYER_N
   
