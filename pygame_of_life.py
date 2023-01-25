from sys import exit
import sys
import numpy as np
from settings_constants import *
from widgets import *
from random import randint
from time import sleep
from multiprocessing import Process, Queue


# TODO: Refactor it into two classes: board and draw, because at some point I need to make lots of boards.
class Board:
    generation = 0

    def __init__(self):
        self.board = self.make_board()
        # self.populate_with_random()

        self.process = Process(target=self.new_cicle_loop)
        self.queue = Queue()
        self.simulation_state = False
        self.simulation_speed = 4

    # Initialize board with only zeroes
    def make_board(self):
        return np.zeros((BOARD_SIZE, BOARD_SIZE), dtype="bool")

    # Randomly make alive cells in board using NUMBER_OF_RANDOM_CELLS from settings
    def populate_with_random(self) -> None:
        self.board[0][0] = True
        for _ in range(NUMBER_OF_RANDOM_CELLS):
            x, y = randint(0, BOARD_SIZE - 1), randint(0, BOARD_SIZE - 1)
            self.board[x][y] = True

    # Clear board
    def zerofy_board(self) -> None:
        self.board.fill(0)

    # Get cell state using x and y coordinates
    def get_cell_state(self, cell_x, cell_y) -> bool:
        return self.board[cell_x][cell_y] == 1

    # Kill cell (turn off) using x and y coordinates
    def remove_cell(self, cell_x, cell_y, board) -> None:
        try:
            board[cell_x][cell_y] = 0
        except IndexError:
            pass

    # Born cell (turn on) using x and y coordinates
    def make_cell(self, cell_x, cell_y, board) -> None:
        try:
            board[cell_x][cell_y] = 1
        except IndexError:
            pass

    # Get alive neighbours by Moore neighbourhood
    def get_neighbours(self, cell_x, cell_y, board) -> int:
        neighbours = 0
        for i in range(cell_x - 1, cell_x + 2):
            for j in range(cell_y - 1, cell_y + 2):
                if not (i == cell_x and j == cell_y):
                    try:
                        neighbours += board[i][j]
                    except IndexError:
                        pass

        return neighbours

    # Create new generation using rules in match statement using neighbours count
    def new_cicle(self) -> None:
        # print(f"Cicle {self.generation}")
        # We need to make temporary board so neighbours doesn't affected by actions we make during this generation
        temp_board = np.copy(self.board)
        for x in range(BOARD_SIZE):
            for y in range(BOARD_SIZE):
                neighbours = self.get_neighbours(x, y, self.board)
                """
                This is basic B3/23S rule:
                Any live cell with fewer than two live neighbours dies (referred to as underpopulation or exposure).
                Any live cell with more than three live neighbours dies (referred to as overpopulation or overcrowding).
                Any live cell with two or three live neighbours lives, unchanged, to the next generation.
                Any dead cell with exactly three live neighbours will come to life.
                """
                match neighbours:
                    case 2:
                        pass
                    case 3:
                        self.make_cell(x, y, temp_board)
                    case _:
                        self.remove_cell(x, y, temp_board)
        self.board = temp_board
        self.queue.put(temp_board)
        return temp_board

    # This is function to draw one cell from the board according to its coordinates and state
    def draw_one_cell(self, row, column, color) -> None:
        cell_rect = pygame.Rect(row * CELL_SIZE,  # Cell x position
                                column * CELL_SIZE,  # Cell y position
                                CELL_SIZE - CELL_PADDING, CELL_SIZE - CELL_PADDING)  # Cell size
        pygame.draw.rect(inner_board_surface, color, cell_rect)

    # Draw entire board
    def draw_all_board(self) -> None:
        if self.queue.empty():
            pass
        else:
            self.board = self.queue.get()

        for x in range(BOARD_SIZE):
            for y in range(BOARD_SIZE):
                # This is on state color
                if self.get_cell_state(x, y):
                    color = COLOR_DARK_PURPLE

                # This is off state color
                else:
                    if self.simulation_state:  # This is color while simulation is running
                        color = COLOR_WHITE
                    else:
                        color = COLOR_WHITE_FADED  # This is color while simulation is stopped
                self.draw_one_cell(x, y, color)

        if self.generation == 0:  # Center board in the begining
            self.center_board()
        self.return_to_board()

        self.generation += 1

    # Focus center of the board
    def center_board(self) -> None:
        board_center = inner_board_surface.get_rect()
        board_center.center = BOARD_SURFACE_CENTER
        Board.board_rect = board_center

    # You can't go out of bounds
    def return_to_board(self) -> None:
        if self.board_rect.x > 500:
            self.board_rect.x = 500
        if self.board_rect.y > 500:
            self.board_rect.y = 500
        if self.board_rect.x < -BOARD_SIZE_IN_PX + 500:
            self.board_rect.x = -BOARD_SIZE_IN_PX + 500
        if self.board_rect.y < -BOARD_SIZE_IN_PX + 500:
            self.board_rect.y = -BOARD_SIZE_IN_PX + 500

    # Process of making new cicles at specific speed using simulation_speed
    def new_cicle_loop(self) -> None:
        while True:
            self.draw_all_board()
            sleep(1 / self.simulation_speed)
            self.new_cicle()


    def update_simulation_speed(self, value) -> None:
        if value > 1:
            self.simulation_speed = value
        print(f"Sim speed: {self.simulation_speed}")
        if self.simulation_state == 1:
            self.stop_simulation()
            self.run_simulation()


    def toggle_simulation_state(self) -> None:
        if self.simulation_state:
            self.stop_simulation()
        else:
            self.run_simulation()



    # Make separate process of cicles so interface doesn't lag while new_cicle called
    def run_simulation(self) -> None:
        if not self.simulation_state:
            print("Starting simulation")
            self.process.start()
            self.simulation_state = True
            start_button.update_text("Stop")

    # Stop this process
    def stop_simulation(self) -> None:
        if self.simulation_state:
            print("Stopping simulation")
            self.process.terminate()
            self.process.kill()
            self.process.join()
            self.process = Process(target=self.new_cicle_loop)
            self.simulation_state = False
            start_button.update_text("Start")

