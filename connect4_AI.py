import numpy as np
import pygame
import sys
import math
import random

ROWS = 6
COLUMNS = 7
SQUARESIZE = 100
RADIUS = int(SQUARESIZE/2 - 4)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
PLAYER = 0
AI = 1

EMPTY = 0
PLAYER_PIECE = 1
AI_PIECE = 2

pygame.init()
msg_font = pygame.font.SysFont("monospace", 75)


def create_board():
    ''' initializes the board'''
    board = np.zeros((ROWS, COLUMNS))
    return board


def drop_piece(board, row, col, piece):
    """ adds the pieces to the board """
    board[row][col] = piece


def is_valid_location(board, col):
    """ Checks if the selected column is full """
    return board[ROWS - 1][col] == 0


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

    # checking negatively sloped diagonal
    for c in range(COLUMNS-3):
        for r in range(3, ROWS):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True

def evaluate_window(window, piece):
    score = 0
    opponent_piece = PLAYER_PIECE
    if piece == PLAYER_PIECE:
        opponent_piece = AI_PIECE
    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(EMPTY) == 1:
        score += 20
    elif window.count(piece) == 2 and window.count(EMPTY) == 2:
        score += 10 

    if window.count(opponent_piece) == 3 and window.count(EMPTY) == 1:
        score -= 60   
    return score

def board_score(board, piece):
    score = 0
    #Horizontal evaluation
    for r in range(ROWS):
        row_list = [int(i) for i in list(board[r,:])]
        for c in range(COLUMNS-3):
            four_window = row_list[c:c+4]
            score += evaluate_window(four_window, piece)

    #Vertical evaluation
    for c in range(COLUMNS):
        col_list = [int(i) for i in list(board[:,c])]
        for r in range(ROWS - 3):
            four_window = col_list[r:r+4]
            score += evaluate_window(four_window, piece)

    
    #Positively sloped diagonal evaluation
    for r in range(ROWS - 3):
        for c in range(COLUMNS-3):
            four_window = [board[r+i][c+i] for i in range(4)]
            score += evaluate_window(four_window, piece)


    #Negatively sloped diagonal evaluation
    for r in range(ROWS - 3):
        for c in range(COLUMNS-3):
            four_window = [board[r+(3-i)][c+i] for i in range(4)]
            score += evaluate_window(four_window, piece)
    return score

def get_valid_locations(board):
    valid_locations = []
    for col in range(COLUMNS):
        if is_valid_location(board, col):
            valid_locations.append(col)
    return valid_locations

def pick_move(board, piece):
    best_score = -999999
    valid_locations = get_valid_locations(board)
    best_col = random.choice(valid_locations)
    for col in valid_locations:
        row = get_next_open_row(board, col)
        #creating a copy so we don't modify the original game board
        simulation_board = board.copy()
        drop_piece(simulation_board, row, col, piece)
        score = board_score(simulation_board, piece)
        if score > best_score:
            best_score = score
            best_col = col
        
    return best_col


def draw_board(board):
    for c in range(COLUMNS):
        for r in range(ROWS):
            pygame.draw.rect(window, BLUE, (c*SQUARESIZE, (r+1)
                                            * SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(window, BLACK, (int(
                c*SQUARESIZE + SQUARESIZE/2), int((r+1)*SQUARESIZE + SQUARESIZE/2)), RADIUS)
    for c in range(COLUMNS):
        for r in range(ROWS):
            if board[r][c] == PLAYER_PIECE:
                pygame.draw.circle(window, RED, (int(
                    c*SQUARESIZE + SQUARESIZE/2), height-int((r)*SQUARESIZE + SQUARESIZE/2)), RADIUS)
            elif board[r][c] == AI_PIECE:
                pygame.draw.circle(window, YELLOW, (int(
                    c*SQUARESIZE + SQUARESIZE/2), height-int((r)*SQUARESIZE + SQUARESIZE/2)), RADIUS)
    pygame.display.update()


board = create_board()
game_over = False


width = COLUMNS * SQUARESIZE
height = (ROWS + 1) * SQUARESIZE

window = pygame.display.set_mode((width, height))
draw_board(board)
pygame.display.update()

#Randomly selecting who goes first
turn = random.randint(PLAYER, AI)

#Game loop
while not game_over:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(window, BLACK, (0, 0, width, SQUARESIZE))
            posx = event.pos[0]
            if turn == PLAYER:
                pygame.draw.circle(
                    window, RED, (posx, int(SQUARESIZE/2)), RADIUS)
            # else:
            #     pygame.draw.circle(
            #         window, YELLOW, (posx, int(SQUARESIZE/2)), RADIUS)
            pygame.display.update()
        if event.type == pygame.MOUSEBUTTONDOWN:
            # # Check whose turn it is
            if turn == PLAYER:
                # Player 1 input
                posx = event.pos[0]
                column = (posx // SQUARESIZE)
                if is_valid_location(board, column):
                    row = get_next_open_row(board, column)
                    drop_piece(board, row, column, PLAYER_PIECE)
                    if winning(board, PLAYER_PIECE):
                        pygame.draw.rect(
                            window, BLACK, (0, 0, width, SQUARESIZE))
                        label = msg_font.render(
                            "Player wins!", 1, (255, 255, 255))
                        window.blit(label, (40, 10))
                        game_over = True
                    turn += 1
                    turn %= 2
                    draw_board(board)


    if turn == AI and not game_over:
        # column = random.randint(0, COLUMNS-1)
        column = pick_move(board, AI_PIECE)
        if is_valid_location(board, column):
            pygame.time.wait(1000)
            row = get_next_open_row(board, column)
            drop_piece(board, row, column, AI_PIECE)
            if winning(board, AI_PIECE):
                pygame.draw.rect(window, BLACK, (0, 0, width, SQUARESIZE))
                label = msg_font.render("AI wins!", 1, (255, 255, 255))
                window.blit(label, (40, 10))
                game_over = True

            turn += 1
            turn %= 2
            draw_board(board)

    if game_over:
        pygame.time.wait(3000)