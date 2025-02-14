from src.MVC.controllers.main_menu_controller import MainMenuController
from src.MVC.controllers.cell_selector_controller import CellSelectorController


class FormuLabApplication:
    def __init__(self, root):
        self.root = root

        width = self.root.winfo_screenwidth()
        height = self.root.winfo_screenheight()
        self.root.geometry("%dx%d" % (width, height))

        self.current_controller = MainMenuController(self)

    def show_main_menu(self):
        # Переход к главному меню.
        if isinstance(self.current_controller, CellSelectorController):
            self.current_controller.view.pack_forget()
        self.current_controller = MainMenuController(self)
        self.current_controller.view.pack()

    def show_cell_selector(self):
        # Переход к экрану выбора ячеек.
        if isinstance(self.current_controller, MainMenuController):
            self.current_controller.view.pack_forget()

        # Создаем контроллер для выбора ячеек с необходимыми данными.
        file_path = self.current_controller.model.file_path
        notebook_data = self.current_controller.model.notebook_data
        self.current_controller = CellSelectorController(self, file_path, notebook_data)
        self.current_controller.view.pack()

    def launch(self):
        self.show_main_menu()  # Показать главное меню при запуске.
        self.root.mainloop()