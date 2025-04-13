import os
from tkinter import filedialog, messagebox

from src.MVC.models.main_menu_model import MainMenuModel
from src.MVC.views.main_menu_view import MainMenuView
from src.utils.formulab_exceptions import EmptyIpynbFileException


class MainMenuController:
    def __init__(self, app):
        self.app = app
        self.model = MainMenuModel()
        self.view = MainMenuView(self)

    def load_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Jupyter Notebook Files", "*.ipynb"), ("All Files", "*.*")],
            title="Выберите .ipynb-файл"
        )

        if file_path:
            try:
                self.model.load_ipynb_file(file_path)
                self.app.show_cell_selector()
            except EmptyIpynbFileException as e:
                messagebox.showerror("Ошибка", str(e))
            except Exception as e:
                messagebox.showerror("Ошибка", str(e))

    def load_folder(self):
        folder_path = filedialog.askdirectory(
            title="Выберите папку с .ipynb-файлами",
            mustexist=True
        )

        if folder_path:
            try:
                self.model.load_notebooks_from_folder(folder_path)
                self.app.show_cell_selector()
            except Exception as e:
                messagebox.showerror("Ошибка", str(e))