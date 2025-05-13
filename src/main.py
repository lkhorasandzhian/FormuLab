import tkinter as tk
import warnings

from nbformat.warnings import MissingIDFieldWarning

from src.formulab_application import FormuLabApplication

# Запуск приложения.
if __name__ == "__main__":
    import subprocess
    from src.utils.windows_subprocess import popen_hidden
    subprocess.Popen = popen_hidden

    warnings.filterwarnings("ignore", category=MissingIDFieldWarning)
    warnings.filterwarnings("ignore", message="IPython3 lexer unavailable, falling back on Python 3")
    root = tk.Tk()
    app = FormuLabApplication(root)
    app.launch()