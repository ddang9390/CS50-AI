"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    xs = 0
    os = 0
    for row in board:
        xs += row.count(X)
        os += row.count(O)

    if xs > os:
        return O
    
    return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    if terminal(board):
        return set()
    
    res = set()

    for i, row in enumerate(board):
        for j, col in enumerate(row):
            if board[i][j] == EMPTY:
                res.add((i, j))

    return res


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    acts = actions(board)
    if action not in acts:
        raise RuntimeError('Action not permitted')
    
    i = action[0]
    j = action[1]
    board_copy = copy.deepcopy(board)
    board_copy[i][j] = player(board)

    return board_copy


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    #Checking rows
    for row in board:
        if len(set(row)) == 1 and row[0] != EMPTY:
            return row[0]
        
    #Checking diagonals
    diagonal1 = set()
    diagonal1.update([board[0][0], board[1][1], board[2][2]])
    if len(diagonal1) == 1:
        return board[0][0]
    
    diagonal2 = set()
    diagonal2.update([board[2][0], board[1][1], board[0][2]])
    if len(diagonal2) == 1:
        return board[2][0]

    #Checking columns
    col = 0
    while col < 3:
        column = set()
        column.add(board[0][col])
        column.add(board[1][col])
        column.add(board[2][col])

        if len(column) == 1:
            return board[0][col]
        
        col +=1
    return None

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) != None:
        return True
    
    for row in board:
        for col in row:
            if col == EMPTY:
                return False

    return True

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    win = winner(board)

    if win == X:
        return 1
    elif win == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    p = player(board)

    if p == X:
        return max_value(board, None)[1]
    else:
        return min_value(board, None)[1]
    
 
    
def max_value(board, a):
    v = [-math.inf, None]
    if terminal(board):
        return [utility(board), None]

    for action in actions(board):
        m = min_value(result(board, action), action)[0]
        if v[0] < m:

            v = [m, action]
            if v[0] == 1:
                return v

    return v

def min_value(board, a):
    v = [math.inf, None]
    if terminal(board):
        return [utility(board), None]

    for action in actions(board):
        m = max_value(result(board, action), action)[0]
        if v[0] > m:
            v = [m, action]
            if v[0] == -1:
                return v

    return v