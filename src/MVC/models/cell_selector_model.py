import base64
import nbformat
from nbconvert import LatexExporter
from re import sub, DOTALL

from traitlets.config import Config


class CellSelectorModel:
    def __init__(self, notebook_data):
        self.notebook_data = notebook_data
        self.tex_content = None
        self.ipynb_images = {}

    def get_cells(self):
        return self.notebook_data['cells'] if self.notebook_data else []

    def convert_to_tex(self, selected_indices):
        # Нумерация в selected_indices идет с 1, а в notebook_data с 0.
        selected_cells = [self.notebook_data['cells'][i - 1] for i in selected_indices]
        temp_notebook = nbformat.v4.new_notebook()
        temp_notebook.cells = selected_cells

        self.__extract_images(selected_cells)

        c = Config()
        c.ExtractOutputPreprocessor.output_filename_template = "image_{index}{extension}"

        latex_exporter = LatexExporter(config=c)
        try:
            tex_content, _ = latex_exporter.from_notebook_node(temp_notebook)
            tex_content = CellSelectorModel.__validate_tex(tex_content)
            self.tex_content = tex_content
        except Exception as e:
            raise Exception(f"Ошибка экспорта в LaTeX: {e}")

    def __extract_images(self, cells):
        """
        Проходит по всем output- и attachment-данным ячеек,
        извлекает картинки и сохраняет их в self.ipynb_images.
        """
        counter = 1
        for cell in cells:
            # Из выходных данных ячеек.
            for output in cell.get('outputs', []):
                for mime, content in output.get('data', {}).items():
                    if mime.startswith('image/'):
                        ext = mime.split('/')[1]
                        img_data = base64.b64decode(content)
                        name = f'image_{counter}.{ext}'
                        self.ipynb_images[name] = img_data
                        counter += 1
            # Из attachment в markdown.
            for attachment in cell.get('attachments', {}).values():
                for mime, content in attachment.items():
                    if mime.startswith('image/'):
                        ext = mime.split('/')[1]
                        img_data = base64.b64decode(content)
                        name = f'attach_{counter}.{ext}'
                        self.ipynb_images[name] = img_data
                        counter += 1

    @staticmethod
    def __validate_tex(tex_content):
        tex_lines = tex_content.split("\n")
        tex_lines = CellSelectorModel.__add_required_libraries(tex_lines)
        tex_lines = CellSelectorModel.__comment_title(tex_lines)
        tex_lines = CellSelectorModel.__add_star_to_sections(tex_lines)
        tex_lines = CellSelectorModel.__remove_labels(tex_lines)
        tex_lines = CellSelectorModel.__handle_long_math_formulas(tex_lines)
        return "\n".join(tex_lines)

    @staticmethod
    def __add_star_to_sections(tex_lines):
        # Добавляем * к \section, \subsection, \subsubsection для отмены нумерации заголовков h1, h2, h3.
        tex_lines = [
            line if not any(
                line.strip().startswith(command) for command in ["\\section", "\\subsection", "\\subsubsection"])
            else line.replace("\\section", "\\section*").replace("\\subsection", "\\subsection*").replace(
                "\\subsubsection", "\\subsubsection*")
            for line in tex_lines
        ]
        return tex_lines

    @staticmethod
    def __comment_title(tex_lines):
        # Комментируем \maketitle, если он есть.
        tex_lines = [
            "% \\maketitle" if line.strip() == "\\maketitle" else line
            for line in tex_lines
        ]

        return tex_lines

    @staticmethod
    def __add_required_libraries(tex_lines):
        header_insert = (
            # Заголовки для поддержки русского языка.
            "\\usepackage[T2A]{fontenc}\n"
            "\\usepackage[utf8]{inputenc} % Для поддержки Unicode (UTF-8)\n"
            "\\usepackage[russian]{babel} % Подключение русского языка\n"
            # Поддержка валидного отображения длинных математических формул.
            "\\usepackage{breqn}\n"
        )

        if tex_lines and tex_lines[0].startswith("\\documentclass"):
            tex_lines.insert(1, header_insert)

        return tex_lines

    @staticmethod
    def __remove_labels(tex_lines):
        # Используем регулярное выражение для удаления \label{...}.
        tex_lines = [
            sub(r'\\label\{.*?}', '', line)  # Заменяем \label{...} на пустую строку.
            for line in tex_lines
        ]
        return tex_lines

    @staticmethod
    def __handle_long_math_formulas(tex_lines):
        """
        Ищет блоки формул, оформленные как $\displaystyle ...$, и если их содержимое превышает заданный порог,
        заменяет их на окружение display math (например, dmath* из пакета breqn), которое обеспечивает
        автоматический перенос строк.
        """
        threshold = 200  # Пороговое значение длины математической формулы.
        tex_str = "\n".join(tex_lines)

        def replace_inline_math(match):
            content = match.group(1).strip()
            if len(content) > threshold:
                # Меняем на окружение dmath* для автоматического переноса длинных формул.
                return "\\begin{dmath*}\n" + content + "\n\\end{dmath*}"
            else:
                # Оставляем как есть.
                return match.group(0)

        # Ищем конструкции вида $\displaystyle ...$.
        tex_str = sub(r'\$\\displaystyle\s*(.*?)\$', replace_inline_math, tex_str, flags=DOTALL)
        return tex_str.split("\n")