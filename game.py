import pygame
import sys
import settings
from board import Board
from piece_factory import PieceGenerator
from renderer import Renderer
from data_manager import DataManager
from tetrominoes import TetrominoRegistry

class TetrisGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
       
        pygame.display.set_caption("Tetris")
        self.clock = pygame.time.Clock()
        self.renderer = Renderer(self.screen)
        
        self.board = Board(settings.COLS, settings.ROWS)
        self.piece_generator = PieceGenerator(start_x=3, start_y=0, preview_size=3)
        self.current_piece = self.piece_generator.get_next_piece()
        self.data_manager = DataManager()
        
        self.score = 0
        self.running = True
        self.paused = False
        self.game_over = False
        
        if not self.board.validate_space(self.current_piece):
            print("Game Over at start!")
            self.running = False

        self.fall_time = 0
        self.speed_time = 0

        self.fall_speed = settings.FALL_SPEED
        self.fall_interval = 1000 / self.fall_speed

        self.font = pygame.font.SysFont("comicsans", 30)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            if event.type == pygame.KEYDOWN:
                
                if event.key == pygame.K_ESCAPE:
                    print(f"Game exited! Final Score: {self.score}")
                    self.data_manager.save_new_score(self.score)
                    self.game_over = True
                    continue
                
                if self.game_over and event.key == pygame.K_x:
                    self.running = False
                    continue

                if self.game_over:
                    continue
                    
                if event.key == pygame.K_LEFT:
                    self.current_piece.move_left()

                    if not self.board.validate_space(self.current_piece):
                        self.current_piece.move_right()

                elif event.key == pygame.K_RIGHT:
                    self.current_piece.move_right()

                    if not self.board.validate_space(self.current_piece):
                        self.current_piece.move_left()
                        
                elif event.key == pygame.K_SPACE:
                    while self.board.validate_space(self.current_piece):
                        self.current_piece.move_down()
                    self.current_piece.move_up()
                    self.fall_time = self.fall_speed

                elif event.key == pygame.K_UP:
                    self.current_piece.rotate()

                    if not self.board.validate_space(self.current_piece):
                        self.current_piece.rotate_back()
                        
                elif event.key == pygame.K_c:
                    self.current_piece = self.piece_generator.hold_piece(self.current_piece)
                    if not self.board.validate_space(self.current_piece):
                        print("Game Over after hold!")
                        self.data_manager.save_new_score(self.score)
                        self.running = False
                
                elif event.key == pygame.K_p:
                    self.paused = not self.paused
                      
                

    def update(self):
        if not self.running:
            return

        if self.game_over:
            return

        if self.paused:
            return

        dt = self.clock.tick(settings.FPS)
        self.fall_time += dt
        self.speed_time += dt

        if self.speed_time >= settings.SPEED_INCREASE_INTERVAL * 1000:
            self.speed_time = 0
            self.fall_speed += self.fall_speed * settings.SPEED_INCREASE_PERCENT
            
            if self.fall_speed > settings.MAX_FALL_SPEED:
                self.fall_speed = settings.MAX_FALL_SPEED

            self.fall_interval = 1000 / self.fall_speed

        keys = pygame.key.get_pressed()

        current_interval = self.fall_interval
        if keys[pygame.K_DOWN]:
            current_interval = self.fall_interval / settings.SOFT_DROP_MULTIPLIER
        if self.fall_time >= current_interval:
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
                    self.data_manager.save_new_score(self.score)
                    self.running = False
                else:
                    self.current_piece = self.piece_generator.get_next_piece()

    def draw(self):
        self.screen.fill((40, 40, 50))
        
        self.renderer = Renderer(self.screen)
        self.renderer.draw_title()
        
        self.renderer.draw_grid(
            settings.COLS, settings.ROWS, 
            settings.GRID_X, settings.GRID_Y, 
            settings.GRID_BG, settings.GRID_LINE
        )
        
        # Малюємо заблоковані кубики знизу
        for (x, y), color in self.board.locked_positions.items():
            if y >= 0:
                self.renderer.draw_shape([(x, y)], color, settings.GRID_X, settings.GRID_Y)

        # Малюємо активну фігуру (ту, що падає)
        shape_coords = self.current_piece.get_formatted_shape()
        self.renderer.draw_shape(shape_coords, self.current_piece.color, settings.GRID_X, settings.GRID_Y)
                
        # Текст інтерфейсу
        label = self.font.render(f"Score: {self.score}", True, settings.WHITE)
        self.screen.blit(label, (settings.GRID_X + settings.COLS * settings.CELL + 30, settings.GRID_Y + 50))
        
        # Вивід рекорду
        high_score = self.data_manager.high_score_data["score"]
        hs_date = self.data_manager.high_score_data["date"]
        
        hs_label = self.font.render(f"High Score: {high_score}", True, (255, 215, 0))
        self.screen.blit(hs_label, (settings.GRID_X + settings.COLS * settings.CELL + 30, settings.GRID_Y + 100))
        
        date_label = self.font.render(f"Date: {hs_date}", True, settings.WHITE)
        self.screen.blit(date_label, (settings.GRID_X + settings.COLS * settings.CELL + 30, settings.GRID_Y + 130))

        hold_label = self.font.render("Hold:", True, settings.WHITE)
        self.screen.blit(
            hold_label,
            (settings.GRID_X + settings.COLS * settings.CELL + 30, settings.GRID_Y + 190)
        )

        held_shape_type = self.piece_generator.get_held_shape_type()

        if held_shape_type is not None:
            held_definition = TetrominoRegistry.get_definition(held_shape_type)
            held_template = held_definition.get_state(0)

            hold_x = settings.GRID_X + settings.COLS * settings.CELL + 70
            hold_y = settings.GRID_Y + 240

            self.renderer.draw_shape(
                held_template,
                held_definition.color,
                hold_x,
                hold_y
            )

        next_label = self.font.render("Next:", True, settings.WHITE)
        self.screen.blit(
            next_label,
            (settings.GRID_X + settings.COLS * settings.CELL + 30, settings.GRID_Y + 350)
        )

        next_shapes = self.piece_generator.peek_next_shape_types()

        if next_shapes:
            next_shape_type = next_shapes[0]
            next_definition = TetrominoRegistry.get_definition(next_shape_type)
            next_template = next_definition.get_state(0)

            preview_x = settings.GRID_X + settings.COLS * settings.CELL + 70
            preview_y = settings.GRID_Y + 400

            self.renderer.draw_shape(
                next_template,
                next_definition.color,
                preview_x,
                preview_y
            )
        
        if self.paused:
            overlay = pygame.Surface((settings.WIDTH, settings.HEIGHT))
            overlay.set_alpha(180)
            overlay.fill((0, 0, 0))
            self.screen.blit(overlay, (0, 0))
            pause_font = pygame.font.SysFont("arialblack", 60)

            pause_label = pause_font.render(
                "PAUSED",
                True,
                (255, 255, 255)
            )
            continue_label = self.font.render(
                "Press P to continue",
                True,
                settings.WHITE
            )

            pause_x = settings.WIDTH // 2 - pause_label.get_width() // 2
            pause_y = settings.HEIGHT // 2 - pause_label.get_height() // 2

            self.screen.blit(pause_label, (pause_x, pause_y))
            continue_x = settings.WIDTH // 2 - continue_label.get_width() // 2
            continue_y = settings.HEIGHT // 2 + 50
            self.screen.blit(continue_label, (continue_x, continue_y))
            
        
           
        if self.game_over:
            overlay = pygame.Surface((settings.WIDTH, settings.HEIGHT))
            overlay.set_alpha(180)
            overlay.fill((0, 0, 0))
            self.screen.blit(overlay, (0, 0))
            game_over_font = pygame.font.SysFont("arialblack", 50)

            result_label = game_over_font.render(
                f"Final Score: {self.score}",
                True,
                settings.WHITE
            )

            exit_label = self.font.render(
                "Press X to exit",
                True,
                settings.WHITE
            )

            result_x = settings.WIDTH // 2 - result_label.get_width() // 2
            result_y = settings.HEIGHT // 2 - 40

            exit_x = settings.WIDTH // 2 - exit_label.get_width() // 2
            exit_y = settings.HEIGHT // 2 + 30

            self.screen.blit(result_label, (result_x, result_y))
            self.screen.blit(exit_label, (exit_x, exit_y))
        pygame.display.update()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            if self.running: # Малюємо лише якщо гра триває
                self.draw()
        
        pygame.quit()