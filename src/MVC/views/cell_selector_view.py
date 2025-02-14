import tkinter as tk


class CellSelectorView(tk.Frame):
    def __init__(self, controller, cells):
        super().__init__(controller.app.root)
        self.controller = controller
        self.cell_vars = []
        self.show_screen(cells)

    def show_screen(self, cells):
        self.controller.app.root.title("Выбор ячеек")

        tk.Label(self, text="Выберите ячейки для конвертации", font=("Arial", 14)).pack(pady=10)

        for i, cell in enumerate(cells):
            var = tk.BooleanVar()
            self.cell_vars.append(var)
            cell_type = cell['cell_type']
            content = cell['source'][:50] + ("..." if len(cell['source']) > 50 else "")
            tk.Checkbutton(self, text=f"{i + 1}: [{cell_type}] {content}", variable=var).pack(anchor="w")

        tk.Button(self, text="Выделить все", command=self.select_all).pack(pady=5)
        tk.Button(self, text="Снять выделение", command=self.deselect_all).pack(pady=5)
        tk.Button(self, text="Конвертировать", command=self.controller.convert).pack(pady=10)
        tk.Button(self, text="Назад", command=self.controller.back).pack(pady=10)

    def select_all(self):
        for var in self.cell_vars:
            var.set(True)

    def deselect_all(self):
        for var in self.cell_vars:
            var.set(False)

    def get_selected_indices(self):
        return [i for i, var in enumerate(self.cell_vars) if var.get()]