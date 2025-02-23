from tkinter import messagebox

from src.MVC.models.cell_selector_model import CellSelectorModel
from src.MVC.views.cell_selector_view import CellSelectorView


class CellSelectorController:
    def __init__(self, app, notebook_data):
        self.app = app
        self.model = CellSelectorModel(notebook_data)
        self.view = CellSelectorView(self, self.model.get_cells())

    def convert(self):
        selected_indices = self.view.get_selected_indices()
        if not selected_indices:
            messagebox.showwarning("Предупреждение", "Выберите хотя бы одну ячейку!")
            return

        try:
            self.model.convert_to_tex(selected_indices)
            self.app.show_file_finalization()
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def back(self):
        self.app.show_main_menu()