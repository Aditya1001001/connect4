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


def draw_board(board):
    for c in range(COLUMNS):
        for r in range(ROWS):
            pygame.draw.rect(window, BLUE, (c*SQUARESIZE, (r+1)
                                            * SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(window, BLACK, (int(
                c*SQUARESIZE + SQUARESIZE/2), int((r+1)*SQUARESIZE + SQUARESIZE/2)), RADIUS)
    for c in range(COLUMNS):
        for r in range(ROWS):
            if board[r][c] == 1:
                pygame.draw.circle(window, RED, (int(
                    c*SQUARESIZE + SQUARESIZE/2), height-int((r)*SQUARESIZE + SQUARESIZE/2)), RADIUS)
            elif board[r][c] == 2:
                pygame.draw.circle(window, YELLOW, (int(
                    c*SQUARESIZE + SQUARESIZE/2), height-int((r)*SQUARESIZE + SQUARESIZE/2)), RADIUS)
    pygame.display.update()


board = create_board()
game_over = False
turn = 0


width = COLUMNS * SQUARESIZE
height = (ROWS + 1) * SQUARESIZE

window = pygame.display.set_mode((width, height))
draw_board(board)
pygame.display.update()


#Game loop
while not game_over:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(window, BLACK, (0, 0, width, SQUARESIZE))
            posx = event.pos[0]
            if turn == 0:
                pygame.draw.circle(
                    window, RED, (posx, int(SQUARESIZE/2)), RADIUS)
            else:
                pygame.draw.circle(
                    window, YELLOW, (posx, int(SQUARESIZE/2)), RADIUS)
            pygame.display.update()
        if event.type == pygame.MOUSEBUTTONDOWN:
            # # Check whose turn it is
            if turn == PLAYER:
                # Player 1 input
                posx = event.pos[0]
                column = (posx // SQUARESIZE)
                if is_valid_location(board, column):
                    row = get_next_open_row(board, column)
                    drop_piece(board, row, column, 1)
                    if winning(board, 1):
                        pygame.draw.rect(
                            window, BLACK, (0, 0, width, SQUARESIZE))
                        label = msg_font.render(
                            "Player 1 wins!", 1, (255, 255, 255))
                        window.blit(label, (40, 10))
                        game_over = True
                    turn += 1
                    turn %= 2


    if turn == AI and not game_over:
        column = random.randint(0, COLUMNS-1)
        if is_valid_location(board, column):
            pygame.time.wait(1000)
            row = get_next_open_row(board, column)
            drop_piece(board, row, column, 2)
            if winning(board, 2):
                pygame.draw.rect(window, BLACK, (0, 0, width, SQUARESIZE))
                label = msg_font.render("AI wins!", 1, (255, 255, 255))
                window.blit(label, (40, 10))
                game_over = True

            turn += 1
            turn %= 2
            draw_board(board)
            if game_over:
                pygame.time.wait(5000)