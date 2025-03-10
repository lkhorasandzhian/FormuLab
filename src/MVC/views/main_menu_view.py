import tkinter as tk


class MainMenuView(tk.Frame):
    def __init__(self, controller):
        super().__init__(controller.app.root)
        self.controller = controller
        self.show_screen()

    def show_screen(self):
        self.controller.app.root.title("FormuLab")

        tk.Label(self, text="Добро пожаловать в FormuLab!", font=("Arial", 14)).pack(pady=20)
        tk.Button(self, text="Загрузить ipynb-файл", command=self.controller.load_file).pack(pady=10)
        tk.Button(self, text="Загрузить папку, содержащую ipynb-файлы", command=self.controller.load_folder).pack(pady=10)
        tk.Button(self, text="Выход", command=self.quit).pack(pady=10)