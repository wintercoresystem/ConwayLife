from sys import exit
import pygame
import numpy as np
from settings_constants import *
from random import randint
from time import sleep
from multiprocessing import Process, Queue



class Board:
    generation = 0

    def __init__(self):
        self.make_board()
        self.populate_with_random()

        self.process = Process(target=self.new_cicle_loop)
        self.queue = Queue()
        self.simulation_state = False


    def make_board(self):
        self.board = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype="bool")


    def populate_with_random(self):
        self.board[0][0] = True
        for _ in range(NUMBER_OF_RANDOM_CELLS):
            x, y = randint(0, BOARD_SIZE - 1), randint(0, BOARD_SIZE - 1)
            self.board[x][y] = True


    def zerofy_board(self):
        self.board.fill(0)


    def get_cell_state(self, cell_x, cell_y):
        return self.board[cell_x][cell_y] == 1


    def remove_cell(self, cell_x, cell_y, board):
        board[cell_x][cell_y] = 0


    def make_cell(self, cell_x, cell_y, board):
        board[cell_x][cell_y] = 1


    def get_neighbours(self, cell_x, cell_y, board):
        neighbours = 0
        for i in range(cell_x - 1, cell_x + 2):
            for j in range(cell_y - 1, cell_y + 2):
                if not (i == cell_x and j == cell_y):
                    try:
                        neighbours += board[i][j]
                    except Exception:
                        pass

        return neighbours


    def new_cicle(self):
        temp_board = np.copy(self.board)
        for x in range(BOARD_SIZE):
            for y in range(BOARD_SIZE):
                neighbours = self.get_neighbours(x, y, self.board)
                if neighbours < 2:
                    self.remove_cell(x,y, temp_board)
                elif neighbours == 3:
                    self.make_cell(x,y, temp_board)
                elif neighbours > 3:
                    self.remove_cell(x,y, temp_board)
        self.board = temp_board
        self.queue.put(temp_board)
        return temp_board


    def draw_one_cell(self, row, column, color):
        cell_rect = pygame.Rect(row * CELL_SIZE,        # Cell x position
                                column * CELL_SIZE,     # Cell y position
                                CELL_SIZE - CELL_PADDING, CELL_SIZE - CELL_PADDING) # Cell size
        pygame.draw.rect(inner_board_surface, color, cell_rect)


    def draw_all_board(self):
        if self.queue.empty():
            pass
        else:
            self.board = self.queue.get()

        for x in range(BOARD_SIZE):
            for y in range(BOARD_SIZE):
                if self.get_cell_state(x, y):
                    color = COLOR_ACCENT_RED
                else:
                    color = COLOR_WHITE
                self.draw_one_cell(x,y, color)

        if Board.generation == 0:
            self.center_board()
        Board.generation += 1


    def center_board(self):
        board_center = inner_board_surface.get_rect()
        board_center.center = BOARD_SURFACE_CENTER
        Board.board_rect = board_center


    def new_cicle_loop(self):
        while True:
            print("yeah")
            self.draw_all_board()
            sleep(SIMULATION_SPEED)
            self.new_cicle()


    def run_simulation(self):
        if not self.simulation_state:
            print("Starting simulation")
            self.process.start()
            self.simulation_state = True

    def stop_simulation(self):
        if self.simulation_state:
            print("Stopping simulation")
            self.process.terminate()
            self.process.kill()
            self.process.join()
            self.process = Process(target=self.new_cicle_loop)
            self.simulation_state = False



screen = pygame.display.set_mode((WIDTH, HEIGHT)) 
clock = pygame.time.Clock()

board_surface = pygame.Surface(BOARD_SURFACE_DIM)
board_surface_rect = board_surface.get_rect()
inner_board_surface = pygame.Surface((BOARD_SIZE_IN_PX, BOARD_SIZE_IN_PX))
button_surface = pygame.Surface(BUTTON_SURFACE_DIM)

game_board = Board()

middle_button_drag = False
first_button_drag = False

game_board.run_simulation()


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print("Exiting...")
            game_board.stop_simulation()
            pygame.quit()
            exit()

    # Mouse events
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Cell toggling catch
            if event.button == 1:
                if board_surface_rect.collidepoint(event.pos):
                    first_button_drag = True
                    mouse_x, mouse_y = event.pos
                    row = ((mouse_x - Board.board_rect.x - PADDING) // CELL_SIZE)
                    column = ((mouse_y - Board.board_rect.y - PADDING) // CELL_SIZE)
                    state = game_board.get_cell_state(row, column)

                    game_board.stop_simulation()
                    if state == 1:
                        game_board.remove_cell(row, column, game_board.board)
                    else:
                        game_board.make_cell(row, column, game_board.board)

            # Panning catch
            if event.button == 2:            
                if board_surface_rect.collidepoint(event.pos):
                    middle_button_drag = True
                    mouse_x, mouse_y = event.pos
                    offset_x = Board.board_rect.x - mouse_x
                    offset_y = Board.board_rect.y - mouse_y

            if event.button == 4:
                print("up")
            if event.button == 5:
                print("down")

        elif event.type == pygame.MOUSEMOTION:
            if first_button_drag:
                mouse_x, mouse_y = event.pos
                row, column = (0, 0)
                row = ((mouse_x - Board.board_rect.x - PADDING) // CELL_SIZE)
                column = ((mouse_y - Board.board_rect.y - PADDING) // CELL_SIZE)
                if state == 1:
                    game_board.remove_cell(row, column, game_board.board)
                else:
                    game_board.make_cell(row, column, game_board.board)


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
                game_board.run_simulation()
            if event.button == 2:            
                middle_button_drag = False


        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                game_board.board = game_board.new_cicle()
            if event.key == pygame.K_a:
                game_board.run_simulation()
            if event.key == pygame.K_d:
                game_board.stop_simulation()
            if event.key == pygame.K_w:
                SIMULATION_SPEED /= 1.1
                game_board.stop_simulation()
                game_board.run_simulation()
            if event.key == pygame.K_s:
                SIMULATION_SPEED *= 1.1
                game_board.stop_simulation()
                game_board.run_simulation()
                


    game_board.draw_all_board()

    screen.fill(COLOR_BACKGROUND)
    board_surface.fill(COLOR_BACKGROUND_BRIGHT)
    button_surface.fill(COLOR_BACKGROUND_BRIGHT)


    board_surface.blit(inner_board_surface, (Board.board_rect.topleft))
    screen.blit(board_surface, (PADDING, PADDING))
    screen.blit(button_surface, (PADDING + BOARD_SURFACE_DIM[0] + PADDING, PADDING))

    pygame.display.update()
    clock.tick(FPS)
