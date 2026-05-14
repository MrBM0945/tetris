import json
import os
import sys
from datetime import datetime

class DataManager:
    """
    Клас для керування збереженнями та рекордами гри.
    """
    def __init__(self, filename="highscore.json"):
        self.filename = filename
        self.filepath = self._get_save_path()
        self.high_score_data = self.load_high_score()

    def _get_save_path(self):
        """Визначає шлях до файлу поруч із .exe або скриптом."""
        if getattr(sys, 'frozen', False):
            base_path = os.path.dirname(sys.executable)
        else:
            base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
        return os.path.join(base_path, self.filename)

    def load_high_score(self):
        """Завантажує рекорд із файлу."""
        if os.path.exists(self.filepath):
            try:
                with open(self.filepath, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                pass
        return {"score": 0, "date": "---"}

    def save_new_score(self, score):
        """Перевіряє та зберігає новий рекорд."""
        if score > self.high_score_data["score"]:
            self.high_score_data = {
                "score": score,
                "date": datetime.now().strftime("%d.%m.%Y %H:%M")
            }
            try:
                with open(self.filepath, 'w', encoding='utf-8') as f:
                    json.dump(self.high_score_data, f, indent=4, ensure_ascii=False)
                return True
            except IOError as e:
                print(f"Помилка збереження: {e}")
        return False