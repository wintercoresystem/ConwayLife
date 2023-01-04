import numpy as np
from settings_constants import *
from random import randint
from time import sleep


def make_board():
    global board
    board = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype="bool")
    board[BOARD_SIZE // 2][BOARD_SIZE // 2] = 1

def generate_random_board():
    board[0][0] = True
    for _ in range(NUMBER_OF_RANDOM_CELLS):
        x, y = randint(0, BOARD_SIZE - 1), randint(0, BOARD_SIZE - 1)
        board[x][y] = True

def zerofy_board():
    board.fill(0)


make_board()
generate_random_board()

# def toggle_cell(cell_x, cell_y):
#     if board[cell_x][cell_y] == 1:
#         board[cell_x][cell_y] = 0
#     else:
#         board[cell_x][cell_y] = 1


def remove_cell(cell_x, cell_y):
    board[cell_x][cell_y] = 0


def make_cell(cell_x, cell_y):
    board[cell_x][cell_y] = 1


def display_board():
    print(str(board * 1)
          .replace("1", "■")
          .replace("0", "·")
          .replace("[", " ")
          .replace("]", " ")
          )
    print("---------------------------------------------------------------")

def get_neighbours(cell_x, cell_y, board):
    # neighbours += board[cell_x + 1][cell_y]
    # neighbours += board[cell_x][cell_y + 1]
    # neighbours += board[cell_x + 1][cell_y + 1]
    # neighbours += board[cell_x - 1][cell_y]
    # neighbours += board[cell_x][cell_y - 1]
    # neighbours += board[cell_x - 1][cell_y - 1]
    # neighbours += board[cell_x + 1][cell_y - 1]
    # neighbours += board[cell_x - 1][cell_y + 1]
    # print(f"Neighbours at ({cell_x}, {cell_y}): {neighbours}")
    neighbours = 0
    for i in range(cell_x - 1, cell_x + 2):
        for j in range(cell_y - 1, cell_y + 2):
            neighbours += board[i][j]
        print(neighbours, end=" ")
    print()

    return neighbours


def new_cicle():
    temp_board = np.copy(board)
    temp_board = np.tile(temp_board, (3,3))
    for x in range(BOARD_SIZE):
        for y in range(BOARD_SIZE):
            neighbours = get_neighbours(x, y, temp_board)
            if neighbours < 2:
                remove_cell(x,y)
            elif neighbours == 3:
                make_cell(x,y)
            elif neighbours > 3:
                remove_cell(x,y)

display_board()
new_cicle()
display_board()
