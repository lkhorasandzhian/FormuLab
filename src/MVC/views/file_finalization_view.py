import tkinter as tk
from tkinter import scrolledtext


class FileFinalizationView(tk.Frame):
    def __init__(self, controller, tex_content):
        super().__init__(controller.app.root)
        self.controller = controller
        self.tex_content = tex_content
        self.is_table_of_contents_included = tk.BooleanVar()
        self.is_headers_numeration_included = tk.BooleanVar()
        self.show_screen()

    def show_screen(self):
        self.controller.app.root.title("FormuLab")

        tk.Label(self, text="Доработка файла", font=("Arial", 14)).pack(pady=20)
        tk.Checkbutton(self, text="Добавить оглавление", variable=self.is_table_of_contents_included).pack(anchor="w")
        tk.Checkbutton(self, text="Добавить нумерацию заголовков", variable=self.is_headers_numeration_included).pack(anchor="w")

        # Readonly-предпросмотр полученного предварительного файла tex.
        tk.Label(self, text="Предпросмотр .tex файла:").pack(pady=10)
        preview = scrolledtext.ScrolledText(self, height=15, wrap=tk.WORD, font=("Courier", 10))
        preview.insert(tk.END, self.tex_content)
        preview.config(state=tk.DISABLED)
        preview.pack(expand=True, fill="both", padx=10, pady=10)

        tk.Button(self, text="Скачать файл", command=self.controller.finalize_file).pack(pady=10)
        tk.Button(self, text="Назад", command=self.controller.back).pack(pady=10)