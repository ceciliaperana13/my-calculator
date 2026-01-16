import tkinter as tk
from tkinter import ttk



# CONFIGURATION


# Colors used in the calculator
COLORS = {
    "light_gray": "#D4D4D2",
    "black": "#1C1C1C",
    "dark_gray": "#505050",
    "blue": "#043A5C",
    "white": "#FFFFFF",
    "display_gray": "#888888",
}

BUTTON_LAYOUT = [
    ["AC", "%", "(", ")"],
    ["7", "8", "9", "÷"],
    ["4", "5", "6", "×"],
    ["1", "2", "3", "-"],
    ["0", ".", "Hist", "+"],
    ["+/-", "√", "xʸ", "="]
]

OPERATORS = {"+", "-", "×", "÷", "^"}
SPECIAL_FUNCTIONS = {"AC", "+/-", "%", "√", "(", ")", "xʸ", "Hist"}



# CALCULATION ENGINE


class CalculationEngine:


    def format_number(self, num):
        # Number 0
        if num == 0:
            return "0"
        
        # If the number is too large (>= 10 billion) or too small in absolute value
        if abs(num) >= 1e10 or (abs(num) < 1e-3 and num != 0):
            # Max 10 characters
            result = f"{num:.3e}"
            
            if len(result) > 10:
                for precision in range(2, -1, -1):
                    result = f"{num:.{precision}e}"
                    if len(result) <= 10:
                        break
            return result
        
        # If it's an integer
        if num % 1 == 0:
            result = str(int(num))
            # If the integer part exceeds 10 digits, use scientific notation
            if len(result) > 10:
                return f"{num:.3e}"[:10]
            return result
        else:
            # Normal decimal number
            integer_part = int(abs(num))
            sign = "-" if num < 0 else ""
            
            if len(str(integer_part)) > 10:
                return f"{num:.3e}"[:10]
            
            # Format with a maximum of 3 decimal places
            result = f"{round(num, 3):.3f}".rstrip("0").rstrip(".")
            
            # Check if it exceeds 10 characters
            if len(result) > 10:
                # Reduce decimals
                num_decimals = 3
                while num_decimals > 0:
                    result = f"{num:.{num_decimals}f}".rstrip("0").rstrip(".")
                    if len(result) <= 10:
                        break
                    num_decimals -= 1
                
                # If still too long, use scientific notation
                if len(result) > 10:
                    result = f"{num:.3e}"[:10]
            
            return result

    def _tokenize(self, expr):
        # Tokenize expression
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
        # Convert to Reverse Polish Notation
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
                while stack and stack[-1] != "(" and priority.get(stack[-1], 0) >= priority.get(t, 0):
                    output.append(stack.pop())
                stack.append(t)

        while stack:
            output.append(stack.pop())
        return output

    def _evaluate_rpn(self, rpn):
        # Evaluate RPN expression
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
        return self.format_number(stack[0])

    def evaluate(self, expression):
        """Evaluate a mathematical expression"""
        tokens = self._tokenize(expression)
        rpn = self._to_rpn(tokens)
        return self._evaluate_rpn(rpn)



# HISTORY MANAGER


