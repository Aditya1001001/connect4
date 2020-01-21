import numpy as np 

ROWS = 6
COLUMNS = 7

def create_board():
    board = np.zeros((ROWS,COLUMNS))
    return board

def drop_piece(board, row, col, piece):
    """ adds the pieces to the board """
    board[row][col] = piece

def is_valid_location(board, col):
    """ Checks if the selected column is full """
    return board[ROWS -1][col] == 0 

def get_next_open_row(board, col):
    """ Finds the first empty row in the selected column """
    for r in range(ROWS):
        if board[r][col] == 0:
            return r

def print_board(board):
    """ flips the board """
    print(np.flip(board, 0))

def winning(board, piece):
    """ Checks for winning condition"""
    # checking horizontal neighbours for win
    for c in range(COLUMNS-3):
        for r in range(ROWS):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True

    # checking vertical neighbours for win
    for c in range(COLUMNS):
        for r in range(ROWS - 3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True

    # checking positively sloped diagonal
    for c in range(COLUMNS-3):
        for r in range(ROWS - 3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True

    # checking positively sloped diagonal
    for c in range(COLUMNS-3):
        for r in range(3, ROWS):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True




board = create_board()
game_over = False
turn = 0

while not game_over:
    # Check whose turn it is
    if turn == 0:
        # Player 1 input
        column = int(input("Player 1 choose your selected column(0-6): "))
        if is_valid_location(board, column):
            row = get_next_open_row(board, column)
            drop_piece(board, row,column, 1)
            if winning(board, 1):
                print("Player 1 wins!")
                game_over = True
    else:
        # Player 2 input
        column = int(input("Player 2 choose your selected column(0-6): "))
        if is_valid_location(board, column):
            row = get_next_open_row(board, column)
            drop_piece(board, row,column, 2  )
            if winning(board, 2):
                print("Player 2 wins!")
                game_over = True
    turn +=1
    turn %=2
    if not game_over:
        print_board(board)

