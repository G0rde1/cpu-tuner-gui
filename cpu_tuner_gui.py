#!/usr/bin/env python3
# CPU Tuner - десктопное приложение для управления CPU

import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import psutil
import threading
import time

class CPUTunerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CPU Tuner - Управление процессором")
        self.root.geometry("700x550")
        self.root.resizable(True, True)
        
        # Переменные
        self.governors = ['performance', 'powersave', 'ondemand', 'conservative', 'schedutil']
        self.current_governor = tk.StringVar()
        self.monitoring = False
        
        # Интерфейс
        self.setup_ui()
        
        # Обновление данных
        self.refresh_data()
        
    def setup_ui(self):
        # Стиль
        style = ttk.Style()
        style.theme_use('clam')
        
        # Заголовок
        title = tk.Label(self.root, text="⚡ CPU Tuner", font=('Arial', 20, 'bold'))
        title.pack(pady=10)
        
        # Рамка с информацией о CPU
        info_frame = tk.LabelFrame(self.root, text="📊 Информация о CPU", padx=10, pady=10)
        info_frame.pack(fill="x", padx=20, pady=10)
        
        self.cpu_model_label = tk.Label(info_frame, text="Модель: Загрузка...", font=('Arial', 10))
        self.cpu_model_label.pack(anchor="w")
        
        self.cpu_cores_label = tk.Label(info_frame, text="Ядра: Загрузка...", font=('Arial', 10))
        self.cpu_cores_label.pack(anchor="w")
        
        # Рамка с температурами
        temp_frame = tk.LabelFrame(self.root, text="🌡️ Температуры", padx=10, pady=10)
        temp_frame.pack(fill="x", padx=20, pady=10)
        
        self.temp_labels = []
        for i in range(8):
            label = tk.Label(temp_frame, text=f"Core {i}: --°C", font=('Arial', 10))
            label.pack(anchor="w")
            self.temp_labels.append(label)
        
        # Рамка с управлением governor
        gov_frame = tk.LabelFrame(self.root, text="⚡ Управление частотой (Governor)", padx=10, pady=10)
        gov_frame.pack(fill="x", padx=20, pady=10)
        
        tk.Label(gov_frame, text="Текущий режим:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        
        self.gov_combo = ttk.Combobox(gov_frame, textvariable=self.current_governor, values=self.governors, state="readonly")
        self.gov_combo.grid(row=0, column=1, padx=5, pady=5)
        
        self.apply_btn = tk.Button(gov_frame, text="Применить", command=self.set_governor, bg="#4CAF50", fg="white", padx=10)
        self.apply_btn.grid(row=0, column=2, padx=10, pady=5)
        
        # Рамка с загрузкой CPU
        usage_frame = tk.LabelFrame(self.root, text="📈 Загрузка CPU", padx=10, pady=10)
        usage_frame.pack(fill="x", padx=20, pady=10)
        
        self.cpu_usage_label = tk.Label(usage_frame, text="Общая загрузка: --%", font=('Arial', 12, 'bold'))
        self.cpu_usage_label.pack(anchor="w")
        
        self.cpu_cores_usage = []
        cores_usage_frame = tk.Frame(usage_frame)
        cores_usage_frame.pack(fill="x", pady=5)
        
        for i in range(8):
            label = tk.Label(cores_usage_frame, text=f"Core {i}: --%", width=12, anchor="w")
            label.grid(row=i//4, column=i%4, padx=5, pady=2, sticky="w")
            self.cpu_cores_usage.append(label)
        
        # Кнопки управления
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=15)
        
        self.monitor_btn = tk.Button(btn_frame, text="▶ Запустить мониторинг", command=self.toggle_monitoring, bg="#2196F3", fg="white", padx=15)
        self.monitor_btn.pack(side="left", padx=10)
        
        self.refresh_btn = tk.Button(btn_frame, text="🔄 Обновить", command=self.refresh_data, bg="#FF9800", fg="white", padx=15)
        self.refresh_btn.pack(side="left", padx=10)
        
        # Статус
        self.status_label = tk.Label(self.root, text="Готов", fg="green", font=('Arial', 9))
        self.status_label.pack(pady=5)
        
    def get_cpu_info(self):
        try:
            # Модель CPU
            with open('/proc/cpuinfo', 'r') as f:
                for line in f:
                    if 'model name' in line:
                        model = line.split(':')[1].strip()
                        break
            # Количество ядер
            cores = psutil.cpu_count()
            return model, cores
        except:
            return "Не определено", 0
            
    def get_temperatures(self):
        temps = {}
        try:
            output = subprocess.check_output(['sensors'], text=True)
            for line in output.split('\n'):
                if 'Core' in line or 'Tctl' in line:
                    import re
                    match = re.search(r'\+(\d+\.\d+)', line)
                    if match:
                        name = line.split(':')[0].strip()
                        temps[name] = float(match.group(1))
        except:
            pass
        return temps
        
    def get_governor(self):
        try:
            with open('/sys/devices/system/cpu/cpu0/cpufreq/scaling_governor', 'r') as f:
                return f.read().strip()
        except:
            return "unknown"
            
    def set_governor(self):
        gov = self.current_governor.get()
        if not gov:
            return
            
        try:
            for cpu in range(psutil.cpu_count()):
                with open(f'/sys/devices/system/cpu/cpu{cpu}/cpufreq/scaling_governor', 'w') as f:
                    f.write(gov)
            self.status_label.config(text=f"✅ Governor изменён на {gov}", fg="green")
            self.refresh_data()
        except Exception as e:
            self.status_label.config(text=f"❌ Ошибка: запустите с sudo", fg="red")
            messagebox.showerror("Ошибка", "Нужны права root!\nЗапустите: sudo python3 cpu_tuner_gui.py")
            
    def refresh_data(self):
        # CPU информация
        model, cores = self.get_cpu_info()
        self.cpu_model_label.config(text=f"Модель: {model[:60]}")
        self.cpu_cores_label.config(text=f"Ядра: {cores}")
        
        # Governor
        gov = self.get_governor()
        self.current_governor.set(gov)
        
        # Температуры
        temps = self.get_temperatures()
        for i, label in enumerate(self.temp_labels):
            core_name = f"Core {i}"
            if core_name in temps:
                temp = temps[core_name]
                label.config(text=f"{core_name}: {temp}°C")
                if temp > 80:
                    label.config(fg="red")
                elif temp > 70:
                    label.config(fg="orange")
                else:
                    label.config(fg="white")
            else:
                label.config(text=f"Core {i}: --°C")
        
        # Загрузка CPU
        cpu_percent = psutil.cpu_percent(interval=0.5)
        self.cpu_usage_label.config(text=f"Общая загрузка: {cpu_percent}%")
        
        per_cpu = psutil.cpu_percent(interval=0.5, percpu=True)
        for i, label in enumerate(self.cpu_cores_usage):
            if i < len(per_cpu):
                label.config(text=f"Core {i}: {per_cpu[i]}%")
            else:
                label.config(text=f"Core {i}: --%")
                
    def monitor_loop(self):
        while self.monitoring:
            self.refresh_data()
            time.sleep(2)
            
    def toggle_monitoring(self):
        if not self.monitoring:
            self.monitoring = True
            self.monitor_btn.config(text="⏸ Остановить мониторинг", bg="#f44336")
            self.status_label.config(text="🟢 Мониторинг запущен (обновление каждые 2 сек)", fg="blue")
            thread = threading.Thread(target=self.monitor_loop, daemon=True)
            thread.start()
        else:
            self.monitoring = False
            self.monitor_btn.config(text="▶ Запустить мониторинг", bg="#2196F3")
            self.status_label.config(text="⏸ Мониторинг остановлен", fg="orange")

if __name__ == "__main__":
    root = tk.Tk()
    app = CPUTunerApp(root)
    root.mainloop()