class HistoryManager:
    """Manages the history of calculations in memory"""
    
    def __init__(self, parent_window):
        self.parent_window = parent_window
        self.history = []
        self.hist_window = None 
        self.listbox = None  
    
    def save(self, expression, result):
        """Save calculation to history"""
        self.history.append({
            "expression": expression,
            "result": result
        })
        
        # Keep only the last 50 entries
        if len(self.history) > 50:
            self.history = self.history[-50:]
        
        # Update the display in real time if the window is open
        if self.listbox and self.hist_window and self.hist_window.winfo_exists():
            self.listbox.insert(0, f"{expression} = {result}")
    
    def display(self):
        """Display the history window (only once)"""
        
        if self.hist_window and self.hist_window.winfo_exists():
            self.hist_window.lift()
            self.hist_window.focus_force()
            return
        
        # Create new window
        self.hist_window = tk.Toplevel(self.parent_window)
        self.hist_window.title("History")
        self.hist_window.geometry("400x550")
        self.hist_window.resizable(False, False)
        
        # Frame with scrollbar
        frame = tk.Frame(self.hist_window)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.listbox = tk.Listbox(
            frame,
            yscrollcommand=scrollbar.set,
            font=("Arial", 12),
            bg=COLORS["black"],
            fg=COLORS["white"]
        )
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.listbox.yview)
        
        # Add history entries
        for entry in reversed(self.history):
            self.listbox.insert(tk.END, f"{entry['expression']} = {entry['result']}")
        
        # Frame for buttons
        btn_frame = tk.Frame(self.hist_window)
        btn_frame.pack(pady=10)
        
        # Clear button
        btn_clear = tk.Button(
            btn_frame,
            text="Clear History",
            command=self._clear_history,
            bg=COLORS["blue"],
            fg="white",
            font=("Arial", 12),
            width=18
        )
        btn_clear.pack(side=tk.LEFT, padx=5)
        
        # Close button
        btn_close = tk.Button(
            btn_frame,
            text="Close",
            command=self.hist_window.destroy,
            bg="#C41E3A",
            fg="white",
            font=("Arial", 12),
            width=18
        )
        btn_close.pack(side=tk.LEFT, padx=5)
    
    def _clear_history(self):
        """Clear all history"""
        self.history = []
        self.listbox.delete(0, tk.END)



# CALCULATOR INTERFACE


