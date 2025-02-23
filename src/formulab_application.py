from src.MVC.controllers.main_menu_controller import MainMenuController
from src.MVC.controllers.cell_selector_controller import CellSelectorController
from src.MVC.controllers.file_finalization_controller import FileFinalizationController


class FormuLabApplication:
    def __init__(self, root):
        self.root = root

        # Текущий редактируемый файл Jupyter Notebook.
        self.editable_notebook_data = None

        width = self.root.winfo_screenwidth()
        height = self.root.winfo_screenheight()
        self.root.geometry("%dx%d" % (width, height))

        self.current_controller = MainMenuController(self)

    def show_main_menu(self):
        # Переход к главному меню.
        if isinstance(self.current_controller, (CellSelectorController, FileFinalizationController)):
            self.current_controller.view.pack_forget()
        self.current_controller = MainMenuController(self)
        self.current_controller.view.pack()

    def show_cell_selector(self):
        # Переход к экрану выбора ячеек.
        if isinstance(self.current_controller, (MainMenuController, FileFinalizationController)):
            self.current_controller.view.pack_forget()

        # Создаем контроллер для выбора ячеек с необходимыми данными.
        # Обновляем текущее состояние хранимого ноутбука в случае, если пользователь выбрал новый файл.
        if isinstance(self.current_controller, MainMenuController):
            self.editable_notebook_data = self.current_controller.model.notebook_data
        self.current_controller = CellSelectorController(self, self.editable_notebook_data)
        self.current_controller.view.pack()

    def show_file_finalization(self):
        # Переход к экрану доработки файла tex.
        if isinstance(self.current_controller, CellSelectorController):
            self.current_controller.view.pack_forget()

        # Создаем контроллер для доработки полученного файла tex.
        tex_content = self.current_controller.model.tex_content
        self.current_controller = FileFinalizationController(self, tex_content)
        self.current_controller.view.pack()

    def launch(self):
        self.show_main_menu()  # Показать главное меню при запуске.
        self.root.mainloop()