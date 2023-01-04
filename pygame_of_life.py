from sys import exit
import pygame
import numpy as np
from settings_constants import *
from random import randint
from time import sleep



class Board:
    generation = 0


    def __init__(self):
        self.board = self.make_board()
        self.generate_random_board()


    def make_board(self):
        self.board = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype="bool")
        return self.board


    def generate_random_board(self):
        self.board[0][0] = True
        for _ in range(NUMBER_OF_RANDOM_CELLS):
            x, y = randint(0, BOARD_SIZE - 1), randint(0, BOARD_SIZE - 1)
            self.board[x][y] = True


    def zerofy_board(self):
        self.board.fill(0)


    def get_cell_state(self, cell_x, cell_y):
        if self.board[cell_x][cell_y] == 1:
            return 1 
        else:
            return 0



    def toggle_cell(self, cell_x, cell_y):
        if self.board[cell_x][cell_y] == 1:
            self.board[cell_x][cell_y] = 0
        else:
            self.board[cell_x][cell_y] = 1


    def remove_cell(self, cell_x, cell_y):
        self.board[cell_x][cell_y] = 0


    def make_cell(self, cell_x, cell_y):
        self.board[cell_x][cell_y] = 1


    def get_neighbours(self, cell_x, cell_y, board):
        neighbours = 0
        cell_x += 1
        cell_y += 1
        for i in range(cell_x - 1, cell_x + 2):
            for j in range(cell_y - 1, cell_y + 2):
                if not (i == cell_x and j == cell_y):
                    neighbours += board[i][j]

        return neighbours


    def new_cicle(self):
        temp_board = np.copy(self.board)
        temp_board = np.insert(temp_board, BOARD_SIZE, False, axis=0)
        temp_board = np.insert(temp_board, 0,          False, axis=0)
        temp_board = np.insert(temp_board, BOARD_SIZE, False, axis=1)
        temp_board = np.insert(temp_board, 0,          False, axis=1)
        for x in range(BOARD_SIZE):
            for y in range(BOARD_SIZE):
                neighbours = self.get_neighbours(x, y, temp_board)
                if neighbours < 2:
                    self.remove_cell(x,y)
                elif neighbours == 3:
                    self.make_cell(x,y)
                elif neighbours > 3:
                    self.remove_cell(x,y)


    def draw_one_cell(self, row, column, color):
        cell_rect = pygame.Rect(row * CELL_SIZE,        # Cell x position
                                column * CELL_SIZE,     # Cell y position
                                CELL_SIZE - CELL_PADDING, CELL_SIZE - CELL_PADDING) # Cell size
        pygame.draw.rect(inner_board_surface, color, cell_rect)


    def center_board(self):
        board_rect = inner_board_surface.get_rect()
        board_rect.center = BOARD_SURFACE_CENTER
        Board.board_rect = board_rect


    def draw_all_board(self):
        for x in range(BOARD_SIZE):
            for y in range(BOARD_SIZE):
                if self.board[x][y] == 0:
                    color = COLOR_WHITE
                else:
                    color = COLOR_DARK_PURPLE

                self.draw_one_cell(x,y, color)

        if Board.generation == 0:
            self.center_board()
        Board.generation += 1

        self.new_cicle()



screen = pygame.display.set_mode((WIDTH, HEIGHT)) 
clock = pygame.time.Clock()

board_surface = pygame.Surface(BOARD_SURFACE_DIM)
board_surface_rect = board_surface.get_rect()
inner_board_surface = pygame.Surface((BOARD_SIZE_IN_PX, BOARD_SIZE_IN_PX))
button_surface = pygame.Surface(BUTTON_SURFACE_DIM)

game_board = Board()

middle_button_drag = False
first_button_drag = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print("Exiting...")
            pygame.quit()
            exit()

    # Mouse events
        # Pan on middle button
        elif event.type == pygame.MOUSEBUTTONDOWN:

            # Cell toggling catch
            if event.button == 1:
                if board_surface_rect.collidepoint(event.pos):
                    first_button_drag = True
                    mouse_x, mouse_y = event.pos
                    row = ((mouse_x - Board.board_rect.x - PADDING) // CELL_SIZE)
                    column = ((mouse_y - Board.board_rect.y - PADDING) // CELL_SIZE)
                    state = game_board.get_cell_state(row, column)

                    if state == 1:
                        game_board.remove_cell(row, column)
                    else:
                        game_board.make_cell(row, column)

            # Panning catch
            if event.button == 2:            
                if board_surface_rect.collidepoint(event.pos):
                    middle_button_drag = True
                    mouse_x, mouse_y = event.pos
                    offset_x = Board.board_rect.x - mouse_x
                    offset_y = Board.board_rect.y - mouse_y

        elif event.type == pygame.MOUSEMOTION:
            if first_button_drag:
                mouse_x, mouse_y = event.pos
                row, column = (0, 0)
                row = ((mouse_x - Board.board_rect.x - PADDING) // CELL_SIZE)
                column = ((mouse_y - Board.board_rect.y - PADDING) // CELL_SIZE)
                if state == 1:
                    game_board.remove_cell(row, column)
                else:
                    game_board.make_cell(row, column)


            # Panning
            if middle_button_drag:
                mouse_x, mouse_y = event.pos
                if 600 > Board.board_rect.x > -1400:
                    Board.board_rect.x = mouse_x + offset_x
                else:
                    if Board.board_rect.x > 0:
                        Board.board_rect.x -= 1
                    else:
                        Board.board_rect.x += 1

                if 600 > Board.board_rect.y > -1400:
                    Board.board_rect.y = mouse_y + offset_y
                else:
                    if Board.board_rect.y > 0:
                        Board.board_rect.y -= 1
                    else:
                        Board.board_rect.y += 1

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:            
                first_button_drag = False
            if event.button == 2:            
                middle_button_drag = False


        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                game_board.new_cicle()


    screen.fill(COLOR_BACKGROUND)
    board_surface.fill(COLOR_BACKGROUND_BRIGHT)
    button_surface.fill(COLOR_BACKGROUND_BRIGHT)

    game_board.draw_all_board()

    board_surface.blit(inner_board_surface, (Board.board_rect.topleft))
    screen.blit(board_surface, (PADDING, PADDING))
    screen.blit(button_surface, (PADDING + BOARD_SURFACE_DIM[0] + PADDING, PADDING))

    pygame.display.update()
    clock.tick(FPS)
