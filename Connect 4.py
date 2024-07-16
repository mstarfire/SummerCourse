import random
import math

# Constants for the game
ROWS = 6
COLS = 7
EMPTY = 0
PLAYER_ONE = 1
PLAYER_TWO = 2
WINDOW_LENGTH = 4
AI_PLAYER = PLAYER_TWO
HUMAN_PLAYER = PLAYER_ONE

# Create the game board
def create_board():
    board = [[EMPTY for _ in range(COLS)] for _ in range(ROWS)]
    return board

# Drop a piece into the board
def drop_piece(board, row, col, piece):
    board[row][col] = piece

# Check if a column is a valid location to drop a piece
def is_valid_location(board, col):
    return board[ROWS-1][col] == EMPTY

# Get the next open row in the column
def get_next_open_row(board, col):
    for r in range(ROWS):
        if board[r][col] == EMPTY:
            return r

# Print the board
def print_board(board):
    for row in reversed(board):
        print(' '.join(map(str, row)))

# Check for a winning move
def winning_move(board, piece):
    # Check horizontal locations
    for c in range(COLS-3):
        for r in range(ROWS):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True

    # Check vertical locations
    for c in range(COLS):
        for r in range(ROWS-3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True

    # Check positively sloped diagonals
    for c in range(COLS-3):
        for r in range(ROWS-3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True

    # Check negatively sloped diagonals
    for c in range(COLS-3):
        for r in range(3, ROWS):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True

# Evaluate the window
def evaluate_window(window, piece):
    score = 0
    opp_piece = PLAYER_ONE if piece == PLAYER_TWO else PLAYER_TWO

    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(EMPTY) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(EMPTY) == 2:
        score += 2

    if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
        score -= 4

    return score

# Score the board
def score_position(board, piece):
    score = 0

    # Score center column
    center_array = [int(i) for i in list(zip(*board))[COLS//2]]
    center_count = center_array.count(piece)
    score += center_count * 3

    # Score horizontal
    for r in range(ROWS):
        row_array = [int(i) for i in board[r]]
        for c in range(COLS-3):
            window = row_array[c:c+WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    # Score vertical
    for c in range(COLS):
        col_array = [int(i) for i in list(zip(*board))[c]]
        for r in range(ROWS-3):
            window = col_array[r:r+WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    # Score positively sloped diagonal
    for r in range(ROWS-3):
        for c in range(COLS-3):
            window = [board[r+i][c+i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    # Score negatively sloped diagonal
    for r in range(ROWS-3):
        for c in range(COLS-3):
            window = [board[r+3-i][c+i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    return score

# Check if the board is full
def is_terminal_node(board):
    return winning_move(board, PLAYER_ONE) or winning_move(board, PLAYER_TWO) or len(get_valid_locations(board)) == 0

# Minimax algorithm with alpha-beta pruning
def minimax(board, depth, alpha, beta, maximizingPlayer):
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)
    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(board, PLAYER_TWO):
                return (None, 100000000000000)
            elif winning_move(board, PLAYER_ONE):
                return (None, -10000000000000)
            else: # Game is over, no more valid moves
                return (None, 0)
        else: # Depth is zero
            return (None, score_position(board, PLAYER_TWO))
    if maximizingPlayer:
        value = -math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = [row.copy() for row in board]
            drop_piece(b_copy, row, col, PLAYER_TWO)
            new_score = minimax(b_copy, depth-1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return column, value
    else: # Minimizing player
        value = math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = [row.copy() for row in board]
            drop_piece(b_copy, row, col, PLAYER_ONE)
            new_score = minimax(b_copy, depth-1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return column, value

# Get valid locations
def get_valid_locations(board):
    valid_locations = []
    for col in range(COLS):
        if is_valid_location(board, col):
            valid_locations.append(col)
    return valid_locations

# Main game loop
def play_connect4():
    board = create_board()
    print_board(board)
    game_over = False
    turn = random.randint(PLAYER_ONE, PLAYER_TWO)

    while not game_over:
        if turn == PLAYER_ONE:
            col = int(input("Player 1 Make your Selection (0-6): "))

            if is_valid_location(board, col):
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, PLAYER_ONE)

                if winning_move(board, PLAYER_ONE):
                    print_board(board)
                    print("Player 1 wins!!")
                    game_over = True

        else: # AI's turn
            col, minimax_score = minimax(board, 5, -math.inf, math.inf, True)

            if is_valid_location(board, col):
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, PLAYER_TWO)

                if winning_move(board, PLAYER_TWO):
                    print_board(board)
                    print("Player 2 wins!!")
                    game_over = True

        print_board(board)
        turn += 1
        turn = turn % 2

if __name__ == "__main__":
    play_connect4()
