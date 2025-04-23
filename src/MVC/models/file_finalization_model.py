import os
from tkinter import filedialog

from src.utils.formulab_exceptions import FileNotSelectedException


class FileFinalizationModel:
    def __init__(self, intermediate_tex_content, ipynb_images):
        self.intermediate_tex_content = intermediate_tex_content
        self.ipynb_images = ipynb_images
        self.final_tex_content = None

    def refine_file(self, include_toc=False, include_headers_numeration=False):
        """Дорабатывает tex-файл на основе выбранных опций."""
        self.final_tex_content = self.intermediate_tex_content

        if include_toc:
            self.__add_table_of_contents()

        if include_headers_numeration:
            self.__add_header_numeration()

        # Случай, при котором необходимо принудительно включить ненумерованные заголовки в оглавление.
        if include_toc and not include_headers_numeration:
            self.__add_not_numbered_headers_to_toc()

    def save_file(self):
        """Сохраняет доработанный tex-файл."""
        if self.final_tex_content is None:
            raise ValueError("Нет содержимого для сохранения.")

        file_path = filedialog.asksaveasfilename(defaultextension=".tex", filetypes=[("LaTeX files", "*.tex")])

        if not file_path:
            raise FileNotSelectedException()

        # Определение папки для картинок рядом с tex-файлом.
        base, _ = os.path.splitext(os.path.basename(file_path))
        folder_name = f"{base}_FormuLab_images"
        img_folder = os.path.join(os.path.dirname(file_path), folder_name)

        # Сохранение изображений в отдельной папке, если они есть.
        if self.ipynb_images:
            self.save_images(img_folder)

        with open(file_path, "w", encoding="utf-8") as f:
                f.write(self.final_tex_content)

    def save_images(self, output_dir):
        """
        Сохраняет все извлеченные картинки в указанную папку.
        """
        if not self.ipynb_images:
            return
        os.makedirs(output_dir, exist_ok=True)
        for filename, data in self.ipynb_images.items():
            with open(os.path.join(output_dir, filename), 'wb') as f:
                f.write(data)

    def __add_table_of_contents(self):
        """Добавляет оглавление в tex-файл."""
        self.final_tex_content = self.final_tex_content.replace(
            "\\begin{document}",
            "\\begin{document}\n\\tableofcontents",
            1
        )

    def __add_header_numeration(self):
        """Добавляет нумерацию заголовков h1, h2, h3 в tex-файл."""
        # Разбиваем исходный tex-файл построчно.
        tex_lines = self.final_tex_content.split("\n")

        # Убираем * из \section*, \subsection*, \subsubsection* для возврата нумерации заголовков h1, h2, h3.
        tex_lines = [
            line if not any(
                line.strip().startswith(command) for command in ["\\section", "\\subsection", "\\subsubsection"])
            else line.replace("\\section*", "\\section").replace("\\subsection*", "\\subsection").replace(
                "\\subsubsection*", "\\subsubsection")
            for line in tex_lines
        ]

        self.final_tex_content = "\n".join(tex_lines)

    def __add_not_numbered_headers_to_toc(self):
        """Добавляет ненумерованные заголовки в оглавление."""
        tex_lines = self.final_tex_content.split("\n")
        new_tex_lines = []

        for i, line in enumerate(tex_lines):
            # Проверяем, начинается ли строка с ненумерованного заголовка.
            if line.strip().startswith(("\\section*{", "\\subsection*{", "\\subsubsection*{")):
                # Определяем уровень заголовка.
                if line.strip().startswith("\\section*{"):
                    level = "section"
                elif line.strip().startswith("\\subsection*{"):
                    level = "subsection"
                else:
                    level = "subsubsection"

                # Извлекаем название заголовка (может быть на одной или нескольких строках).
                header_content = line.split("{", 1)[1] if "{" in line else ""
                if not header_content.endswith("}"):
                    for j in range(i + 1, len(tex_lines)):
                        header_content += tex_lines[j].strip()
                        if tex_lines[j].strip().endswith("}"):
                            break
                header_content = header_content.rstrip("}")

                # Добавляем строку для оглавления ПЕРЕД самой строкой с заголовком.
                new_tex_lines.append(f"\\addcontentsline{{toc}}{{{level}}}{{{header_content}}}")

            # Добавляем саму строку с заголовком.
            new_tex_lines.append(line)

        self.final_tex_content = "\n".join(new_tex_lines)