# FormuLab
Desktop-приложение для обработки текста, полученного nbconvert и содержащего формулы Latex

# Repository Structure

## Source Code Directory
`src/` - содержит исходный код приложения.

### Main Application Files
- `main.py` - Главный файл для запуска приложения.
- `formulab_application.py` - Файл приложения для навигации между окнами.

### Utility Files
`utils/` - содержит утилиты по работе с файлами.
- `__init__.py` - Инициализация пакета utils.
- `formulab_exceptions.py` - Специализированные исключения приложения FormuLab.
- `windows_subprocess.py` - Скрытие консольных окон дочерних процессов от основного процесса приложения FormuLab, а также патч для фонового запуска внешних утилит (например, `pandoc`) без мерцания терминала.

## MVC Structure
`MVC/` - Model-View-Controller архитектура для компонент приложения.

### Models
`models/` - компоненты моделей.
- `__init__.py` - Инициализация пакета models.
- `main_menu_model.py` - Модель главного меню.
- `cell_selector_model.py` - Модель выбора ячеек.
- `file_finalization_model.py` - Модель доработки файла.

### Views
`views/` - компоненты представления.
- `__init__.py` - Инициализация пакета views.
- `main_menu_view.py` - Представление главного меню.
- `cell_selector_view.py` - Представление выбора ячеек.
- `file_finalization_view.py` - Представление доработки файла.

### Controllers
`controllers/` - компоненты контроллеров.
- `__init__.py` - Инициализация пакета controllers.
- `main_menu_controller.py` - Контроллер главного меню.
- `cell_selector_controller.py` - Контроллер выбора ячеек.
- `file_finalization_controller.py` - Контроллер доработки файла.
