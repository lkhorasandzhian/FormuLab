import os
import sys
import tkinter as tk
import warnings

from nbformat.warnings import MissingIDFieldWarning

from src.formulab_application import FormuLabApplication

def resource_path(rel_path):
    """Возвращает корректный путь к файлу как в режиме dev, так и в упакованном exe."""
    # Проверка на запуск release-версии.
    if hasattr(sys, "_MEIPASS"):
        # PyInstaller распаковал ресурсы сюда.
        # noinspection PyProtectedMember
        return os.path.join(sys._MEIPASS, rel_path)
    # В режиме разработки поднимаемся на один уровень вверх (из папки src/ в корень проекта).
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, rel_path)

# Запуск приложения.
if __name__ == "__main__":
    import subprocess
    from src.utils.windows_subprocess import popen_hidden
    subprocess.Popen = popen_hidden

    warnings.filterwarnings("ignore", category=MissingIDFieldWarning)
    warnings.filterwarnings("ignore", message="IPython3 lexer unavailable, falling back on Python 3")
    root = tk.Tk()
    # Устанавливаем иконку окна.
    icon_file = resource_path("assets\logo.ico")
    # noinspection PyBroadException
    try:
        # для Windows.
        root.iconbitmap(icon_file)
    except Exception:
        # fallback (например, если iconbitmap не сработал).
        img = tk.PhotoImage(file=icon_file)
        root.iconphoto(False, img)
    app = FormuLabApplication(root)
    app.launch()