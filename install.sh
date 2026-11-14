#!/bin/bash

# -e: остановить выполнение при ошибке
# -x: выводить каждую команду в консоль перед выполнением
set -ex

# --- НАСТРОЙКИ ---
REPO_URL="https://github.com/mkspeaker/testbuild.git"
APT_PACKAGES="git portaudio19-dev ollama" 
# -----------------

echo "Обновление списка пакетов и установка системных зависимостей..."
sudo apt update
sudo apt install -y $APT_PACKAGES

echo "Клонирование репозитория..."
REPO_DIR=$(basename "$REPO_URL" .git)
git clone "$REPO_URL"
cd "$REPO_DIR"

echo "Создание виртуального окружения Python..."
python3 -m venv venv

echo "Активация окружения и установка зависимостей pip..."
source venv/bin/activate

pip install --upgrade pip
if [ -f "req.txt" ]; then
    pip install -r req.txt
else
    echo "Файл requirements.txt не найден, пропускаем установку pip-пакетов."
fi

echo "Готово!"
