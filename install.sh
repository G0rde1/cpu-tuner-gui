#!/bin/bash
# CPU Tuner - Установщик

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}🖥️  CPU Tuner - Установка${NC}"
echo -e "${BLUE}════════════════════════════════════════════════════════${NC}"

if [[ $EUID -ne 0 ]]; then
   echo -e "${RED}❌ Запустите с sudo: sudo ./install.sh${NC}"
   exit 1
fi

echo -e "\n${GREEN}📦 Обновление системы...${NC}"
apt update

echo -e "\n${GREEN}📦 Установка зависимостей...${NC}"
apt install -y python3 python3-tk python3-psutil lm-sensors

echo -e "\n${GREEN}🌡️ Настройка датчиков...${NC}"
sensors-detect --auto

echo -e "\n${GREEN}🔗 Создание глобальной команды...${NC}"
cat > /usr/local/bin/cpu-tuner << EOF
#!/bin/bash
cd /opt/cpu-tuner
sudo python3 cpu_tuner_gui.py
EOF
chmod +x /usr/local/bin/cpu-tuner

echo -e "\n${GREEN}════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}✅ УСТАНОВКА ЗАВЕРШЕНА!${NC}"
echo -e "${BLUE}════════════════════════════════════════════════════════${NC}"
echo -e ""
echo -e "${YELLOW}▶ Запуск:${NC} cpu-tuner"
echo -e "${YELLOW}▶ Или:${NC} cd /opt/cpu-tuner && sudo python3 cpu_tuner_gui.py"
echo -e ""
echo -e "${RED}⚠️  ВНИМАНИЕ: Запускайте с sudo!${NC}"
