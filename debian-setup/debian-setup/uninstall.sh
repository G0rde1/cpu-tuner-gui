#!/bin/bash
# Удаление CPU Tuner GUI

RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

echo -e "${RED}🗑️  Удаление CPU Tuner GUI...${NC}"

if [[ $EUID -ne 0 ]]; then
   echo -e "${RED}❌ Запустите с sudo: sudo ./uninstall.sh${NC}"
   exit 1
fi

# Удаление глобальной команды
rm -f /usr/local/bin/cpu-tuner

# Удаление ярлыка
rm -f /usr/share/applications/cpu-tuner.desktop

# Удаление папки с программой
rm -rf /opt/cpu-tuner-gui

echo -e "${GREEN}✅ Удаление завершено!${NC}"
