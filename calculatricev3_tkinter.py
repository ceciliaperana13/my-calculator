import tkinter as tk
from typing import Optional

# Configuration des couleurs
COLORS = {
    "light_gray": "#D4D4D2",
    "black": "#1C1C1C",
    "dark_gray": "#505050",
    "blue": "#043A5C",
    "white": "#FFFFFF",
    "display_gray": "#888888",
}

# Configuration des boutons
BUTTON_LAYOUT = [
    ["AC", "%", "(", ")"],
    ["7", "8", "9", "÷"],
    ["4", "5", "6", "×"],
    ["1", "2", "3", "-"],
    ["0", ".", "x²", "+"],
    ["x³", "+/-", "√", "="]
]

OPERATORS = {"+", "-", "×", "÷"}
SPECIAL_FUNCTIONS = {"AC", "+/-", "%", "√", "(", ")", "x²", "x³"}

class Calculator:
    def __init__(self, window: tk.Tk):
        self.window = window
        self.expression = ""
        self.result_shown = False

        self._setup_window()
        self._create_display()
        self._create_buttons()
        self._center_window()

    def _setup_window(self):
        self.window.title("Calculator")
        self.window.resizable(False, False)
        self.frame = tk.Frame(self.window)
        self.frame.pack()

    def _create_display(self):
        self.operation_label = tk.Label(
            self.frame,
            text="",
            font=("Arial", 20),
            bg=COLORS["black"],
            fg=COLORS["display_gray"],
            anchor="e"
        )
        self.operation_label.grid(row=0, column=0, columnspan=4, sticky="we")

        self.display_label = tk.Label(
            self.frame,
            text="0",
            font=("Arial", 45),
            bg=COLORS["black"],
            fg=COLORS["white"],
            anchor="e"
        )
        self.display_label.grid(row=1, column=0, columnspan=4, sticky="we")

    def _create_buttons(self):
        for r, row in enumerate(BUTTON_LAYOUT):
            for c, value in enumerate(row):
                btn = tk.Button(
                    self.frame,
                    text=value,
                    font=("Arial", 30),
                    width=4,
                    command=lambda v=value: self.button_clicked(v)
                )

                if value in SPECIAL_FUNCTIONS:
                    btn.config(bg=COLORS["light_gray"])
                elif value in OPERATORS or value == "=":
                    btn.config(bg=COLORS["blue"], fg="white")
                else:
                    btn.config(bg=COLORS["dark_gray"], fg="white")

                btn.grid(row=r + 2, column=c)

    def _center_window(self):
        self.window.update()
        w, h = self.window.winfo_width(), self.window.winfo_height()
        sw, sh = self.window.winfo_screenwidth(), self.window.winfo_screenheight()
        self.window.geometry(f"{w}x{h}+{(sw-w)//2}+{(sh-h)//2}")

    # MOTEUR DE CALCUL 

    def _format_number(self, num: float) -> str:
        if num % 1 == 0:
            return str(int(num))
        return f"{round(num, 3):.3f}".rstrip("0").rstrip(".")

    def _tokenize(self, expr: str):
        tokens = []
        number = ""
        i = 0

        while i < len(expr):
            c = expr[i]

            if c.isdigit() or c == ".":
                number += c
            elif c == "-" and (i == 0 or expr[i-1] in "+-×÷("):
                if i + 1 < len(expr) and expr[i+1] == "(":
                 tokens.append("0")
                 tokens.append("-")
                else: 
                 number += c
            else:
                if number:
                    tokens.append(number)
                    number = ""
                tokens.append(c)
            i += 1

        if number:
            tokens.append(number)

        return tokens

    def _to_rpn(self, tokens):
        priority = {"+": 1, "-": 1, "×": 2, "÷": 2}
        output = []
        stack = []

        for t in tokens:
            if t.replace(".", "", 1).lstrip("-").isdigit():
                output.append(t)
            elif t == "(":
                stack.append(t)
            elif t == ")":
                while stack and stack[-1] != "(":
                    output.append(stack.pop())
                stack.pop()
            else:
                while stack and stack[-1] != "(" and priority.get(stack[-1], 0) >= priority[t]:
                    output.append(stack.pop())
                stack.append(t)

        while stack:
            output.append(stack.pop())

        return output

    def _evaluate_rpn(self, rpn):
        stack = []
        for t in rpn:
            if t.replace(".", "", 1).lstrip("-").isdigit():
                stack.append(float(t))
            else:
                b, a = stack.pop(), stack.pop()
                if t == "+":
                    stack.append(a + b)
                elif t == "-":
                    stack.append(a - b)
                elif t == "×":
                    stack.append(a * b)
                elif t == "÷":
                    if b == 0:
                        raise ZeroDivisionError
                    stack.append(a / b)
        return self._format_number(stack[0])

    # INTERACTIONS 

    def button_clicked(self, value: str):
        if self.display_label.cget("text") == "Erreur" and value != "AC":
            return

        match value:
            case "AC":
                self.expression = ""
                self.result_shown = False
                self.display_label.config(text="0")
                self.operation_label.config(text="")

            case "=":
                try:
                    tokens = self._tokenize(self.expression)
                    rpn = self._to_rpn(tokens)
                    result = self._evaluate_rpn(rpn)
                    self.operation_label.config(text=self.expression + " =")
                    self.display_label.config(text=result)
                    self.expression = result
                    self.result_shown = True
                except Exception:
                    self.display_label.config(text="Erreur")
                    self.expression = ""
                    self.result_shown = True

            case "+/-":
                current = self.display_label.cget("text")
                if current.startswith("-"):
                    current = current[1:]
                else:
                    current = "-" + current
                self.display_label.config(text=current)
                self.expression = current
                self.operation_label.config(text=current)

            case "√":
                try:
                    current = float(self.display_label.cget("text"))
                    result = self._format_number(current ** 0.5)
                    self.display_label.config(text=result)
                    self.expression = result
                    self.operation_label.config(text=f"√({current})")
                    self.result_shown = True
                except Exception:
                    self.display_label.config(text="Erreur")

            case "x²":
                try:
                    current = float(self.display_label.cget("text"))
                    result = self._format_number(current ** 2)
                    self.display_label.config(text=result)
                    self.expression = result
                    self.operation_label.config(text=f"({current})²")
                    self.result_shown = True
                except Exception:
                    self.display_label.config(text="Erreur")

            case "x³":
                try:
                    current = float(self.display_label.cget("text"))
                    result = self._format_number(current ** 3)
                    self.display_label.config(text=result)
                    self.expression = result
                    self.operation_label.config(text=f"({current})³")
                    self.result_shown = True
                except Exception:
                    self.display_label.config(text="Erreur")

            case "%":
                current = float(self.display_label.cget("text"))
                result = self._format_number(current / 100)
                self.display_label.config(text=result)
                self.expression = result
                self.operation_label.config(text=result)
                self.result_shown = True

            case "+" | "-" | "×" | "÷":
                if self.expression and self.expression[-1] in "+-×÷":
                    self.expression = self.expression[:-1]
                self.expression += value
                self.operation_label.config(text=self.expression)
                self.display_label.config(text="0")
                self.result_shown = False

            case ".":
                current = self.display_label.cget("text")
                if "." not in current:
                    self.display_label.config(text=current + ".")
                    self.expression += "."

            case _:
                if self.result_shown:
                    self.expression = value
                    self.display_label.config(text=value)
                    self.result_shown = False
                else:
                    current = self.display_label.cget("text")
                    self.display_label.config(text=value if current == "0" else current + value)
                    self.expression += value
                self.operation_label.config(text=self.expression)

# Lancement
if __name__ == "__main__":
    window = tk.Tk()
    Calculator(window)
    window.mainloop()
