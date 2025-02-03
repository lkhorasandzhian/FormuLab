import nbformat
from nbconvert import LatexExporter


class CellSelectorModel:
    def __init__(self, file_path, notebook_data):
        self.file_path = file_path
        self.notebook_data = notebook_data

    def get_cells(self):
        return self.notebook_data['cells'] if self.notebook_data else []

    def convert_to_tex(self, selected_indices):
        selected_cells = [self.notebook_data['cells'][i] for i in selected_indices]
        temp_notebook = nbformat.v4.new_notebook()
        temp_notebook.cells = selected_cells

        latex_exporter = LatexExporter()
        try:
            tex_content, _ = latex_exporter.from_notebook_node(temp_notebook)
            tex_content = CellSelectorModel.__validate_tex(tex_content)
            return tex_content
        except Exception as e:
            raise Exception(f"Ошибка экспорта в LaTeX: {e}")

    @staticmethod
    def __validate_tex(tex_content):
        tex_lines = tex_content.split("\n")
        tex_lines = CellSelectorModel.__add_russian_letters(tex_lines)
        tex_lines = CellSelectorModel.__comment_title(tex_lines)
        tex_lines = CellSelectorModel.__add_star_to_sections(tex_lines)
        return "\n".join(tex_lines)

    @staticmethod
    def __add_star_to_sections(tex_lines):
        """
        Сделать опциональным.
        :param tex_lines: list of lines with text format
        :return: tex lines with added stars
        """
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
    def __add_russian_letters(tex_lines):
        # Заголовки для поддержки русского языка.
        header_insert = (
            "\\usepackage[T2A]{fontenc}\n"
            "\\usepackage[utf8]{inputenc} % Для поддержки Unicode (UTF-8)\n"
            "\\usepackage[russian]{babel} % Подключение русского языка\n"
        )

        if tex_lines and tex_lines[0].startswith("\\documentclass"):
            tex_lines.insert(1, header_insert)

        return tex_lines