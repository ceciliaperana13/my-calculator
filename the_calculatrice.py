import tkinter as tk
from tkinter import ttk
import re

# ============================================
# CONFIGURATION
# ============================================

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


# ============================================
# MOTEUR DE CALCUL
# ============================================

class CalculEngine:
    """Moteur de calcul avec évaluation d'expressions"""
    
    def format_number(self, num):
        """Formate un nombre pour l'affichage avec limitation à 10 chiffres avant virgule et 3 après"""
        # Si c'est un entier
        if num % 1 == 0:
            result = str(int(num))
            # Si la partie entière dépasse 10 chiffres, tronquer
            if len(result) > 10:
                return result[:10]
            return result
        else:
            # Séparer partie entière et décimale
            partie_entiere = int(abs(num))
            signe = "-" if num < 0 else ""
            
            # Si partie entière > 10 chiffres, tronquer sans décimales
            if len(str(partie_entiere)) > 10:
                return signe + str(partie_entiere)[:10]
            
            # Sinon, formater avec 3 décimales max
            result = f"{round(num, 3):.3f}".rstrip("0").rstrip(".")
            
            # Vérifier si ça dépasse 10 caractères (incluant le point et le signe)
            if len(result) > 10 + (1 if num < 0 else 0):
                # Réduire les décimales
                nb_decimales = 3
                while nb_decimales > 0:
                    result = f"{num:.{nb_decimales}f}".rstrip("0").rstrip(".")
                    if len(result) <= 10 + (1 if num < 0 else 0):
                        break
                    nb_decimales -= 1
                
                # Si toujours trop long, tronquer la partie entière
                if len(result) > 10 + (1 if num < 0 else 0):
                    result = signe + str(partie_entiere)[:10]
            
            return result

    def _tokenize(self, expr):
        """Convertit une expression en tokens"""
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
        """Convertit les tokens en notation polonaise inversée"""
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
        """Évalue une expression en notation polonaise inversée"""
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

    def evaluer(self, expression):
        """Évalue une expression mathématique"""
        tokens = self._tokenize(expression)
        rpn = self._to_rpn(tokens)
        return self._evaluate_rpn(rpn)


# ============================================
# GESTIONNAIRE D'HISTORIQUE
# ============================================

class HistoriqueManager:
    """Gère l'historique des calculs en mémoire"""
    
    def __init__(self, parent_window):
        self.parent_window = parent_window
        self.historique = []
        self.hist_window = None  # Référence à la fenêtre d'historique
    
    def sauvegarder(self, expression, resultat):
        """Sauvegarde un calcul dans l'historique"""
        self.historique.append({
            "expression": expression,
            "resultat": resultat
        })
        
        # Limiter à 50 entrées
        if len(self.historique) > 50:
            self.historique = self.historique[-50:]
    
    def afficher(self):
        """Affiche la fenêtre d'historique (une seule fois)"""
        # Si la fenêtre existe déjà et est ouverte, la mettre en avant
        if self.hist_window and self.hist_window.winfo_exists():
            self.hist_window.lift()
            self.hist_window.focus_force()
            return
        
        # Créer une nouvelle fenêtre
        self.hist_window = tk.Toplevel(self.parent_window)
        self.hist_window.title("Historique")
        self.hist_window.geometry("400x550")
        self.hist_window.resizable(False, False)
        
        # Frame avec scrollbar
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
        
        # Remplir l'historique (inversé pour avoir le plus récent en haut)
        for entry in reversed(self.historique):
            self.listbox.insert(tk.END, f"{entry['expression']} = {entry['resultat']}")
        
        # Frame pour les boutons
        btn_frame = tk.Frame(self.hist_window)
        btn_frame.pack(pady=10)
        
        # Bouton effacer en bleu
        btn_clear = tk.Button(
            btn_frame,
            text="Effacer l'historique",
            command=self._effacer_historique,
            bg=COLORS["blue"],
            fg="white",
            font=("Arial", 12),
            width=18
        )
        btn_clear.pack(side=tk.LEFT, padx=5)
        
        # Bouton fermer en rouge
        btn_close = tk.Button(
            btn_frame,
            text="Fermer",
            command=self.hist_window.destroy,
            bg="#C41E3A",
            fg="white",
            font=("Arial", 12),
            width=18
        )
        btn_close.pack(side=tk.LEFT, padx=5)
    
    def _effacer_historique(self):
        """Efface tout l'historique"""
        self.historique = []
        self.listbox.delete(0, tk.END)


