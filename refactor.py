import os
import re
import shutil

MAPPING = {
    "settings": "src.config.settings",
    "states": "src.core.states",
    "game": "src.core.game",
    "board": "src.core.board",
    "piece": "src.entities.piece",
    "piece_factory": "src.entities.piece_factory",
    "tetrominoes": "src.entities.tetrominoes",
    "renderer": "src.ui.renderer",
    "sound_manager": "src.managers.sound_manager",
    "data_manager": "src.managers.data_manager",
    "input_handler": "src.managers.input_handler",
}

def update_imports(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    for old_mod, new_mod in MAPPING.items():
        # import old_mod -> from src.path import old_mod
        pattern1 = r'^import\s+' + old_mod + r'(?=\s|$)'
        repl1 = r'from ' + new_mod.rsplit('.', 1)[0] + r' import ' + old_mod
        content = re.sub(pattern1, repl1, content, flags=re.MULTILINE)
        
        # from old_mod import X -> from new_mod import X
        pattern2 = r'^from\s+' + old_mod + r'\s+import\s+'
        repl2 = r'from ' + new_mod + r' import '
        content = re.sub(pattern2, repl2, content, flags=re.MULTILINE)
        
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

FILES_TO_MOVE = {
    "settings.py": "src/config/settings.py",
    "states.py": "src/core/states.py",
    "game.py": "src/core/game.py",
    "board.py": "src/core/board.py",
    "piece.py": "src/entities/piece.py",
    "piece_factory.py": "src/entities/piece_factory.py",
    "tetrominoes.py": "src/entities/tetrominoes.py",
    "renderer.py": "src/ui/renderer.py",
    "sound_manager.py": "src/managers/sound_manager.py",
    "data_manager.py": "src/managers/data_manager.py",
    "input_handler.py": "src/managers/input_handler.py",
}

# Fix data_manager.py
dm_path = "data_manager.py"
if os.path.exists(dm_path):
    with open(dm_path, "r", encoding="utf-8") as f:
        dm_content = f.read()
    dm_content = dm_content.replace(
        "base_path = os.path.dirname(os.path.abspath(__file__))",
        "base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))"
    )
    with open(dm_path, "w", encoding="utf-8") as f:
        f.write(dm_content)

py_files = list(FILES_TO_MOVE.keys()) + ["main.py"]
for f in py_files:
    if os.path.exists(f):
        update_imports(f)

for src_f, dest_f in FILES_TO_MOVE.items():
    if os.path.exists(src_f):
        os.makedirs(os.path.dirname(dest_f), exist_ok=True)
        shutil.move(src_f, dest_f)

print("Files successfully moved and imports updated.")
