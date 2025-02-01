from src.MVC.controllers.main_menu_controller import MainMenuController
from src.MVC.controllers.cell_selector_controller import CellSelectorController


class FormuLabApplication:
    def __init__(self, root):
        self.root = root
        self.root.withdraw()
        self.current_controller = MainMenuController(self)

    def show_main_menu(self):
        self.current_controller.view.destroy()
        self.current_controller = MainMenuController(self)

    def show_cell_selector(self):
        if not isinstance(self.current_controller, MainMenuController):
            raise TypeError
        self.current_controller.view.destroy()
        file_path = self.current_controller.model.file_path
        notebook_data = self.current_controller.model.notebook_data
        self.current_controller = CellSelectorController(self, file_path, notebook_data)

    def launch(self):
        self.root.mainloop()