#!/usr/bin/env bash
set -e

# Скрипт сборки и переименования для проекта FormuLab.
# Запускается из корня проекта (где находится папка src и .venv).

# Очистка предыдущих сборок.
rm -rf build dist

# Создание каталога для логов.
mkdir -p logs

# Использование Python из виртуального окружения напрямую.
echo "Запуск PyInstaller..."
"${PWD}/.venv/Scripts/python" -m PyInstaller --onefile --paths="${PWD}" src/main.py > logs/pyinstaller_build.log 2>&1
echo "Лог сборки сохранен в logs/pyinstaller_build.log"

# Переименовывание исполняемого файла.
echo "Переименование исполняемого файла main.exe в FormuLab.exe..."
if [ -f "dist/main.exe" ]; then
  mv "dist/main.exe" "dist/FormuLab.exe"
  echo "Готово: dist/FormuLab.exe"
else
  echo "Ошибка: dist/main.exe не найден. Необходимо проверить сборку." >&2
  exit 1
fi
