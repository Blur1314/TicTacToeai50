"""
Tic Tac Toe Player
"""
from copy import deepcopy
import math

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
    if terminal(board) is True:
        return None

    i = 0
    for x in board:
        for j in x:
            if j == X or j == O:
                i+= 1

    if i%2 == 0:
        return X
    else:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    if terminal(board) is True:
        return set()
    target = EMPTY
    ret = set()
    for r , row in enumerate (board):
        for c, val in enumerate(row):
            if val == target:
                ret.add((r, c))

    return ret



def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """

    if board[action[0]][action[1]] == X or board[action[0]][action[1]] == O:
        raise Exception("Space already taken")

    boar = deepcopy(board)

    if player(board) == X:
        boar[action[0]][action[1]] = X
        return boar

    elif player(board) == O:
        boar[action[0]][action[1]] = O
        return boar

    else:
        raise Exception("Player function not working or draw")

def checkwon(board):
    # checking horizontally

    for x in board:
        if x[0] == x[1] == x[2] != EMPTY:
            return True

    # checking vertically
    for i in range(3):
        # board[row][column]
        if board[0][i] == board[1][i] == board[2][i] != EMPTY:
            return True


    # checking diaganally
    b = board

    if b[0][0] == b[1][1] == b[2][2] != EMPTY:
        return True
    elif b[0][2] == b[1][1] == b[2][0] != EMPTY:
        return True

    return None

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    for row in board:
        if row[0] == row[1] == row[2] and row[0] is not None:
            return row[0]

        # Check columns directly (using your fixed column loop logic!)
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] is not None:
            return board[0][col]

        # Check diagonals directly
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not None:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] is not None:
        return board[0][2]

        # No winner found
    return None

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """

    if checkwon(board) is True:
        return True



    #checking for all filled , game is tied
    for x in board:
        for j in x:
            if j == EMPTY:
                return False
    return True




def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board) is True:
        return None
    if board == initial_state():
        return (0, 0)
    def Max_value(board):
        if terminal(board):
            return utility(board)

        v = -math.inf


        for action in actions(board):
            v = max(v, Min_value(result(board, action)))
        return v

    def Min_value(board):
        if terminal(board):
            return utility(board)

        v = math.inf


        for action in actions(board):
            v = min(v, Max_value(result(board, action)))
        return v


    current_player = player(board)
    best_move = None

    if current_player == X:
        best_val = -math.inf
        for action in actions(board):
            # X wants the HIGHEST score resulting from O's best response
            move_val = Min_value(result(board, action))
            if move_val > best_val:
                best_val = move_val
                best_move = action

    elif current_player == O:
        best_val = math.inf
        for action in actions(board):
            # O wants the LOWEST score resulting from X's best response
            move_val = Max_value(result(board, action))
            if move_val < best_val:
                best_val = move_val
                best_move = action

    return best_move