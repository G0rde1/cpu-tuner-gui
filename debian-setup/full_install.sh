#!/bin/bash
# Полная установка CPU Tuner GUI на Debian

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${BLUE}════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}🖥️  CPU Tuner GUI - Полная установка для Debian${NC}"
echo -e "${BLUE}════════════════════════════════════════════════════════${NC}"

# Проверка прав
if [[ $EUID -ne 0 ]]; then
   echo -e "${RED}❌ Запустите с sudo: sudo ./full_install.sh${NC}"
   exit 1
fi

# 1. Обновление системы
echo -e "\n${GREEN}📦 Шаг 1/7: Обновление системы...${NC}"
apt update && apt upgrade -y

# 2. Установка Python и зависимостей
echo -e "\n${GREEN}📦 Шаг 2/7: Установка Python и пакетов...${NC}"
apt install -y python3 python3-pip python3-tk python3-psutil wget git

# 3. Установка lm-sensors (датчики температур)
echo -e "\n${GREEN}🌡️ Шаг 3/7: Установка lm-sensors...${NC}"
apt install -y lm-sensors
echo -e "${YELLOW}▶ Настройка датчиков...${NC}"
sensors-detect --auto

# 4. Скачивание приложения
echo -e "\n${GREEN}📥 Шаг 4/7: Скачивание приложения...${NC}"
cd /opt
if [ -d "cpu-tuner-gui" ]; then
    echo "Папка уже существует, обновляем..."
    rm -rf cpu-tuner-gui
fi
git clone https://github.com/G0rde1/cpu-tuner-gui.git
cd cpu-tuner-gui

# 5. Установка прав
echo -e "\n${GREEN}🔧 Шаг 5/7: Настройка прав...${NC}"
chmod +x cpu_tuner_gui.py
chmod +x install.sh

# 6. Создание глобальной команды
echo -e "\n${GREEN}🔗 Шаг 6/7: Создание глобальной команды...${NC}"
cat > /usr/local/bin/cpu-tuner << EOF
#!/bin/bash
cd /opt/cpu-tuner-gui
sudo python3 cpu_tuner_gui.py
EOF
chmod +x /usr/local/bin/cpu-tuner

# 7. Создание ярлыка на рабочем столе
echo -e "\n${GREEN}🖱️ Шаг 7/7: Создание ярлыка...${NC}"
cat > /usr/share/applications/cpu-tuner.desktop << EOF
[Desktop Entry]
Name=CPU Tuner
Comment=Управление процессором
Exec=gksudo python3 /opt/cpu-tuner-gui/cpu_tuner_gui.py
Icon=/opt/cpu-tuner-gui/icon.png
Terminal=false
Type=Application
Categories=System;Monitor;
EOF

echo -e "\n${GREEN}════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}✅ УСТАНОВКА ЗАВЕРШЕНА!${NC}"
echo -e "${BLUE}════════════════════════════════════════════════════════${NC}"
echo -e ""
echo -e "${YELLOW}▶ Запуск из терминала:${NC} sudo cpu-tuner"
echo -e "${YELLOW}▶ Или:${NC} cd /opt/cpu-tuner-gui && sudo python3 cpu_tuner_gui.py"
echo -e "${YELLOW}▶ Ярлык в меню:${NC} Система → CPU Tuner"
echo -e ""
echo -e "${RED}⚠️  ВНИМАНИЕ: Приложение требует права root!${NC}"
echo -e "${RED}   Запускайте через sudo или через меню (будет запрошен пароль)${NC}"
