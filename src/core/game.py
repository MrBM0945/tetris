from src.core.states import GameState
from src.managers.sound_manager import SoundManager
import pygame
import sys
from src.config import settings

from datetime import datetime
from src.entities.piece import Piece
from src.core.board import Board
from src.entities.piece_factory import PieceGenerator
from src.ui.renderer import Renderer
from src.managers.data_manager import DataManager
from src.entities.tetrominoes import TetrominoRegistry
from src.managers.input_handler import InputHandler


# Таблиця очок за кількість очищених ліній
SCORE_TABLE = {1: 100, 2: 300, 3: 500, 4: 1200}

# Оффсет панелі (права сторона)
PANEL_X = settings.GRID_X + settings.COLS * settings.CELL + 30


class TetrisGame:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        self.screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
        pygame.display.set_caption("Tetris")
        self.clock = pygame.time.Clock()

        # --- Підсистеми ---
        self.renderer = Renderer(self.screen)
        self.data_manager = DataManager()
        self.sound_manager = SoundManager()
        self.input_handler = InputHandler(self)

        # --- Стан гри ---
        self.running: bool = True
        self.state = GameState.MENU
    
    def restart_game(self):
        """Цей метод викликається при старті з меню або після програшу."""
        self.board = Board(settings.COLS, settings.ROWS)
        self.piece_generator = PieceGenerator(start_x=3, start_y=0, preview_size=3)
        self.score = 0
        
        self.fall_speed = settings.FALL_SPEED
        self.fall_interval = 1000.0 / self.fall_speed
        self.fall_time = 0.0
        self.speed_time = 0.0
        
        self.start_time = datetime.now()
        self.start_ticks = pygame.time.get_ticks()
        self.elapsed_seconds = 0

        self.current_piece = self.piece_generator.get_next_piece()
        self.ghost_coords = []
        self._update_ghost()
        
        self.state = GameState.PLAYING # Переводимо в режим гри

    def run(self):
        while self.running:
            dt = self.clock.tick(settings.FPS)
            self.input_handler.handle_input()

            if self.state == GameState.PLAYING:
                self._update(dt)

            self.draw()

        pygame.quit()
        sys.exit()
    
    def _trigger_game_over(self):
        if self.state == GameState.GAME_OVER:
            return
        self.data_manager.save_new_score(self.score)
        self.sound_manager.play("game_over")
        self.state = GameState.GAME_OVER

    def _update(self, dt: float):
        self.elapsed_seconds = (pygame.time.get_ticks() - self.start_ticks) // 1000
        self.fall_time += dt
        self.speed_time += dt

        # Збільшення швидкості кожні N секунд
        if self.speed_time >= settings.SPEED_INCREASE_INTERVAL * 1000:
            self.speed_time = 0.0
            self.fall_speed = min(
                self.fall_speed * (1.0 + settings.SPEED_INCREASE_PERCENT),
                settings.MAX_FALL_SPEED
            )
            self.fall_interval = 1000.0 / self.fall_speed

        # Soft drop (утримання ↓)
        keys = pygame.key.get_pressed()
        current_interval = (
            self.fall_interval / settings.SOFT_DROP_MULTIPLIER
            if keys[pygame.K_DOWN]
            else self.fall_interval
        )

        if self.fall_time >= current_interval:
            self.fall_time = 0.0
            self.current_piece.move_down()
            if not self.board.validate_space(self.current_piece):
                self.current_piece.move_up()
                self.sound_manager.play("drop")
                self._lock_piece()

    def _lock_piece(self):
        """Фіксує фігуру на полі, очищає рядки, нараховує очки."""
        for x, y in self.current_piece.get_formatted_shape():
            self.board.locked_positions[(x, y)] = self.current_piece.color

        cleared = self.board.clear_rows()

        if cleared > 0:
            self.sound_manager.play("clear")

        self.score += SCORE_TABLE.get(cleared, 0)

        if self.board.check_game_over():
            self._trigger_game_over()
        else:
            self.current_piece = self.piece_generator.get_next_piece()
            self._update_ghost()

    def _update_ghost(self):
        """ОБЧИСЛЮЄ координати тіні. Викликати ТІЛЬКИ при зміні позиції/повороту фігури."""
        ghost = Piece(
            self.current_piece.x,
            self.current_piece.y,
            self.current_piece.shape_type
        )
        ghost.rotation = self.current_piece.rotation

        while self.board.validate_space(ghost):
            ghost.move_down()
        ghost.move_up()

        # Зберігаємо готові координати
        self.ghost_coords = ghost.get_formatted_shape()
    
    def draw(self):
        if self.state == GameState.MENU:
            # 1. Малюємо ТІЛЬКИ головне меню, ніякого поля і блоків
            self.renderer.draw_main_menu()
        else:
            # 2. Малюємо гру (PLAYING, PAUSED або GAME_OVER)
            self.screen.fill((40, 40, 50))
            self.renderer.draw_title()
            self.renderer.draw_grid(settings.GRID_X, settings.GRID_Y)

            for (x, y), color in self.board.locked_positions.items():
                if y >= 0:
                    self.renderer.draw_shape([(x, y)], color, settings.GRID_X, settings.GRID_Y)

            self.renderer.draw_ghost(self.ghost_coords, self.current_piece.color)
            self.renderer.draw_shape(
                self.current_piece.get_formatted_shape(),
                self.current_piece.color,
                settings.GRID_X, settings.GRID_Y
            )

            self.renderer.draw_ui_panel(
                score=self.score,
                high_score=self.data_manager.high_score_data["score"],
                start_time=self.start_time,
                elapsed_seconds=self.elapsed_seconds,
                held_type=self.piece_generator.get_held_shape_type(),
                next_shapes=self.piece_generator.peek_next_shape_types()
            )

            # Оверлеї поверх гри
            if self.state == GameState.PAUSED:
                self.renderer.draw_pause()
            elif self.state == GameState.GAME_OVER:
                self.renderer.draw_game_over(self.score)

        pygame.display.update()


   

