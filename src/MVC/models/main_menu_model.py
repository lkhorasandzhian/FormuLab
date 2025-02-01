import nbformat


class MainMenuModel:
    def __init__(self):
        self.file_path = None
        self.notebook_data = None

    def load_ipynb_file(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                self.notebook_data = nbformat.read(f, as_version=4)
            self.file_path = file_path
        except Exception as e:
            raise Exception(f"Ошибка загрузки файла: {e}")