#!/usr/bin/env bash
set -e

# Скрипт сборки и переименования для проекта FormuLab.
# Запускается из корня проекта (где лежат src/, .venv/ и pandoc-full/).

# Очистка предыдущих сборок.
rm -rf build dist

# Создание каталога для логов.
mkdir -p logs

ICON_PATH="assets/logo.ico"

echo "Запуск PyInstaller..."
pyinstaller \
  --clean \
  --windowed \
  --name FormuLab \
  --icon "$ICON_PATH" \
  --noupx \
  --collect-all nbconvert \
  --collect-all jupyter_core \
  --collect-all jupyter_client \
  --add-data ".venv\\share\\jupyter;share/jupyter" \
  --add-data "$ICON_PATH;assets" \
  src/main.py                                    \
  > logs/pyinstaller_build.log 2>&1

echo "Лог сборки сохранён в logs/pyinstaller_build.log"

echo "Готово: dist/FormuLab/FormuLab.exe"