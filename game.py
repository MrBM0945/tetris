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

        # --- Шрифти (кешуються один раз) ---
        self.font = pygame.font.SysFont("comicsans", 30)
        self.big_font = pygame.font.SysFont("arialblack", 60)
        self.medium_font = pygame.font.SysFont("arialblack", 50)

        # --- Кешовані Surface для overlay ---
        self._overlay = pygame.Surface((settings.WIDTH, settings.HEIGHT))
        self._overlay.set_alpha(180)
        self._overlay.fill((0, 0, 0))

        # --- Звуки ---
        self.move_sound       = pygame.mixer.Sound("assets/sounds/move.wav")
        self.rotate_sound     = pygame.mixer.Sound("assets/sounds/rotate.wav")
        self.drop_sound       = pygame.mixer.Sound("assets/sounds/drop.wav")
        self.hard_drop_sound  = pygame.mixer.Sound("assets/sounds/hard_drop.wav")
        self.clear_sound      = pygame.mixer.Sound("assets/sounds/clear.wav")
        self.hold_sound       = pygame.mixer.Sound("assets/sounds/hold.wav")
        self.game_over_sound  = pygame.mixer.Sound("assets/sounds/game_over.wav")

        # --- Перша фігура ---
        self.current_piece = self.piece_generator.get_next_piece()
        if not self.board.validate_space(self.current_piece):
            self._trigger_game_over()

    # ------------------------------------------------------------------
    # Публічний метод запуску
    # ------------------------------------------------------------------

    def run(self):
        while self.running:
            # clock.tick() ЗАВЖДИ викликається — це головний обмежувач FPS.
            # Якщо прибрати звідси — CPU йде в 100% при паузі/game_over.
            dt = self.clock.tick(settings.FPS)

            self.handle_events()

            if not self.game_over and not self.paused:
                self._update(dt)

            self.draw()

        pygame.quit()
        sys.exit()

    # ------------------------------------------------------------------
    # Обробка подій
    # ------------------------------------------------------------------

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return

            if event.type != pygame.KEYDOWN:
                continue

            # ESC — завершення гри
            if event.key == pygame.K_ESCAPE:
                self._trigger_game_over()
                continue

            # X — вихід з екрану game over
            if self.game_over:
                if event.key == pygame.K_x:
                    self.running = False
                continue

            # P — пауза
            if event.key == pygame.K_p:
                self.paused = not self.paused
                continue

            # Решта керування — тільки під час активної гри
            if self.paused:
                continue

            self._handle_gameplay_key(event.key)

    def _handle_gameplay_key(self, key: int):
        if key == pygame.K_LEFT:
            self.current_piece.move_left()
            if not self.board.validate_space(self.current_piece):
                self.current_piece.move_right()
            else:
                self.move_sound.play()

        elif key == pygame.K_RIGHT:
            self.current_piece.move_right()
            if not self.board.validate_space(self.current_piece):
                self.current_piece.move_left()
            else:
                self.move_sound.play()

        elif key == pygame.K_UP:
            self.current_piece.rotate()
            if not self.board.validate_space(self.current_piece):
                self.current_piece.rotate_back()
            else:
                self.rotate_sound.play()

        elif key == pygame.K_SPACE:
            # Hard drop
            while self.board.validate_space(self.current_piece):
                self.current_piece.move_down()
            self.current_piece.move_up()
            self.hard_drop_sound.play()
            self._lock_piece()

        elif key == pygame.K_c:
            # Hold — звук лише якщо hold спрацював
            new_piece = self.piece_generator.hold_piece(self.current_piece)
            if new_piece is not self.current_piece:
                self.hold_sound.play()
            self.current_piece = new_piece
            if not self.board.validate_space(self.current_piece):
                self._trigger_game_over()

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
                self.drop_sound.play()
                self._lock_piece()

    def _lock_piece(self):
        """Фіксує фігуру на полі, очищає рядки, нараховує очки."""
        for x, y in self.current_piece.get_formatted_shape():
            self.board.locked_positions[(x, y)] = self.current_piece.color

        cleared = self.board.clear_rows()

        if cleared > 0:
            self.clear_sound.play()

        self.score += SCORE_TABLE.get(cleared, 0)

        if self.board.check_game_over():
            self._trigger_game_over()
        else:
            self.current_piece = self.piece_generator.get_next_piece()

    def _trigger_game_over(self):
        """Єдина точка входу для завершення гри."""
        if self.game_over:
            return  # уникаємо подвійного збереження рекорду
        self.data_manager.save_new_score(self.score)
        self.game_over_sound.play()
        self.game_over = True

    # ------------------------------------------------------------------
    # Малювання
    # ------------------------------------------------------------------

    def draw(self):
        self.screen.fill((40, 40, 50))

        self.renderer.draw_title()
        self.renderer.draw_grid(settings.GRID_X, settings.GRID_Y)

        # Заблоковані блоки
        for (x, y), color in self.board.locked_positions.items():
            if y >= 0:
                self.renderer.draw_shape([(x, y)], color, settings.GRID_X, settings.GRID_Y)

        # Ghost piece
        self._draw_ghost()

        # Поточна фігура
        self.renderer.draw_shape(
            self.current_piece.get_formatted_shape(),
            self.current_piece.color,
            settings.GRID_X, settings.GRID_Y
        )

        # Панель справа
        self._draw_panel()

        # Оверлеї (пауза / game over) поверх усього
        if self.paused:
            self._draw_pause_overlay()
        elif self.game_over:
            self._draw_game_over_overlay()

        pygame.display.update()

    # ------------------------------------------------------------------
    # Допоміжні методи малювання
    # ------------------------------------------------------------------

    def _draw_ghost(self):
        """Малює ghost-piece (тінь падіння)."""
        ghost = Piece(
            self.current_piece.x,
            self.current_piece.y,
            self.current_piece.shape_type
        )
        ghost.rotation = self.current_piece.rotation

        while self.board.validate_space(ghost):
            ghost.move_down()
        ghost.move_up()

        r, g, b = self.current_piece.color
        ghost_color = (
            (r + 255 * 3) // 4,
            (g + 255 * 3) // 4,
            (b + 255 * 3) // 4
        )
        self.renderer.draw_ghost_shape(
            ghost.get_formatted_shape(), ghost_color,
            settings.GRID_X, settings.GRID_Y
        )

    def _draw_panel(self):
        """Малює бічну панель зі статистикою, hold та next-preview."""
        x = PANEL_X

        # Score
        self.screen.blit(
            self.font.render(f"Score: {self.score}", True, settings.WHITE),
            (x, settings.GRID_Y + 50)
        )

        # High score
        high_score = self.data_manager.high_score_data["score"]
        self.screen.blit(
            self.font.render(f"High Score: {high_score}", True, (255, 215, 0)),
            (x, settings.GRID_Y + 100)
        )

        # Дата (рендериться кожен кадр — не змінюється частіше ніж раз на добу,
        # але дешевший варіант — кешувати. Залишаємо як є.)
        current_date = self.start_time.strftime("%d.%m.%Y")
        self.screen.blit(
            self.font.render(f"Date: {current_date}", True, settings.WHITE),
            (x, settings.GRID_Y + 130)
        )

        # Час початку та тривалість
        start_time_str = self.start_time.strftime("%H:%M:%S")
        minutes = self.elapsed_seconds // 60
        seconds = self.elapsed_seconds % 60
        self.renderer.draw_game_stats(start_time_str, f"{minutes:02}:{seconds:02}")

        # Hold
        held_shape_type = self.piece_generator.get_held_shape_type()
        if held_shape_type is not None:
            held_def = TetrominoRegistry.get_definition(held_shape_type)
            self.screen.blit(
                self.font.render("Hold:", True, settings.WHITE),
                (x, settings.GRID_Y + 210)
            )
            self.renderer.draw_shape(
                held_def.get_state(0), held_def.color,
                x + 40, settings.GRID_Y + 240
            )

        # Next preview
        self.screen.blit(
            self.font.render("Next:", True, settings.WHITE),
            (x, settings.GRID_Y + 350)
        )
        next_shapes = self.piece_generator.peek_next_shape_types()
        if next_shapes:
            next_def = TetrominoRegistry.get_definition(next_shapes[0])
            self.renderer.draw_shape(
                next_def.get_state(0), next_def.color,
                x + 40, settings.GRID_Y + 400
            )

    def _draw_pause_overlay(self):
        self.screen.blit(self._overlay, (0, 0))

        pause_label = self.big_font.render("PAUSED", True, settings.WHITE)
        cont_label = self.font.render("Press P to continue", True, settings.WHITE)

        self.screen.blit(
            pause_label,
            (settings.WIDTH // 2 - pause_label.get_width() // 2,
             settings.HEIGHT // 2 - pause_label.get_height() // 2)
        )
        self.screen.blit(
            cont_label,
            (settings.WIDTH // 2 - cont_label.get_width() // 2,
             settings.HEIGHT // 2 + 50)
        )

    def _draw_game_over_overlay(self):
        self.screen.blit(self._overlay, (0, 0))

        go_label = self.medium_font.render("GAME OVER", True, settings.WHITE)
        result_label = self.medium_font.render(f"Final Score: {self.score}", True, settings.WHITE)
        exit_label = self.font.render("Press X to exit", True, settings.WHITE)

        cx = settings.WIDTH // 2
        self.screen.blit(go_label,     (cx - go_label.get_width() // 2,     settings.HEIGHT // 2 - 120))
        self.screen.blit(result_label, (cx - result_label.get_width() // 2, settings.HEIGHT // 2 - 40))
        self.screen.blit(exit_label,   (cx - exit_label.get_width() // 2,   settings.HEIGHT // 2 + 30))