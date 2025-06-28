import tkinter as tk
from tkinter import ttk
import threading
import os
import tempfile
import shutil
import time
import random
import string

class EZtoolKitApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("EZtoolKit")
        self.geometry("700x500")  # Hauptfenster vergrößert
        self.configure(bg="#23272e")
        self.resizable(False, False)
        self.init_main_gui()

    def init_main_gui(self):
        style = ttk.Style(self)
        style.theme_use('clam')
        style.configure('TButton', font=('Segoe UI', 14, 'bold'), background="#7289da", foreground="#fff", padding=10)
        style.map('TButton', background=[('active', '#5865f2')])

        title = tk.Label(self, text="EZtoolKit", font=("Segoe UI", 28, "bold"), fg="#fff", bg="#23272e")
        title.pack(pady=40)

        btn_frame = tk.Frame(self, bg="#23272e")
        btn_frame.pack(pady=20)

        calc_btn = ttk.Button(btn_frame, text="Calculator", width=20, command=self.open_calculator)
        calc_btn.grid(row=0, column=0, padx=20, pady=10)

        storage_btn = ttk.Button(btn_frame, text="Storage Clean", width=20, command=self.open_storage_clean)
        storage_btn.grid(row=0, column=1, padx=20, pady=10)

        password_btn = ttk.Button(btn_frame, text="Password Generator", width=20, command=self.open_password_generator)
        password_btn.grid(row=1, column=0, padx=20, pady=10)

        stopwatch_btn = ttk.Button(btn_frame, text="Stop Watch", width=20, command=self.open_stopwatch)
        stopwatch_btn.grid(row=1, column=1, padx=20, pady=10)

    def open_calculator(self):
        CalculatorWindow(self)

    def open_storage_clean(self):
        StorageCleanWindow(self)

    def open_password_generator(self):
        PasswordGeneratorWindow(self)

    def open_stopwatch(self):
        StopwatchWindow(self)

class CalculatorWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Calculator")
        self.geometry("400x500")  # Taschenrechner-Fenster vergrößert
        self.configure(bg="#23272e")
        self.resizable(False, False)
        self.result_var = tk.StringVar()
        self.create_widgets()

    def create_widgets(self):
        entry = tk.Entry(self, textvariable=self.result_var, font=('Segoe UI', 22), bg="#2c2f36", fg="#fff", justify="right", bd=0)
        entry.pack(fill='x', padx=16, pady=(18, 8), ipady=10)

        btns = [
            ['7', '8', '9', '/'],
            ['4', '5', '6', '*'],
            ['1', '2', '3', '-'],
            ['0', '.', 'C', '+'],
            ['=', '', '', '']
        ]
        for row_idx, row in enumerate(btns):
            btn_row = tk.Frame(self, bg="#23272e")
            btn_row.pack(fill="x", padx=18, pady=4)
            for col_idx, char in enumerate(row):
                if char == '':
                    tk.Label(btn_row, text="", width=5, bg="#23272e").pack(side="left")
                    continue
                btn = tk.Button(
                    btn_row, text=char, font=('Segoe UI', 16), width=6, height=2,
                    bg="#4f545c" if char not in ('=', 'C') else ("#43b581" if char=='=' else "#f04747"),
                    fg="#fff", bd=0,
                    command=lambda c=char: self.on_button_click(c)
                )
                btn.pack(side="left", padx=4)

    def on_button_click(self, char):
        if char == "C":
            self.result_var.set("")
        elif char == "=":
            try:
                result = eval(self.result_var.get())
                self.result_var.set(str(result))
            except Exception:
                self.result_var.set("Error")
        else:
            self.result_var.set(self.result_var.get() + char)

class StorageCleanWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Storage Clean")
        self.geometry("400x250")
        self.configure(bg="#23272e")
        self.resizable(False, False)
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Storage Cleaner", font=("Segoe UI", 17, "bold"), bg="#23272e", fg="#fff").pack(pady=18)
        self.status_lbl = tk.Label(self, text="Ready to scan for junk files.", font=("Segoe UI", 12), bg="#23272e", fg="#bbbbbb")
        self.status_lbl.pack(pady=6)

        self.progress = ttk.Progressbar(self, orient='horizontal', length=350, mode='determinate')
        self.progress.pack(pady=16)

        self.clean_btn = ttk.Button(self, text="Scan & Clean", command=self.start_cleaning)
        self.clean_btn.pack(pady=8)

    def start_cleaning(self):
        self.clean_btn["state"] = "disabled"
        self.status_lbl.config(text="Scanning for junk files...")
        self.progress["value"] = 0
        threading.Thread(target=self.scan_and_clean, daemon=True).start()

    def scan_and_clean(self):
        time.sleep(1)
        junk_files = self.find_junk_files()
        total = len(junk_files)
        cleaned = 0

        self.status_lbl.config(text=f"Found {total} junk files. Cleaning...")
        for f in junk_files:
            time.sleep(0.1)
            try:
                if os.path.isfile(f):
                    os.remove(f)
                elif os.path.isdir(f):
                    shutil.rmtree(f)
            except Exception:
                pass
            cleaned += 1
            percent = int(cleaned / total * 100)
            self.progress["value"] = percent
            self.status_lbl.config(text=f"Cleaning... {percent}%")
            self.update_idletasks()
        self.progress["value"] = 100
        self.status_lbl.config(text=f"Cleanup finished! {total} files cleaned.")
        self.clean_btn["state"] = "normal"

    def find_junk_files(self):
        temp_dir = tempfile.gettempdir()
        junk_files = []
        for root, dirs, files in os.walk(temp_dir):
            for file in files:
                if file.endswith('.tmp') or file.startswith('~'):
                    junk_files.append(os.path.join(root, file))
            for d in dirs:
                if d.lower().startswith('junk'):
                    junk_files.append(os.path.join(root, d))
        return junk_files[:20]

class PasswordGeneratorWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Password Generator")
        self.geometry("400x250")
        self.configure(bg="#23272e")
        self.resizable(False, False)
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Password Generator", font=("Segoe UI", 17, "bold"), bg="#23272e", fg="#fff").pack(pady=18)
        self.password_var = tk.StringVar()

        password_display = tk.Entry(self, textvariable=self.password_var, font=("Segoe UI", 16), bg="#2c2f36", fg="#fff", justify="center", bd=0, state="readonly")
        password_display.pack(pady=10, padx=20, ipady=5)

        generate_btn = ttk.Button(self, text="Generate Password", command=self.generate_password)
        generate_btn.pack(pady=10)

    def generate_password(self):
        password = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
        self.password_var.set(password)

class StopwatchWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Stop Watch")
        self.geometry("500x300")
        self.configure(bg="#23272e")
        self.resizable(False, False)
        self.running = False
        self.elapsed_time = 0
        self.create_widgets()

    def create_widgets(self):
        self.time_var = tk.StringVar(value="00:00:00.000")
        time_display = tk.Label(self, textvariable=self.time_var, font=("Segoe UI", 28), bg="#23272e", fg="#fff")
        time_display.pack(pady=20)

        btn_frame = tk.Frame(self, bg="#23272e")
        btn_frame.pack(pady=20)

        start_btn = ttk.Button(btn_frame, text="Start", command=self.start)
        start_btn.grid(row=0, column=0, padx=10)

        stop_btn = ttk.Button(btn_frame, text="Stop", command=self.stop)
        stop_btn.grid(row=0, column=1, padx=10)

        reset_btn = ttk.Button(btn_frame, text="Reset", command=self.reset)
        reset_btn.grid(row=0, column=2, padx=10)

    def start(self):
        if not self.running:
            self.running = True
            self.update_time()

    def stop(self):
        self.running = False

    def reset(self):
        self.running = False
        self.elapsed_time = 0
        self.time_var.set("00:00:00.000")

    def update_time(self):
        if self.running:
            self.elapsed_time += 0.01
            hours, remainder = divmod(self.elapsed_time, 3600)
            minutes, remainder = divmod(remainder, 60)
            seconds, milliseconds = divmod(remainder, 1)
            time_str = f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}.{int(milliseconds * 1000):03}"
            self.time_var.set(time_str)
            self.after(10, self.update_time)

if __name__ == "__main__":
    app = EZtoolKitApp()
    app.mainloop()