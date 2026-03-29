import pygame
import sys
import settings
from board import Board
from piece_factory import create_random_piece
import draw
class TetrisGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
        self.board = Board(settings.COLS, settings.ROWS)
        self.current_piece = create_random_piece()
        self.score = 0
        self.running = True

    def handle_events(self):
        for event in pygame.event.get():
            pass

    def update(self):
        pass

    def draw(self):
        pass

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()