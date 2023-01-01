from board_generator import *
from sys import exit
import pygame

pygame.init()
make_board()


class Board:
    generation = 0


    def __init__(self):
        pass


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
                if board[x][y] == 0:
                    color = COLOR_WHITE
                else:
                    color = COLOR_BACKGROUND
                self.draw_one_cell(x,y, color)

        if Board.generation == 0:
            self.center_board()
        Board.generation += 1
        display_board()



screen = pygame.display.set_mode((WIDTH, HEIGHT)) 
clock = pygame.time.Clock()

board_surface = pygame.Surface(BOARD_SURFACE_DIM)
board_surface_rect = board_surface.get_rect()
inner_board_surface = pygame.Surface((BOARD_SIZE_IN_PX, BOARD_SIZE_IN_PX))
button_surface = pygame.Surface(BUTTON_SURFACE_DIM)

game_board = Board()

rectangle_draging = False
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print("Exiting...")
            pygame.quit()
            exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:            
                if board_surface_rect.collidepoint(event.pos):
                    rectangle_draging = True
                    mouse_x, mouse_y = event.pos
                    offset_x = Board.board_rect.x - mouse_x
                    offset_y = Board.board_rect.y - mouse_y

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:            
                rectangle_draging = False

        elif event.type == pygame.MOUSEMOTION:
            if rectangle_draging:
                mouse_x, mouse_y = event.pos
                Board.board_rect.x = mouse_x + offset_x
                Board.board_rect.y = mouse_y + offset_y


    screen.fill(COLOR_BACKGROUND)
    board_surface.fill(COLOR_BACKGROUND_BRIGHT)
    button_surface.fill(COLOR_BACKGROUND_BRIGHT)

    game_board.draw_all_board()

    board_surface.blit(inner_board_surface, (Board.board_rect.topleft))
    screen.blit(board_surface, (PADDING, PADDING))
    screen.blit(button_surface, (PADDING + BOARD_SURFACE_DIM[0] + PADDING, PADDING))

    pygame.display.update()
    clock.tick(FPS)

