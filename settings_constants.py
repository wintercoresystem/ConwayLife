# Board settings
BOARD_SIZE = 30
NUMBER_OF_RANDOM_CELLS = (BOARD_SIZE ^ 5) * 5

# Utilities
WIDTH = 1800                 # Width of screen in pixels
HEIGHT = 1000                # Height of screen in pixels
PADDING = 10                 # Surface padding
CELL_PADDING = 2             # Cell padding aka grid thickness. Should be less than PADDING
CELL_SIZE = 20
BUTTON_SURFACE_WIDTH = 500   # Width of button surface. Change only this value

# Dont change this
BUTTON_SURFACE_DIM = (BUTTON_SURFACE_WIDTH - PADDING, HEIGHT - PADDING * 2) 
BOARD_SURFACE_DIM = (WIDTH - PADDING * 2 - BUTTON_SURFACE_WIDTH, HEIGHT - PADDING * 2)

BOARD_SURFACE_CENTER = ((BOARD_SURFACE_DIM[0] // 2), BOARD_SURFACE_DIM[1] // 2) 
BOARD_SIZE_IN_PX = BOARD_SIZE * (CELL_SIZE)
BOARD_CENTER = BOARD_SIZE_IN_PX // 2

FPS = 60


# Colors 
COLOR_BACKGROUND = (22, 22, 30)
COLOR_BACKGROUND_BRIGHT = (26, 27, 38)
COLOR_WHITE = (192, 202, 245)
COLOR_ACCENT = (122, 162, 247)
