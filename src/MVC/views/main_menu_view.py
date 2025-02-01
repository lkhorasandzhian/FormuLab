import tkinter as tk


class MainMenuView(tk.Toplevel):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.show_screen()

    def show_screen(self):
        self.title("FormuLab")

        width = self.winfo_screenwidth()
        height = self.winfo_screenheight()
        self.geometry("%dx%d" % (width, height))

        tk.Label(self, text="Добро пожаловать в FormuLab!", font=("Arial", 14)).pack(pady=20)
        tk.Button(self, text="Загрузить ipynb-файл", command=self.controller.load_file).pack(pady=10)
        tk.Button(self, text="Выход", command=self.quit).pack(pady=10)