import pygame

# Board settings
BOARD_SIZE = 100
NUMBER_OF_RANDOM_CELLS = 1000

# Sizes
WIDTH = 1800                 # Width of screen in pixels
HEIGHT = 1000                # Height of screen in pixels
PADDING = 10                 # Surface padding
CELL_PADDING = 2             # Cell padding aka grid thickness. Should be less than PADDING
CELL_SIZE = 20
BUTTON_SURFACE_WIDTH = 400   # Width of button surface. Change only this value
BUTTON_BORDER_WIDTH = 5 

FPS = 24                     # Frames per second of main window


# Colors 
COLOR_BACKGROUND = (22, 22, 30)
COLOR_BACKGROUND_BRIGHT = (26, 27, 38)
COLOR_WHITE = (192, 202, 245)
COLOR_WHITE_FADED = (213, 188, 200)

COLOR_DARK_PURPLE = "#231123"
COLOR_ACCENT_BLUE = "#7AA2F7"
COLOR_ACCENT_YELLOW = "#EB8258"
COLOR_ACCENT_RED = "#A62639"
COLOR_ACCENT_GREEN = "#26C485"


# Dont change this
BUTTON_SURFACE_DIM = (BUTTON_SURFACE_WIDTH - PADDING, HEIGHT - PADDING * 2)             # Dimentions of button surface
BOARD_SURFACE_DIM = (WIDTH - PADDING * 2 - BUTTON_SURFACE_WIDTH, HEIGHT - PADDING * 2)  # Dimentions of board surface
BOARD_CELLS_VISIBLE = (BOARD_SURFACE_DIM[0] // CELL_SIZE) 

BOARD_SURFACE_CENTER = ((BOARD_SURFACE_DIM[0] // 2), BOARD_SURFACE_DIM[1] // 2)         # Center of board surface in px
BOARD_SIZE_IN_PX = BOARD_SIZE * (CELL_SIZE) 
BOARD_CENTER = BOARD_SIZE_IN_PX // 2
BUTTON_X = BOARD_SURFACE_DIM[0] + PADDING * 3      # x value of buttons, so they are in the middle of button surface
BUTTON_WIDTH = BUTTON_SURFACE_WIDTH - PADDING * 3

VISIBLE_CELLS_X = (BOARD_SURFACE_DIM[0] // CELL_SIZE) + 1
VISIBLE_CELLS_Y = (BOARD_SURFACE_DIM[1] // CELL_SIZE) + 1

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
font = pygame.font.SysFont("Fira Code", 20)
