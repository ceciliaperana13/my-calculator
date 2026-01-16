import tkinter as tk

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
    ["0", ".", "", "+"],
    ["+/-", "√", "xʸ", "="]
]

OPERATORS = {"+", "-", "×", "÷", "^"}
SPECIAL_FUNCTIONS = {"AC", "+/-", "%", "√", "(", ")", "xʸ"}

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
            self.frame, text="", font=("Arial", 20),
            bg=COLORS["black"], fg=COLORS["display_gray"], anchor="e"
        )
        self.operation_label.grid(row=0, column=0, columnspan=4, sticky="we")

        self.display_label = tk.Label(
            self.frame, text="0", font=("Arial", 45),
            bg=COLORS["black"], fg=COLORS["white"], anchor="e"
        )
        self.display_label.grid(row=1, column=0, columnspan=4, sticky="we")

    def _create_buttons(self):
        for r, row in enumerate(BUTTON_LAYOUT):
            for c, value in enumerate(row):
                if not value:
                    continue
                btn = tk.Button(
                    self.frame, text=value, font=("Arial", 30),
                    width=4, command=lambda v=value: self.button_clicked(v)
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

    # ---------------- MOTEUR ----------------

    def _format_number(self, num):
        if num % 1 == 0:
            return str(int(num))
        return f"{round(num, 6):.6f}".rstrip("0").rstrip(".")

    def _tokenize(self, expr):
        tokens, number, i = [], "", 0
        while i < len(expr):
            c = expr[i]
            if c == "-" and (i == 0 or expr[i-1] in "+-×÷(^"):
                if i + 1 < len(expr) and expr[i+1] == "(":
                    tokens.extend(["0", "-"])
                else:
                    number += c
            elif c.isdigit() or c == ".":
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
        priority = {"+": 1, "-": 1, "×": 2, "÷": 2, "^": 3}
        output, stack = [], []

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
                while stack and stack[-1] != "(" and priority[stack[-1]] >= priority[t]:
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
                if t == "+": stack.append(a + b)
                elif t == "-": stack.append(a - b)
                elif t == "×": stack.append(a * b)
                elif t == "÷": stack.append(a / b)
                elif t == "^": stack.append(a ** b)
        return self._format_number(stack[0])

    # ---------------- INTERACTIONS ----------------

    def button_clicked(self, value):
        if self.display_label.cget("text") == "Erreur" and value != "AC":
            return

        match value:
            case "AC":
                self.expression = ""
                self.display_label.config(text="0")
                self.operation_label.config(text="")
                self.result_shown = False

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

            case "xʸ":
                if self.expression and self.expression[-1] in "+-×÷^":
                    self.expression = self.expression[:-1]
                self.expression += "^"
                self.operation_label.config(text=self.expression.replace("^", "xʸ"))
                self.display_label.config(text="0")

            case "√":
                try:
                    tokens = self._tokenize(self.expression)
                    rpn = self._to_rpn(tokens)
                    value = float(self._evaluate_rpn(rpn))
                    result = value ** 0.5
                    self.display_label.config(text=self._format_number(result))
                    self.operation_label.config(text=f"√({self.expression})")
                    self.expression = str(result)
                    self.result_shown = True
                except Exception:
                    self.display_label.config(text="Erreur")

            case "%":
                try:
                    value = float(self.display_label.cget("text")) / 100
                    value = self._format_number(value)
                    self.display_label.config(text=value)
                    self.expression = value
                except Exception:
                    self.display_label.config(text="Erreur")

            case "+/-":
                txt = self.display_label.cget("text")
                if txt.startswith("-"):
                    txt = txt[1:]
                else:
                    txt = "-" + txt
                self.display_label.config(text=txt)
                self.expression = txt

            case "(" | ")":
                self.expression += value
                self.operation_label.config(text=self.expression)

            case "+" | "-" | "×" | "÷":
                if self.expression and self.expression[-1] in "+-×÷^":
                    self.expression = self.expression[:-1]
                self.expression += value
                self.display_label.config(text="0")
                self.operation_label.config(text=self.expression)

            case ".":
                current = self.display_label.cget("text")
                if "." not in current:
                    if current == "0":
                        self.display_label.config(text="0.")
                        self.expression += "0."
                    else:
                        self.display_label.config(text=current + ".")
                        self.expression += "."

            case _:
                if self.result_shown:
                    self.expression = value
                    self.display_label.config(text=value)
                    self.result_shown = False
                else:
                    if self.display_label.cget("text") == "0":
                        self.display_label.config(text=value)
                    else:
                        self.display_label.config(text=self.display_label.cget("text") + value)
                    self.expression += value
                self.operation_label.config(text=self.expression)

# Lancement
if __name__ == "__main__":
    window = tk.Tk()
    Calculator(window)
    window.mainloop()