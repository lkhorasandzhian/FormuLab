import os
import re
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
            # Шаг 1: сохранение изображений на ПК в отдельной папке.
            self.__save_images(img_folder)

            # Шаг 2: переименовывание файлов в latex-коде.
            self.__rename_files_in_latex_code()

            # Шаг 3: обновление путей в tex-контенте, добавляя папку перед названием файла.
            self.__add_image_folder_info(folder_name)

        with open(file_path, "w", encoding="utf-8") as f:
                f.write(self.final_tex_content)

    def __save_images(self, output_dir):
        """
        Сохраняет все извлеченные картинки в указанную папку.
        """
        if not self.ipynb_images:
            return
        os.makedirs(output_dir, exist_ok=True)
        i = 0
        for filename, data in self.ipynb_images.items():
            i += 1
            with open(os.path.join(output_dir, f'image_{i}.png'), 'wb') as f:
                f.write(data)

    def __rename_files_in_latex_code(self):
        r"""
        Переименовывает файлы в latex-коде.

        Случай 1:
          \\adjustimage{...}{old.png} ->

          \\adjustimage{...}{image_1.png}
        Случай 2:
          \\pandocbounded{\\includegraphics[...] {old.png}} ->

          \\pandocbounded{\\includegraphics[...] {image_1.png}}
        """
        # Случай 1: переименование adjustimage.
        adjust_counter = 0
        def repl_adjust(match):
            nonlocal adjust_counter
            adjust_counter += 1
            orig = match.group(2)
            _, ext = os.path.splitext(orig)
            return match.group(1) + "{" + f"image_{adjust_counter}{ext}" + "}"
        pattern_adjust = r'(\\adjustimage\{(?:[^{}]|\{[^{}]*\})*\})\{([^}]+)\}'
        self.final_tex_content = re.sub(pattern_adjust, repl_adjust, self.final_tex_content)

        # Случай 2: переименование pandocbounded с includegraphics.
        pandoc_counter = 0
        def repl_pandoc(match):
            nonlocal pandoc_counter
            pandoc_counter += 1
            orig = match.group(2)
            _, ext = os.path.splitext(orig)
            return match.group(1) + f"image_{pandoc_counter}{ext}" + "}"
        pattern_pandoc = r'(\\pandocbounded\{\\includegraphics\[[^\]]*\]\{)([^}]+)\}'
        self.final_tex_content = re.sub(pattern_pandoc, repl_pandoc, self.final_tex_content)

    def __add_image_folder_info(self, folder_name):
        r"""
        Добавляет префикс папки к путям изображений в tex-контенте.

        Случай 1:
          \\adjustimage{...}{image_1.png} ->

          \\adjustimage{...}{folder_name/image_1.png}
        Случай 2:
          \\pandocbounded{\\includegraphics[...]{image_1.png}} ->

          \\pandocbounded{\\includegraphics[...]{folder_name/image_1.png}}
        """

        # Случай 1: обработка adjustimage.
        pattern = r'(\\adjustimage\{(?:[^{}]|\{[^{}]*\})*\})\{([^}]+)\}'
        replacement = r"\1{" + folder_name + r"/\2}"
        self.final_tex_content = re.sub(pattern, replacement, self.final_tex_content)

        # Случай 2: обработка pandocbounded + includegraphics.
        pattern2 = r'(\\pandocbounded\{\\includegraphics\[[^\]]*\]\{)([^}]+)\}'
        replacement2 = r"\1" + folder_name + r"/\2}"
        self.final_tex_content = re.sub(pattern2, replacement2, self.final_tex_content)

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