# ============================================
# INTERFACE CALCULATRICE
# ============================================

class Calculator:
    """Interface graphique de la calculatrice"""
    
    def __init__(self, window: tk.Tk):
        self.window = window
        self.expression = ""
        self.result_shown = False
        
        # Initialiser le moteur de calcul et l'historique
        self.engine = CalculEngine()
        self.historique = HistoriqueManager(self.window)

        self._setup_window()
        self._create_display()
        self._create_buttons()
        self._center_window()

    def _setup_window(self):
        """Configure la fenêtre principale"""
        self.window.title("Calculator")
        self.window.resizable(False, False)
        self.frame = tk.Frame(self.window)
        self.frame.pack()

    def _create_display(self):
        """Crée l'affichage (écran de la calculatrice)"""
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
        """Crée tous les boutons de la calculatrice"""
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

                # Style de boutons
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
        """Centre la fenêtre sur l'écran"""
        self.window.update()
        w, h = self.window.winfo_width(), self.window.winfo_height()
        sw, sh = self.window.winfo_screenwidth(), self.window.winfo_screenheight()
        self.window.geometry(f"{w}x{h}+{(sw-w)//2}+{(sh-h)//2}")

    def button_clicked(self, value: str):
        """Gère les clics sur les boutons"""
        if self.display_label.cget("text") == "Erreur" and value != "AC":
            return

        match value:
            case "Hist":
                self.historique.afficher()

            case "AC":
                self.expression = ""
                self.result_shown = False
                self.display_label.config(text="0")
                self.operation_label.config(text="")

            case "=":
                if not self.expression:
                    return
                try:
                    result = self.engine.evaluer(self.expression)
                    
                    self.operation_label.config(text=self.expression + " =")
                    self.display_label.config(text=result)
                    
                    # Sauvegarder dans l'historique
                    self.historique.sauvegarder(self.expression, result)
                    
                    self.expression = result
                    self.result_shown = True
                except Exception:
                    self.display_label.config(text="Erreur")
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
                    current = float(self.display_label.cget("text"))
                    if current < 0:
                        raise ValueError

                    result = self.engine.format_number(current ** 0.5)
                    self.display_label.config(text=result)
                    self.operation_label.config(text=f"√({current})")
                    self.expression = result
                    self.result_shown = True
                except Exception:
                    self.display_label.config(text="Erreur")
                    self.expression = ""
                    self.result_shown = True

            case "%":
                try:
                    current = float(self.display_label.cget("text"))
                    percent_value = current / 100
                    self.display_label.config(text=self._format_number(percent_value))
                    self.expression = re.sub(r"(\d+(\.\d+)?)(?!.*\d)", str(percent_value), self.expression)
                    
                except Exception:
                    self.display_label.config(text="Erreur")
                    

            case "+/-":
                txt = self.display_label.cget("text")
                if txt != "0" and txt != "Erreur":
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
                
                # Vérifier la limite de 10 caractères
                if len(current) >= 10:
                    return
                
                if "." not in current:
                    if current == "0":
                        self.display_label.config(text="0.")
                        self.expression += "0."
                    else:
                        self.display_label.config(text=current + ".")
                        self.expression += "."

            case _:  # Chiffres
                if self.result_shown:
                    self.expression = value
                    self.display_label.config(text=value)
                    self.operation_label.config(text=self.expression)
                    self.result_shown = False
                    return

                current = self.display_label.cget("text")
                
                # LIMITATION À 10 CARACTÈRES
                if len(current) >= 10 and current != "0":
                    return
                
                if current == "0":
                    self.display_label.config(text=value)
                else:
                    self.display_label.config(text=current + value)

                self.expression += value
                self.operation_label.config(text=self.expression)


# ============================================
# LANCEMENT
# ============================================

if __name__ == "__main__":
    window = tk.Tk()
    Calculator(window)
    window.mainloop()