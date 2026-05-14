from src.core.states import GameState
import pygame
import sys

class InputHandler:
    def __init__(self, game):
        # Передаємо посилання на головний об'єкт гри, 
        # щоб контролер міг викликати його методи
        self.game = game

    # pyrefly: ignore [parse-error]
    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.running = False
                return

            if event.type != pygame.KEYDOWN:
                continue

            # --- Обробка натискань залежно від поточного екрану ---
            if self.game.state == GameState.MENU:
                if event.key == pygame.K_RETURN: # Натиснули Enter
                    self.game.restart_game()
                elif event.key == pygame.K_ESCAPE: # В меню ESC закриває гру
                    self.game.running = False

            elif self.game.state == GameState.GAME_OVER:
                if event.key == pygame.K_RETURN:
                    self.game.restart_game()         # Enter -> почати заново
                elif event.key == pygame.K_ESCAPE:
                    self.game.state = GameState.MENU # ESC -> головне меню

            elif self.game.state == GameState.PAUSED:
                if event.key == pygame.K_p:
                    self.game.state = GameState.PLAYING # P -> забрати паузу
                elif event.key == pygame.K_ESCAPE:
                    self.game.state = GameState.MENU    # ESC -> головне меню

            elif self.game.state == GameState.PLAYING:
                if event.key == pygame.K_p or event.key == pygame.K_ESCAPE:
                    self.game.state = GameState.PAUSED  # ESC або P під час гри -> Пауза
                else:
                    self._handle_gameplay_key(event.key)
    

    # pyrefly: ignore [parse-error]
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