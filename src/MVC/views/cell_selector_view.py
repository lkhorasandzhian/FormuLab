import tkinter as tk


class CellSelectorView(tk.Frame):
    def __init__(self, controller, cells):
        super().__init__(controller.app.root)
        self.controller = controller
        self.cell_vars = []
        self.canvas = None
        self.show_screen(cells)

    def show_screen(self, cells):
        self.controller.app.root.title("FormuLab")
        self.pack(fill=tk.BOTH, expand=True)

        header = tk.Label(self, text="Выберите ячейки для конвертации", font=("Arial", 14))
        header.pack(pady=10, anchor="n")

        # Создаем фрейм для прокручиваемого списка.
        list_frame = tk.Frame(self)
        list_frame.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(list_frame)
        # Глобальный обработчик колёсика для прокрутки всего списка.
        self.canvas.bind_all("<MouseWheel>", self._on_canvas_mousewheel)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(list_frame, orient="vertical", command=self.canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas.config(yscrollcommand=scrollbar.set)

        scrollable_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        # Добавляем поля для ячеек.
        for i, cell in enumerate(cells):
            var = tk.BooleanVar()
            self.cell_vars.append(var)
            cell_type = cell['cell_type']
            content = cell['source']
            cell_frame = tk.Frame(scrollable_frame)
            cell_frame.pack(fill=tk.X, pady=5)

            # Создаем фрейм для текстового поля и его прокручиваемого ползунка.
            text_frame = tk.Frame(cell_frame)
            text_frame.pack(fill=tk.X)

            # Создаем readonly текстовое поле для каждой ячейки.
            text_widget = tk.Text(text_frame, height=5, width=80, wrap=tk.WORD,
                                  bg="white", fg="black", font=("Arial", 10))
            text_widget.insert(tk.END, f"{i + 1}: [{cell_type}] {content}")
            text_widget.config(state=tk.DISABLED)
            text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

            # Обработчик колёсика для текстового поля.
            # При прокрутке внутри ячейки событие не всплывает к канвасу.
            text_widget.bind("<MouseWheel>", self._on_text_mousewheel)

            # Прокручиваемый ползунок для текстового поля.
            scrollbar_inner = tk.Scrollbar(text_frame, orient="vertical", command=text_widget.yview)
            scrollbar_inner.pack(side=tk.RIGHT, fill=tk.Y)
            text_widget.config(yscrollcommand=scrollbar_inner.set)

            # Добавляем чекбокс.
            tk.Checkbutton(cell_frame, text=f"Выбрать {i + 1}", variable=var).pack(anchor="w", pady=2)

        # Обновляем размер canvas после добавления элементов.
        scrollable_frame.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

        # Фрейм для кнопок.
        button_frame = tk.Frame(self)
        button_frame.pack(fill=tk.X, side=tk.BOTTOM)

        # Кнопки по центру.
        tk.Button(button_frame, text="Выделить все", command=self.select_all).pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(button_frame, text="Снять выделение", command=self.deselect_all).pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(button_frame, text="Конвертировать", command=self.controller.convert).pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(button_frame, text="Назад", command=self.controller.back).pack(side=tk.LEFT, padx=5, pady=5)

    def highlight_code(self, text_widget, code):
        pass

    def select_all(self):
        for var in self.cell_vars:
            var.set(True)

    def deselect_all(self):
        for var in self.cell_vars:
            var.set(False)

    def get_selected_indices(self):
        return [i for i, var in enumerate(self.cell_vars) if var.get()]

    # noinspection PyMethodMayBeStatic
    def _on_text_mousewheel(self, event):
        """Обработчик колёсика для прокрутки содержимого конкретного текстового поля.
        Возвращает 'break', чтобы событие не распространилось на глобальный обработчик.
        """
        event.widget.yview_scroll(int(-1 * (event.delta / 120)), "units")
        return "break"

    def _on_canvas_mousewheel(self, event):
        """Глобальный обработчик колёсика для прокрутки всего списка ячеек.
        Он срабатывает, если событие не было перехвачено более специфичным обработчиком.
        """
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")