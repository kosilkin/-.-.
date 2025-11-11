import tkinter as tk
from tkinter import messagebox

class ResizableCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Адаптивный калькулятор")
        self.root.configure(bg="#1e1e2f")
        
        # Цвета
        self.bg_color = "#1e1e2f"
        self.btn_color = "#2d2d44"
        self.accent_color = "#6e56cf"
        self.text_color = "#e0e0ff"
        self.highlight_color = "#8a75e1"
        self.display_text_color = "black"
        
        self.expression = ""
        
        # Конфигурация сетки
        for i in range(4):
            self.root.grid_columnconfigure(i, weight=1)
        for i in range(6):
            self.root.grid_rowconfigure(i, weight=1)
        
        # Заголовок
        self.title_label = tk.Label(
            root,
            text="Калькулятор",
            font=("Segoe UI", 14, "bold"),
            bg=self.bg_color,
            fg=self.text_color
        )
        self.title_label.grid(row=0, column=0, columnspan=4, padx=10, pady=5, sticky="ew")
        
        # Дисплей с рамкой
        self.display_frame = tk.Frame(root, bg=self.accent_color, bd=0, relief="flat")
        self.display_frame.grid(row=1, column=0, columnspan=4, padx=10, pady=5, sticky="nsew")
        
        self.display = tk.Entry(
            self.display_frame,
            font=("Digital-7", 20),
            borderwidth=0,
            bg=self.btn_color,
            fg=self.display_text_color,
            justify="right",
            state="readonly"
        )
        self.display.pack(padx=2, pady=2, fill="both", expand=True)
        
        # Матрица кнопок
        buttons = [
            ('C', 1, 2, self.clear),
            ('←', 1, 2, self.backspace),
            ('7', 1, 1), ('8', 1, 1), ('9', 1, 1), ('/', 1, 1),
            ('4', 1, 1), ('5', 1, 1), ('6', 1, 1), ('*', 1, 1),
            ('1', 1, 1), ('2', 1, 1), ('3', 1, 1), ('-', 1, 1),
            ('0', 1, 1), ('.', 1, 1), ('+', 1, 1),
            ('=', 1, 2, self.calculate)
        ]
        
        row, col = 2, 0
        for btn_data in buttons:
            text, rowspan, colspan = btn_data[0], btn_data[1], btn_data[2]
            cmd = btn_data[3] if len(btn_data) > 3 else lambda t=text: self.append(t)
            
            btn = self.create_button(root, text, cmd, rowspan, colspan)
            btn.grid(row=row, column=col, rowspan=rowspan, columnspan=colspan, padx=2, pady=2, sticky="nsew")
            
            col += colspan
            if col >= 4:
                col = 0
                row += rowspan
        
        # Привязка клавиатурных событий
        self.bind_keyboard()

    def create_button(self, parent, text, command, rowspan=1, colspan=1):
        btn = tk.Button(
            parent,
            text=text,
            font=("Segoe UI", 12, "bold"),
            bd=0,
            bg=self.btn_color,
            fg=self.text_color,
            activebackground=self.highlight_color,
            activeforeground=self.text_color,
            relief="flat",
            command=command,
            cursor="hand2"
        )
        
        btn.bind("<Enter>", lambda e: btn.config(bg=self.highlight_color))
        btn.bind("<Leave>", lambda e: btn.config(bg=self.btn_color))
        
        return btn

    def bind_keyboard(self):
        """Привязка клавиш клавиатуры"""
        # Цифры и операции
        for key in '0123456789+-*/.':
            self.root.bind(key, lambda e, k=key: self.append(k))
        
        # Клавиша Enter = равно
        self.root.bind('<Return>', self.calculate)
        self.root.bind('<KP_Enter>', self.calculate)  # Цифровой блок
        
        # Backspace
        self.root.bind('<BackSpace>', self.backspace)
        
        # Escape = сброс
        self.root.bind('<Escape>', self.clear)
        
        # Фокус на окне для приёма клавиатурных событий
        self.root.focus_set()

    def append(self, char):
        self.expression += str(char)
        self.update_display()

    def clear(self, event=None):
        self.expression = ""
        self.update_display()

    def backspace(self, event=None):
        self.expression = self.expression[:-1]
        self.update_display()

    def calculate(self, event=None):
        try:
            result = str(eval(self.expression.replace(',', '.')))
            self.expression = result
            self.update_display()
        except:
            messagebox.showerror("Ошибка", "Некорректное выражение")
            self.expression = ""
            self.update_display()

    def update_display(self):
        self.display.config(state="normal")
        self.display.delete(0, tk.END)
        self.display.insert(0, self.expression)
        self.display.config(state="readonly")

# Запуск приложения
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("300x400")
    root.resizable(True, True)
    app = ResizableCalculator(root)
    root.mainloop()
