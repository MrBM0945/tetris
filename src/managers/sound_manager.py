import os
import pygame

class SoundManager:
    """
    Клас для безпечного завантаження та відтворення звуків.
    Відповідає за перевірку наявності файлів та управління аудіо.
    """
    def __init__(self, base_path: str = "assets/sounds/"):
        self.base_path = base_path
        self.sounds = {}
        
        # Ініціалізуємо мікшер, якщо він ще не запущений
        if not pygame.mixer.get_init():
            pygame.mixer.init()
            
        self._load_all()

    def _load(self, name: str, filename: str) -> None:
        """Внутрішній метод для безпечного завантаження одного звуку."""
        path = os.path.join(self.base_path, filename)
        if os.path.exists(path):
            self.sounds[name] = pygame.mixer.Sound(path)
        else:
            print(f"[Audio Warning] Звук не знайдено: {path}")
            self.sounds[name] = None

    def _load_all(self) -> None:
        """Завантажує всі необхідні ассети гри."""
        self._load("move", "move.wav")
        self._load("rotate", "rotate.wav")
        self._load("drop", "drop.wav")
        self._load("hard_drop", "hard_drop.wav")
        self._load("clear", "clear.wav")
        self._load("hold", "hold.wav")
        self._load("game_over", "game_over.wav")

    def play(self, name: str) -> None:
        """Безпечно відтворює звук за його іменем."""
        sound = self.sounds.get(name)
        if sound:
            sound.play()