import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import re

class TrainingPlannerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Training Planner (План тренировок)")
        self.root.geometry("650x500")
        
        self.file_path = "trainings.json"
        self.data = self.load_data()

        # --- СЕКЦИЯ ВВОДА ---
        input_frame = tk.LabelFrame(root, text="Добавить новую тренировку", padx=10, pady=10)
        input_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(input_frame, text="Дата (ДД.ММ.ГГГГ):").grid(row=0, column=0, sticky="w")
        self.date_entry = tk.Entry(input_frame)
        self.date_entry.grid(row=0, column=1, padx=5, pady=2)

        tk.Label(input_frame, text="Тип тренировки:").grid(row=1, column=0, sticky="w")
        self.type_entry = tk.Entry(input_frame)
        self.type_entry.grid(row=1, column=1, padx=5, pady=2)

        tk.Label(input_frame, text="Длительность (мин):").grid(row=2, column=0, sticky="w")
        self.duration_entry = tk.Entry(input_frame)
        self.duration_entry.grid(row=2, column=1, padx=5, pady=2)

        add_btn = tk.Button(input_frame, text="Добавить тренировку", command=self.add_training, bg="#4caf50", fg="white")
        add_btn.grid(row=3, column=0, columnspan=2, pady=10, sticky="we")

        # --- СЕКЦИЯ ФИЛЬТРАЦИИ ---
        filter_frame = tk.LabelFrame(root, text="Фильтрация", padx=10, pady=10)
        filter_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(filter_frame, text="Поиск по типу/дате:").pack(side="left")
        self.filter_entry = tk.Entry(filter_frame)
        self.filter_entry.pack(side="left", fill="x", expand=True, padx=5)
        self.filter_entry.bind("<KeyRelease>", lambda event: self.refresh_table())

        # --- ТАБЛИЦА ВЫВОДА ---
        self.tree = ttk.Treeview(root, columns=("date", "type", "duration"), show="headings")
        self.tree.heading("date", text="Дата")
        self.tree.heading("type", text="Тип тренировки")
        self.tree.heading("duration", text="Длительность (мин)")
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        self.refresh_table()

    def validate_date(self, date_str):
        # Простая проверка формата ДД.ММ.ГГГГ регулярным выражением
        pattern = r"^\d{2}\.\d{2}\.\d{4}$"
        return re.match(pattern, date_str) is not None

    def load_data(self):
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except:
                return []
        return []

    def save_data(self):
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4)

    def add_training(self):
        date = self.date_entry.get().strip()
        t_type = self.type_entry.get().strip()
        duration = self.duration_entry.get().strip()

        # Проверки (Валидация)
        if not self.validate_date(date):
            messagebox.showerror("Ошибка", "Неверный формат даты! Используйте ДД.ММ.ГГГГ")
            return

        if not t_type:
            messagebox.showerror("Ошибка", "Введите тип тренировки!")
            return

        try:
            dur_int = int(duration)
            if dur_int <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Ошибка", "Длительность должна быть целым положительным числом!")
            return

        # Добавление данных
        new_entry = {"date": date, "type": t_type, "duration": dur_int}
        self.data.append(new_entry)
        self.save_data()
        self.refresh_table()
        
        # Очистка полей
        self.date_entry.delete(0, tk.END)
        self.type_entry.delete(0, tk.END)
        self.duration_entry.delete(0, tk.END)
        messagebox.showinfo("Успех", "Тренировка добавлена!")

    def refresh_table(self):
        # Очистка таблицы
        for item in self.tree.get_children():
            self.tree.delete(item)

        filter_text = self.filter_entry.get().lower()

        # Заполнение с учетом фильтра
        for entry in self.data:
            if filter_text in entry["type"].lower() or filter_text in entry["date"]:
                self.tree.insert("", tk.END, values=(entry["date"], entry["type"], entry["duration"]))

if __name__ == "__main__":
    root = tk.Tk()
    app = TrainingPlannerApp(root)
    root.mainloop()
