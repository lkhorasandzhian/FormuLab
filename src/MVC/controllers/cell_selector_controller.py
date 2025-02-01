import os
from tkinter import messagebox, filedialog

from src.MVC.models.cell_selector_model import CellSelectorModel
from src.MVC.views.cell_selector_view import CellSelectorView


class CellSelectorController:
    def __init__(self, app, file_path, notebook_data):
        self.app = app
        self.model = CellSelectorModel(file_path, notebook_data)
        self.view = CellSelectorView(self, self.model.get_cells())

    def convert(self):
        selected_indices = self.view.get_selected_indices()
        if not selected_indices:
            messagebox.showwarning("Предупреждение", "Выберите хотя бы одну ячейку!")
            return

        try:
            tex_content = self.model.convert_to_tex(selected_indices)
            save_path = filedialog.asksaveasfilename(
                defaultextension=".tex",
                filetypes=[("LaTeX Files", "*.tex")],
                initialfile=os.path.splitext(os.path.basename(self.model.file_path))[0] + ".tex"
            )
            if save_path:
                with open(save_path, 'w', encoding='utf-8') as f:
                    f.write(tex_content)
                messagebox.showinfo("Успех", f"Файл сохранён: {save_path}")
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def back(self):
        self.app.show_main_menu()