def update_simulation_speed_by_slider():
    game_board.update_simulation_speed(int(simulation_speed_slider.value))


board_surface = pygame.Surface(BOARD_SURFACE_DIM)
board_surface_rect = board_surface.get_rect()
inner_board_surface = pygame.Surface((BOARD_SIZE_IN_PX, BOARD_SIZE_IN_PX))
button_surface = pygame.Surface(BUTTON_SURFACE_DIM)

game_board = Board()

start_button = Button(pos_x=BUTTON_X,
                      pos_y=PADDING * 2, 
                      width=BUTTON_WIDTH, 
                      text="Start",
                      action=game_board.toggle_simulation_state)

simulation_speed_slider = Slider(pos_x=BUTTON_X, 
                                 width=BUTTON_WIDTH, 
                                 min_value=1,
                                 max_value=100,
                                 action=update_simulation_speed_by_slider)


game_board.run_simulation()

middle_button_drag = False
first_button_drag = False
simulation_state_before_drag = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print("Exiting...")
            game_board.stop_simulation()
            pygame.quit()
            print("Done!")
            exit()

        # Mouse click events
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Cell toggling catch and stopping time while dragging
            if event.button == 1:
                if board_surface_rect.collidepoint(event.pos):
                    first_button_drag = True
                    mouse_x, mouse_y = event.pos
                    row = ((mouse_x - game_board.board_rect.x - PADDING) // CELL_SIZE)
                    column = ((mouse_y - game_board.board_rect.y - PADDING) // CELL_SIZE)
                    state = game_board.get_cell_state(row, column)

                    simulation_state_before_drag = game_board.simulation_state
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
                    offset_x = game_board.board_rect.x - mouse_x
                    offset_y = game_board.board_rect.y - mouse_y


        # Mouse dragging events
        elif event.type == pygame.MOUSEMOTION:
            # Create / remove cells while dragging
            if first_button_drag:
                mouse_x, mouse_y = event.pos
                row, column = (0, 0)
                row = ((mouse_x - game_board.board_rect.x - PADDING) // CELL_SIZE)
                column = ((mouse_y - game_board.board_rect.y - PADDING) // CELL_SIZE)
                if state == 1:
                    game_board.remove_cell(row, column, game_board.board)
                else:
                    game_board.make_cell(row, column, game_board.board)

            # Panning while dragging
            if middle_button_drag:
                mouse_x, mouse_y = event.pos
                game_board.board_rect.x = mouse_x + offset_x
                game_board.board_rect.y = mouse_y + offset_y


        # Mouse after click events
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                first_button_drag = False
                # Run simulation again if it was running before cell toggling
                if simulation_state_before_drag:
                    game_board.run_simulation()

            if event.button == 2:
                middle_button_drag = False

        elif event.type == pygame.MOUSEWHEEL:
            # Pan with mouse wheel or touchpad
            game_board.board_rect.x += event.x * 15
            game_board.board_rect.y += event.y * 15

        # Keyboard events
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                game_board.board = game_board.new_cicle()
            if event.key == pygame.K_a:
                game_board.run_simulation()

            if event.key == pygame.K_d:
                game_board.stop_simulation()

            if event.key == pygame.K_w:
                game_board.update_simulation_speed(game_board.simulation_speed + 1)
                simulation_speed_slider.slide.x += 4
                simulation_speed_slider.update_slider_value()

            if event.key == pygame.K_s:
                game_board.update_simulation_speed(game_board.simulation_speed - 1)
                simulation_speed_slider.slide.x -= 4
                simulation_speed_slider.update_slider_value()

        # Automatic widget action catch
        Widget.action_all_widget(event)

    screen.fill(COLOR_BACKGROUND)
    board_surface.fill(COLOR_BACKGROUND_BRIGHT)
    button_surface.fill(COLOR_BACKGROUND_BRIGHT)

    game_board.draw_all_board()


    board_surface.blit(inner_board_surface, (Board.board_rect.topleft))
    screen.blit(board_surface, (PADDING, PADDING))
    screen.blit(button_surface, (PADDING + BOARD_SURFACE_DIM[0] + PADDING, PADDING))

    Widget.draw_all_widgets()


    pygame.display.update()
    clock.tick(FPS)
