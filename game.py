from sound_manager import SoundManager
import pygame
import sys
import settings

from datetime import datetime
from piece import Piece
from board import Board
from piece_factory import PieceGenerator
from renderer import Renderer
from data_manager import DataManager
from tetrominoes import TetrominoRegistry
from input_handler import InputHandler


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
        self.board = Board(settings.COLS, settings.ROWS)
        self.piece_generator = PieceGenerator(start_x=3, start_y=0, preview_size=3)
        self.data_manager = DataManager()
        self.sound_manager = SoundManager()
        self.input_handler = InputHandler(self)

        # --- Стан гри ---
        self.score: int = 0
        self.running: bool = True
        self.paused: bool = False
        self.game_over: bool = False

        # --- Фізика падіння ---
        self.fall_speed: float = settings.FALL_SPEED
        self.fall_interval: float = 1000.0 / self.fall_speed
        self.fall_time: float = 0.0
        self.speed_time: float = 0.0

        # --- Таймер ---
        self.start_time: datetime = datetime.now()
        self.start_ticks: int = pygame.time.get_ticks()
        self.elapsed_seconds: int = 0

        # --- Перша фігура ---
        self.current_piece = self.piece_generator.get_next_piece()
        self.ghost_coords = []
        self._update_ghost()
        if not self.board.validate_space(self.current_piece):
            self._trigger_game_over()

    def run(self):
        while self.running:
            dt = self.clock.tick(settings.FPS)
            self.input_handler.handle_input()

            if not self.game_over and not self.paused:
                self._update(dt)

            self.draw()

        pygame.quit()
        sys.exit()
    # ------------------------------------------------------------------
    # Логіка оновлення стану гри
    # ------------------------------------------------------------------

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

    def _trigger_game_over(self):
        """Єдина точка входу для завершення гри."""
        if self.game_over:
            return  # уникаємо подвійного збереження рекорду
        self.data_manager.save_new_score(self.score)
        self.sound_manager.play("game_over")
        self.game_over = True

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
        # 1. Тло
        self.screen.fill((40, 40, 50))
        self.renderer.draw_title()
        self.renderer.draw_grid(settings.GRID_X, settings.GRID_Y)

        # 2. Нерухомі блоки на полі
        for (x, y), color in self.board.locked_positions.items():
            if y >= 0:
                self.renderer.draw_shape([(x, y)], color, settings.GRID_X, settings.GRID_Y)

        # 3. Тінь та Активна фігура
        self.renderer.draw_ghost(self.ghost_coords, self.current_piece.color)
        self.renderer.draw_shape(
            self.current_piece.get_formatted_shape(),
            self.current_piece.color,
            settings.GRID_X, settings.GRID_Y
        )

        # 4. Бічна панель (передаємо тільки чисті дані)
        self.renderer.draw_ui_panel(
            score=self.score,
            high_score=self.data_manager.high_score_data["score"],
            start_time=self.start_time,
            elapsed_seconds=self.elapsed_seconds,
            held_type=self.piece_generator.get_held_shape_type(),
            next_shapes=self.piece_generator.peek_next_shape_types()
        )

        # 5. Стани (Пауза / Кінець гри)
        if self.paused:
            self.renderer.draw_pause()
        elif self.game_over:
            self.renderer.draw_game_over(self.score)

        pygame.display.update()


   

