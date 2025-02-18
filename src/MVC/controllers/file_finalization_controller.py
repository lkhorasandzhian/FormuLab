from src.MVC.models.file_finalization_model import FileFinalizationModel
from src.MVC.views.file_finalization_view import FileFinalizationView


class FileFinalizationController:
    def __init__(self, app, intermediate_tex_content):
        self.app = app
        self.model = FileFinalizationModel(intermediate_tex_content)
        self.view = FileFinalizationView(self, intermediate_tex_content)

    def finalize_file(self):
        self.model.refine_file(
            include_toc=self.view.is_table_of_contents_included.get(),
            include_headers_numeration=self.view.is_headers_numeration_included.get()
        )                           # Доработка файла с учётом пожеланий пользователя.
        self.model.download_file()  # Скачивание готового файла.
        self.app.show_main_menu()

    def back(self):
        self.app.show_cell_selector()