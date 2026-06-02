#!/bin/bash
set -e

echo "==================================="
echo "🖥️  CPU Tuner GUI - Установка"
echo "==================================="

if [[ $EUID -ne 0 ]]; then
   echo "❌ Запустите с sudo: sudo ./install.sh"
   exit 1
fi

echo "📦 Обновление пакетов..."
apt update

echo "📦 Установка зависимостей..."
apt install -y python3 python3-tk python3-psutil lm-sensors

echo "🌡️ Настройка датчиков..."
sensors-detect --auto

echo "✅ Установка завершена!"
echo ""
echo "🚀 Запуск: sudo python3 cpu_tuner_gui.py"
