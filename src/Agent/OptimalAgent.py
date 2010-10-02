"""
Implements the optimal agent
"""

import Agent
from numpy import random
import numpy as np

PLAYER_X = -1
PLAYER_N = 0
PLAYER_O = 1

CORNERS = [(0, 0), (0, 2), (2, 0), (2, 2)]
CENTER = (1, 1)
EDGE_CENTERS = [(0, 1), (1, 0), (1, 2), (2, 1)]
EMPTY = (-1, -1)

def free_corners(actions):
    return list(set(actions).intersection(CORNERS))
def free_edges(actions):
    return list(set(actions).intersection(EDGE_CENTERS))
def free_center(actions):
    return CENTER in actions

def has_corner(board, player):
    return len(get_corners(board, player)) > 0
def has_edge(board, player):
    return len(get_edges(board, player)) > 0
def has_center(board, player):
    return board[CENTER[0]][CENTER[1]] == player

def get_corners(board, player):
    return [ (i, j) for (i, j) in CORNERS if board[i][j] == player ]
def get_edges(board, player):
    return [ (i, j) for (i, j) in EDGE_CENTERS if board[i][j] == player ]

def flip(pos):
    return (2-pos[0], 2-pos[1])

def choose(lst):
    if len(lst) == 1:
        return lst[0]
    else:
        return lst[random.randint(len(lst))]

class OptimalAgent(Agent.Agent):
    def __init__(self):
        Agent.Agent.__init__(self)

    def count_moves(self, board):
        """Count the number of moves that have been played on the board
        @returns movedFirst?, moveNumber
        """
        count = abs(board).sum()
        return count/2

    def first_player(self, board):
        count = abs(board).sum()
        return count % 2 == 0

    def mark(self, board):
        if self.first_player(board):
            return PLAYER_X
        else:
            return PLAYER_O

    def winning(self, board, player):
        board = board
        board_t = board.transpose()
        board_ = np.fliplr(board)

        pos = EMPTY
        # Rows and Columns
        for row in xrange(len(board)):
            if board[row].sum() == 2 * player:
                col = list(board[row]).index(0)
                pos = (row, col)
        for col in xrange(len(board_t)):
            if board_t[col].sum() == 2 * player: 
                row = list(board_t[col]).index(0)
                pos = (row, col)
        # Diagonals
        if board.trace() == 2 * player:
            i = list(board.diagonal()).index(0)
            pos = (i, i)
        elif board_.trace() == 2 * player:
            i = list(board_.diagonal()).index(0)
            pos = (i, 2-i)

        return pos

    def first_player_strategy(self, board, actions):
        move_count = self.count_moves(board)
        if move_count == 0:
            # Play any corner
            action = choose(free_corners(actions))
        elif move_count == 1:
            # If opponent takes the center
            if has_center(board, PLAYER_O):
                # Play the opposite corner as before
                corner = get_corners(board, PLAYER_X)[0]
                return flip(corner)
            # Otherwise take the center
            else:
            # If opponent moved to a corner
                action = CENTER
        elif move_count == 2:
            # Take a corner move
            action = choose(free_corners(actions))
        else:
            action = choose(actions)
        return action

    def second_player_strategy(self, board, actions):
        # If the opponent has played the center, just play corners
        if has_center(board, PLAYER_X):
            if len(free_corners(actions)) > 0:
                action = choose(free_corners(actions))
            else:
                action = choose(actions)
        else:
            move_count = self.count_moves(board)
            if move_count == 0:
                # The opponent has not played center, play center
                action = CENTER
            elif move_count == 1:
                # If the opponent has played a corner and an edge
                if has_edge(board, PLAYER_X) and has_corner(board, PLAYER_X):
                    # Play the opposite corner
                    corner = get_corners(board, PLAYER_X)[0]
                    return flip(corner)
                elif has_edge(board, PLAYER_X) and not has_corner(board, PLAYER_X):
                    edges = get_edges(board, PLAYER_X)
                    # Take the corner bordered by any of the edges
                    MOVES = [(-1, 0), (0, -1), (0, 1), (1, 0)]

                    corners0 = [ (edges[0][0] + i, edges[0][1] + j) for (i, j) in MOVES]
                    corners0 = [ (i, j) for (i, j) in CORNERS ]

                    corners1 = [ (edges[1][0] + i, edges[1][1] + j) for (i, j) in MOVES]
                    corners1 = [ (i, j) for (i, j) in CORNERS ]

                    # If edges border a corner, take it
                    if edges[0] == flip(edges[1]):
                        action = list(set(corners0).intersection(corners1))[0]
                    else:
                        corners = list(set(corners0).union(corners1))
                        action = choose(corners)
                elif not has_edge(board, PLAYER_X) and has_corner(board, PLAYER_X):
                    action = choose(free_edges(actions))
            else:
                action = choose(actions)
        return action

    def act(self, state, actions, rewards):
        # Automatic behaviour - if winning
        pos = self.winning(state, self.mark(state))
        if pos != EMPTY:
            return pos
        # Automatic behaviour - if threatened
        pos = self.winning(state, -1*self.mark(state))
        if pos != EMPTY:
            return pos

        # Strategy behaviour
        if self.first_player(state):
            return self.first_player_strategy(state, actions)
        else:
            return self.second_player_strategy(state, actions)

