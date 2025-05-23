import nbformat
import os

from src.utils.formulab_exceptions import EmptyIpynbFileException


class MainMenuModel:
    def __init__(self):
        self.file_path = None
        self.notebook_data = None

    def load_ipynb_file(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                self.notebook_data = nbformat.read(f, as_version=4)
        except Exception as e:
            raise Exception(f"Ошибка загрузки файла: {e}")

        # Проверка на наличие ячеек в загруженном файле.
        if not self.notebook_data.get('cells'):
            raise EmptyIpynbFileException()

        self.file_path = file_path

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

        # Проверка на наличие ячеек в загруженном файле.
        if not self.notebook_data.get('cells'):
            raise EmptyIpynbFileException(message="Папка содержит только пустые ipynb-файлы. В них нет ни одной ячейки. "
                                                  "Выберите папку, содержащую хотя бы один непустой ipynb-файл")

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