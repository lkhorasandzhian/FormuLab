import tkinter as tk


class CellSelectorView(tk.Frame):
    def __init__(self, controller, cells):
        super().__init__(controller.app.root)
        self.controller = controller
        self.cell_vars = dict()  # Словарь состояний чекбоксов. Ключ — номер ячейки, значение — состояние чекбокса.
        self.canvas = None
        self.cells = cells  # Все ячейки.
        self.PAGE_SIZE = 250  # Количество ячеек на одной странице.
        self.current_page = 0  # Текущая страница.
        self.TOTAL_PAGES = len(self.cells) // self.PAGE_SIZE + 1  # Общее количество страниц.
        self.show_current_page(self.current_page)  # Показываем первую страницу.

    def show_current_page(self, page_number):
        """Загружаем и отображаем ячейки для текущей страницы."""
        # Вычисление начала и конца диапазона ячеек для текущей страницы.
        start = page_number * self.PAGE_SIZE
        end = start + self.PAGE_SIZE
        page_cells = self.cells[start:end]  # Ячейки для текущей страницы.

        # Обновляем интерфейс.
        self.clear_frame()  # Очищаем текущий экран.

        self.controller.app.root.title("FormuLab")
        self.pack(fill=tk.BOTH, expand=True)

        header = tk.Label(self, text=f"Выберите ячейки для конвертации (стр. {page_number + 1}/{self.TOTAL_PAGES})", font=("Arial", 14))
        header.pack(pady=10, anchor="n")

        self.show_cells(page_cells, page_number)  # Отображаем ячейки для текущей страницы.
        self.update_navigation_buttons(page_number)  # Обновляем кнопки навигации.

    def show_cells(self, page_cells, page_number):
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
        for i, cell in enumerate(page_cells):
            current_cell_index = (page_number * self.PAGE_SIZE) + i + 1
            if current_cell_index not in self.cell_vars:
                var = tk.BooleanVar()
                self.cell_vars[current_cell_index] = var
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
            text_widget.insert(tk.END, f"{current_cell_index}: [{cell_type}] {content}")
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
            tk.Checkbutton(cell_frame, text=f"Выбрать {current_cell_index}", variable=self.cell_vars[current_cell_index]).pack(anchor="w", pady=2)

        # Обновляем размер canvas после добавления элементов.
        scrollable_frame.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def update_navigation_buttons(self, page_number):
        """Обновляем кнопки навигации в зависимости от текущей страницы."""
        # Фрейм для кнопок.
        button_frame = tk.Frame(self)
        button_frame.pack(fill=tk.X, side=tk.BOTTOM)

        # Кнопка "Выделить все" и "Снять выделение" отображаются всегда.
        tk.Button(button_frame, text="Выделить все", command=self.select_all).pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(button_frame, text="Снять выделение", command=self.deselect_all).pack(side=tk.LEFT, padx=5, pady=5)

        # Для последней страницы отображать кнопку "Конвертировать", в остальных случаях — "Далее".
        if (page_number + 1) * self.PAGE_SIZE < len(self.cells):
            tk.Button(button_frame, text="Далее", command=self.next_page).pack(side=tk.LEFT, padx=5, pady=5)
        else:
            tk.Button(button_frame, text="Конвертировать", command=self.controller.convert).pack(side=tk.LEFT, padx=5, pady=5)

        # Для первой страницы отображать кнопку "Отмена", в остальных случаях — "Назад".
        if page_number > 0:
            tk.Button(button_frame, text="Назад", command=self.previous_page).pack(side=tk.LEFT, padx=5, pady=5)
        else:
            tk.Button(button_frame, text="Отмена", command=self.controller.back).pack(side=tk.LEFT, padx=5, pady=5)

    def highlight_code(self, text_widget, code):
        pass

    def clear_frame(self):
        """Очистить экран перед отображением новых ячеек."""
        for widget in self.winfo_children():
            widget.destroy()

    def select_all(self):
        for var in self.cell_vars.values():
            var.set(True)

    def deselect_all(self):
        for var in self.cell_vars.values():
            var.set(False)

    def next_page(self):
        """Перейти на следующую страницу."""
        self.current_page += 1
        self.show_current_page(self.current_page)

    def previous_page(self):
        """Перейти на предыдущую страницу."""
        self.current_page -= 1
        self.show_current_page(self.current_page)

    def get_selected_indices(self):
        return [cell_index for cell_index, cell_status in self.cell_vars.items() if cell_status.get()]

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