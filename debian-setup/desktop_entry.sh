#!/bin/bash
# Создание ярлыка на рабочем столе

if [[ $EUID -ne 0 ]]; then
   echo "Запустите с sudo: sudo ./desktop_entry.sh"
   exit 1
fi

cat > /usr/share/applications/cpu-tuner.desktop << EOF
[Desktop Entry]
Name=CPU Tuner
Comment=Управление процессором
Exec=gksudo python3 /opt/cpu-tuner-gui/cpu_tuner_gui.py
Icon=utilities-system-monitor
Terminal=false
Type=Application
Categories=System;Monitor;
StartupNotify=true
EOF

# Установка gksudo (если нет)
apt install -y gksu 2>/dev/null || echo "gksu не установлен, будет запрос пароля в терминале"

echo "✅ Ярлык создан! Найдите CPU Tuner в меню приложений"