class Calculator:
    """Graphical interface of the calculator"""
    
    def __init__(self, window: tk.Tk):
        self.window = window
        self.expression = ""
        self.result_shown = False
        
        # Initialize the calculation engine and history
        self.engine = CalculationEngine()
        self.history = HistoryManager(self.window)

        self._setup_window()
        self._create_display()
        self._create_buttons()
        self._center_window()

    def _setup_window(self):
        """Configure the main window"""
        self.window.title("Calculator")
        self.window.resizable(False, False)
        self.frame = tk.Frame(self.window)
        self.frame.pack()

    def _create_display(self):
        """Create the display (calculator screen)"""
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
        """Create all calculator buttons"""
        for r, row in enumerate(BUTTON_LAYOUT):
            for c, value in enumerate(row):
                if value == "":
                    continue
                    
                btn = tk.Button(
                    self.frame,
                    text=value,
                    font=("Arial", 30),
                    width=4,
                    command=lambda v=value: self.button_clicked(v)
                )

                # Button styling
                if value == "Hist":
                    btn.config(bg=COLORS["light_gray"], font=("Arial", 20))
                elif value in SPECIAL_FUNCTIONS:
                    btn.config(bg=COLORS["light_gray"])
                elif value in OPERATORS or value == "=":
                    btn.config(bg=COLORS["blue"], fg="white")
                else:
                    btn.config(bg=COLORS["dark_gray"], fg="white")

                btn.grid(row=r + 2, column=c)

    def _center_window(self):
        """Center the window on the screen"""
        self.window.update()
        w, h = self.window.winfo_width(), self.window.winfo_height()
        sw, sh = self.window.winfo_screenwidth(), self.window.winfo_screenheight()
        self.window.geometry(f"{w}x{h}+{(sw-w)//2}+{(sh-h)//2}")

    def button_clicked(self, value: str):
        """Handle button clicks"""
        if self.display_label.cget("text") == "Error" and value != "AC":
            return

        match value:
            case "Hist":
                self.history.display()

            case "AC":
                self.expression = ""
                self.result_shown = False
                self.display_label.config(text="0")
                self.operation_label.config(text="")

            case "=":
                if not self.expression:
                    return
                try:
                    result = self.engine.evaluate(self.expression)
                    
                    self.operation_label.config(text=self.expression + " =")
                    self.display_label.config(text=result)
                    
                    # Save to history
                    self.history.save(self.expression, result)
                    
                    self.expression = result
                    self.result_shown = True
                except Exception:
                    self.display_label.config(text="Error")
                    
                    # Save error to history
                    self.history.save(self.expression, "Error")
                    
                    self.expression = ""
                    self.result_shown = True

            case "xʸ":
                if self.expression and self.expression[-1] in "+-×÷^":
                    self.expression = self.expression[:-1]
                self.expression += "^"
                self.operation_label.config(text=self.expression.replace("^", "xʸ"))
                self.display_label.config(text="0")
                self.result_shown = False

            case "√":
                try:
                    # If an expression is in progress (with operators), evaluate it first
                    if self.expression and any(op in self.expression for op in "+-×÷^"):
                        current = float(self.engine.evaluate(self.expression))
                    else:
                        current = float(self.display_label.cget("text").replace("e", "E"))
                    
                    if current < 0:
                        raise ValueError

                    result = self.engine.format_number(current ** 0.5)
                    self.display_label.config(text=result)
                    
                    # Display the original expression if it exists, otherwise just the number
                    if self.expression and any(op in self.expression for op in "+-×÷^"):
                        display_expr = f"√({self.expression})"
                    else:
                        display_expr = f"√({current})"
                    
                    self.operation_label.config(text=display_expr)
                    
                    # Save to history
                    self.history.save(display_expr, result)
                    
                    self.expression = result
                    self.result_shown = True
                except Exception:
                    self.display_label.config(text="Error")
                    
                    # Save error to history
                    if self.expression:
                        display_expr = f"√({self.expression})"
                    else:
                        current_val = self.display_label.cget("text")
                        display_expr = f"√({current_val})"
                    
                    self.history.save(display_expr, "Error")
                    
                    self.expression = ""
                    self.result_shown = True

            case "%":
                try:
                    current = float(self.display_label.cget("text").replace("e", "E"))
                    result = self.engine.format_number(current / 100)
                    self.display_label.config(text=result)
                    
                    # Save to history
                    self.history.save(f"{current}%", result)
                    
                    self.expression = result
                    self.operation_label.config(text=self.expression)
                    self.result_shown = True
                except Exception:
                    self.display_label.config(text="Error")
                    
                    # Save error to history
                    current_val = self.display_label.cget("text")
                    self.history.save(f"{current_val}%", "Error")
                    
                    self.expression = ""
                    self.result_shown = True

            case "+/-":
                txt = self.display_label.cget("text")
                if txt != "0" and txt != "Error":
                    if txt.startswith("-"):
                        txt = txt[1:]
                    else:
                        txt = "-" + txt
                    self.display_label.config(text=txt)
                    self.expression = txt

            case "(" | ")":
                if self.result_shown:
                    self.expression = ""
                    self.result_shown = False

                self.expression += value
                self.operation_label.config(text=self.expression)

            case "+" | "-" | "×" | "÷":
                self.result_shown = False
                if self.expression and self.expression[-1] in "+-×÷^":
                    self.expression = self.expression[:-1]
                self.expression += value
                self.operation_label.config(text=self.expression)
                self.display_label.config(text="0")

            case ".":
                current = self.display_label.cget("text")
                
                # Don't add decimal point if in scientific notation
                if "e" in current:
                    return
                
                # Check 10 character limit
                if len(current) >= 10:
                    return
                
                if "." not in current:
                    if current == "0":
                        self.display_label.config(text="0.")
                        self.expression += "0."
                    else:
                        self.display_label.config(text=current + ".")
                        self.expression += "."

            case _:  # Numbers
                if self.result_shown:
                    self.expression = value
                    self.display_label.config(text=value)
                    self.operation_label.config(text=self.expression)
                    self.result_shown = False
                    return

                current = self.display_label.cget("text")
                
                # Don't add digits if in scientific notation
                if "e" in current:
                    return
                
                # LIMIT TO 10 CHARACTERS
                if len(current) >= 10 and current != "0":
                    return
                
                if current == "0":
                    self.display_label.config(text=value)
                else:
                    self.display_label.config(text=current + value)

                self.expression += value
                self.operation_label.config(text=self.expression)



# LAUNCH


if __name__ == "__main__":
    window = tk.Tk()
    Calculator(window)
    window.mainloop()