import pygame
import sys
import settings
from board import Board
from piece_factory import PieceGenerator
import draw

class TetrisGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
        pygame.display.set_caption("ShitTetris")
        self.clock = pygame.time.Clock()
        self.renderer = Renderer(self.screen)
        
        self.board = Board(settings.COLS, settings.ROWS)
        self.piece_generator = PieceGenerator(start_x=3, start_y=0, preview_size=3)
        self.current_piece = self.piece_generator.get_next_piece()
        
        self.score = 0
        self.running = True
        
        if not self.board.validate_space(self.current_piece):
            print("Game Over at start!")
            self.running = False

        self.fall_time = 0
        self.fall_speed = settings.FALL_SPEED * 1000 # переводимо в мілісекунди
        self.font = pygame.font.SysFont("comicsans", 30)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.current_piece.move_left()
                    if not self.board.validate_space(self.current_piece):
                        self.current_piece.move_right()
                elif event.key == pygame.K_RIGHT:
                    self.current_piece.move_right()
                    if not self.board.validate_space(self.current_piece):
                        self.current_piece.move_left()
                elif event.key == pygame.K_DOWN:
                    self.current_piece.move_down()
                    if not self.board.validate_space(self.current_piece):
                        self.current_piece.move_up()
                elif event.key == pygame.K_UP:
                    self.current_piece.rotate()
                    if not self.board.validate_space(self.current_piece):
                        self.current_piece.rotate_back()

    def update(self):
        if not self.running:
            return

        dt = self.clock.tick(settings.FPS)
        self.fall_time += dt

        if self.fall_time >= self.fall_speed:
            self.fall_time = 0
            self.current_piece.move_down()
            
            # Якщо після падіння фігура заблокована (досягла дна або іншої фігури)
            if not self.board.validate_space(self.current_piece):
                self.current_piece.move_up()
                
                # Фіксуємо фігуру в словнику на дошці
                for x, y in self.current_piece.get_formatted_shape():
                    self.board.locked_positions[(x, y)] = self.current_piece.color
                
                # Очищаємо заповнені рядки
                self.board.update_grid()
                cleared = self.board.clear_rows()
                self.score += cleared * 10
                
                # Перевірка на кінець гри
                if self.board.check_game_over():
                    print(f"Game Over! Final Score: {self.score}")
                    self.running = False
                else:
                    self.current_piece = self.piece_generator.get_next_piece()

    def draw(self):
        self.screen.fill((40, 40, 50))
        
        # Малюємо сітку через рендерер
        self.renderer.draw_grid(
            settings.COLS, settings.ROWS, 
            settings.GRID_X, settings.GRID_Y, 
            settings.GRID_BG, settings.GRID_LINE
        )
        
        # Малюємо заблоковані фігури на дошці
        for (x, y), color in self.board.locked_positions.items():
            if y >= 0:
                self.renderer.draw_shape([(x, y)], None, settings.GRID_X, settings.GRID_Y)

        # Малюємо активну фігуру
        shape_coords = self.current_piece.get_formatted_shape()
        self.renderer.draw_shape(shape_coords, self.current_piece.shape_type, settings.GRID_X, settings.GRID_Y)
                
        label = self.font.render(f"Score: {self.score}", True, settings.WHITE)
        self.screen.blit(label, (settings.GRID_X + settings.COLS * settings.CELL + 30, settings.GRID_Y + 50))
        pygame.display.update()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            if self.running: # Малюємо лише якщо гра триває
                self.draw()
        
        pygame.quit()

if __name__ == "__main__":
    game = TetrisGame()
    game.run()