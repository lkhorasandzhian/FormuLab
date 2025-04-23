from tkinter import messagebox

from src.MVC.models.file_finalization_model import FileFinalizationModel
from src.MVC.views.file_finalization_view import FileFinalizationView
from src.utils.formulab_exceptions import FileNotSelectedException


class FileFinalizationController:
    def __init__(self, app, intermediate_tex_content, ipynb_images):
        self.app = app
        self.model = FileFinalizationModel(intermediate_tex_content, ipynb_images)
        self.view = FileFinalizationView(self, intermediate_tex_content)

    def finalize_file(self):
        self.model.refine_file(
            include_toc=self.view.is_table_of_contents_included.get(),
            include_headers_numeration=self.view.is_headers_numeration_included.get()
        )  # Доработка файла с учётом пожеланий пользователя.

        try:
            self.model.save_file()  # Сохранение готового файла.
        except ValueError:
            # Ошибка, если файл не был доработан или нет содержимого.
            messagebox.showerror("Ошибка", "Не удалось сохранить файл: отсутствует содержимое для сохранения.")
            return
        except FileNotSelectedException:
            # Ошибка, если пользователь не выбрал файл для сохранения.
            messagebox.showwarning("Предупреждение", "Вы не выбрали место для сохранения.")
            return
        except Exception as e:
            # Обработка всех других ошибок.
            messagebox.showerror("Неизвестная ошибка", f"Произошла ошибка при сохранении файла: {e}")
            return

        self.app.show_main_menu()

    def back(self):
        self.app.show_cell_selector()