# 📀 Установка CPU Tuner GUI на чистый Debian

Это руководство поможет установить приложение на **свежеустановленный Debian**.

---

## 🚀 Быстрая установка (одной командой)

Скопируйте и вставьте в терминал:

```bash
sudo apt update && sudo apt install -y git && \
git clone https://github.com/G0rde1/cpu-tuner-gui.git && \
cd cpu-tuner-gui/debian-setup && \
sudo ./full_install.sh
