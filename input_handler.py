import pygame
import sys

class InputHandler:
    def __init__(self, game):
        # Передаємо посилання на головний об'єкт гри, 
        # щоб контролер міг викликати його методи
        self.game = game

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.running = False
                return

            if event.type != pygame.KEYDOWN:
                continue

            # Глобальна кнопка виходу
            if event.key == pygame.K_ESCAPE:
                if not self.game.game_over:
                    self.game._trigger_game_over()
                else:
                    self.game.running = False
                continue

            # Екран Game Over
            if self.game.game_over:
                if event.key == pygame.K_x:
                    self.game.running = False
                continue

            # Пауза
            if event.key == pygame.K_p:
                self.game.paused = not self.game.paused
                continue

            # Керування фігурою (тільки під час гри)
            if not self.game.paused and not self.game.game_over:
                self._handle_gameplay_key(event.key)

    def _handle_gameplay_key(self, key: int):
        # Тут живе вся та логіка, що була в грі
        if key == pygame.K_LEFT:
            self.game.current_piece.move_left()
            if not self.game.board.validate_space(self.game.current_piece):
                self.game.current_piece.move_right()
            else:
                self.game.sound_manager.play("move")
                self.game._update_ghost()

        elif key == pygame.K_RIGHT:
            self.game.current_piece.move_right()
            if not self.game.board.validate_space(self.game.current_piece):
                self.game.current_piece.move_left()
            else:
                self.game.sound_manager.play("move")
                self.game._update_ghost()

        elif key == pygame.K_UP:
            self.game.current_piece.rotate()
            if not self.game.board.validate_space(self.game.current_piece):
                self.game.current_piece.rotate_back()
            else:
                self.game.sound_manager.play("rotate")
                self.game._update_ghost()

        elif key == pygame.K_SPACE:
            while self.game.board.validate_space(self.game.current_piece):
                self.game.current_piece.move_down()
            self.game.current_piece.move_up()
            self.game.sound_manager.play("hard_drop")
            self.game._lock_piece()

        elif key == pygame.K_c:
            new_piece = self.game.piece_generator.hold_piece(self.game.current_piece)
            if new_piece is not self.game.current_piece:
                self.game.sound_manager.play("hold")
            self.game.current_piece = new_piece
            self.game._update_ghost()
            if not self.game.board.validate_space(self.game.current_piece):
                self.game._trigger_game_over()