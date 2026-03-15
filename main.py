import pygame
from settings import WIDTH, HEIGHT, CELL, GRID_BG, COLS, ROWS, GRID_X, GRID_Y, GRID_LINE, SHAPE_COLORS, TETROMINOES
from draw import draw_shape, draw_grid, draw_gallery

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tetromino Gallery")
clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
    screen.fill((255, 255, 255))

    draw_grid(screen, COLS, ROWS, GRID_X, GRID_Y, GRID_BG, GRID_LINE)
    
    draw_gallery(screen, TETROMINOES, GRID_X + (COLS * CELL) + 50, GRID_Y)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
