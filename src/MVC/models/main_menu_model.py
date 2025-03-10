import nbformat
import os


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

    def load_notebooks_from_folder(self, folder_path):
        """Загружает все .ipynb файлы из папки и объединяет их в один notebook."""
        all_notebook_data = []
        for filename in os.listdir(folder_path):
            if filename.endswith('.ipynb'):
                file_path = os.path.join(folder_path, filename)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        notebook_data = nbformat.read(f, as_version=4)
                        all_notebook_data.append(notebook_data)
                except Exception as e:
                    raise Exception(f"Ошибка при загрузке файла {filename}: {e}")

        if not all_notebook_data:
            raise Exception("Нет файлов .ipynb в выбранной папке.")

        self.notebook_data = self.__combine_notebooks(all_notebook_data)
        self.file_path = folder_path

    @staticmethod
    def __combine_notebooks(notebook_data_list):
        """Объединяет ячейки всех ноутбуков в один."""
        combined_notebook = nbformat.v4.new_notebook()
        all_cells = []
        for notebook_data in notebook_data_list:
            all_cells.extend(notebook_data['cells'])
        combined_notebook.cells = all_cells
        return combined_notebook