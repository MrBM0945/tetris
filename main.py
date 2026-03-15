import pygame
from settings import WIDTH, HEIGHT, PASTEL_BLUE, GRID_BG, GRID_LINE, COLS, ROWS, GRID_X, GRID_Y
from draw import draw_shape, draw_grid, draw_gallery
from tetrominoes import tetrominoes

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tetromino Gallery")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial",30,True)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(PASTEL_BLUE)

    title = font.render("TETRIS", True, (40,40,40))
    screen.blit(title, (WIDTH//2 - title.get_width()//2, 30))

    draw_grid(screen, COLS, ROWS, GRID_X, GRID_Y, GRID_BG, GRID_LINE)

    gallery_start_x = GRID_X + COLS*20 + 50
    gallery_start_y = GRID_Y
    draw_gallery(screen, tetrominoes, gallery_start_x, gallery_start_y, cols_per_row=4, spacing=5)

    pygame.display.update()
    clock.tick(60)

pygame.quit()
