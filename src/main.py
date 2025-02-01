import tkinter as tk

from src.formulab_application import FormuLabApplication

# Запуск приложения.
if __name__ == "__main__":
    root = tk.Tk()
    app = FormuLabApplication(root)
    app.launch()