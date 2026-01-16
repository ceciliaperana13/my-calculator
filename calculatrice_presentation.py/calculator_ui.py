"""
Interface utilisateur de la calculatrice
"""

import tkinter as tk
import re
from config import COLORS, BUTTON_LAYOUT, OPERATORS, SPECIAL_FUNCTIONS
from calcul_engine import CalculEngine
from historique_manager import HistoriqueManager


class Calculator:
    """Interface graphique de la calculatrice"""
    
    def __init__(self, window: tk.Tk):
        self.window = window
        self.expression = ""
        self.result_shown = False
        
        # Initialiser les composants
        self.engine = CalculEngine()
        self.historique = HistoriqueManager(self.window)
        
        # Créer l'interface
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
        """Crée l'affichage de la calculatrice"""
        # Label pour l'opération en cours
        self.operation_label = tk.Label(
            self.frame,
            text="",
            font=("Arial", 20),
            bg=COLORS["black"],
            fg=COLORS["display_gray"],
            anchor="e"
        )
        self.operation_label.grid(row=0, column=0, columnspan=4, sticky="we")

        # Label pour le résultat principal
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
                if not value:
                    continue
                
                btn = self._create_single_button(value)
                btn.grid(row=r + 2, column=c)

    def _create_single_button(self, value):
        """Crée un bouton individuel avec son style"""
        btn = tk.Button(
            self.frame,
            text=value,
            font=("Arial", 30 if value != "Hist" else 20),
            width=4,
            command=lambda v=value: self.button_clicked(v)
        )
        
        # Appliquer le style approprié
        if value in SPECIAL_FUNCTIONS:
            btn.config(bg=COLORS["light_gray"])
        elif value in OPERATORS or value == "=":
            btn.config(bg=COLORS["blue"], fg="white")
        else:
            btn.config(bg=COLORS["dark_gray"], fg="white")
        
        return btn

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
                self._handle_history()
            case "AC":
                self._handle_clear()
            case "=":
                self._handle_equals()
            case "xʸ":
                self._handle_power()
            case "√":
                self._handle_square_root()
            case "%":
                self._handle_percentage()
            case "+/-":
                self._handle_sign_change()
            case "(" | ")":
                self._handle_parenthesis(value)
            case "+" | "-" | "×" | "÷":
                self._handle_operator(value)
            case ".":
                self._handle_decimal()
            case _:
                self._handle_digit(value)

    def _handle_history(self):
        """Affiche l'historique"""
        self.historique.afficher()

    def _handle_clear(self):
        """Réinitialise la calculatrice"""
        self.expression = ""
        self.result_shown = False
        self.display_label.config(text="0")
        self.operation_label.config(text="")

    def _handle_equals(self):
        """Calcule et affiche le résultat"""
        if not self.expression:
            return
        
        try:
            result = self.engine.evaluer(self.expression)
            self.operation_label.config(text=self.expression + " =")
            self.display_label.config(text=result)
            self.historique.sauvegarder(self.expression, result)
            self.expression = result
            self.result_shown = True
        except Exception:
            self.display_label.config(text="Erreur")
            self.expression = ""
            self.result_shown = True

    def _handle_power(self):
        """Gère l'opération puissance"""
        if self.expression and self.expression[-1] in "+-×÷^":
            self.expression = self.expression[:-1]
        
        self.expression += "^"
        self.operation_label.config(text=self.expression.replace("^", "xʸ"))
        self.display_label.config(text="0")
        self.result_shown = False

    def _handle_square_root(self):
        """Calcule la racine carrée de l'expression actuelle"""
        if not self.expression:
            return
        
        try:
            # Évaluer l'expression actuelle
            result_value = float(self.engine.evaluer(self.expression))
            
            if result_value < 0:
                raise ValueError("Racine carrée d'un nombre négatif")
            
            result = self.engine.format_number(result_value ** 0.5)
            self.operation_label.config(text=f"√({self.expression})")
            self.display_label.config(text=result)
            self.expression = result
            self.result_shown = True
        except Exception:
            self.display_label.config(text="Erreur")
            self.expression = ""
            self.result_shown = True

    def _handle_percentage(self):
        """Calcule le pourcentage - amélioration avec remplacement dans l'expression"""
        try:
            current = float(self.display_label.cget("text"))
            percent_value = current / 100
            formatted_value = self.engine.format_number(percent_value)
            
            self.display_label.config(text=formatted_value)
            
            # Remplacer le dernier nombre dans l'expression par sa valeur en pourcentage
            self.expression = re.sub(
                r"(\d+(\.\d+)?)(?!.*\d)", 
                str(percent_value), 
                self.expression
            )
            
            self.operation_label.config(text=self.expression)
        except Exception:
            self.display_label.config(text="Erreur")
            self.expression = ""
            self.result_shown = True

    def _handle_sign_change(self):
        """Change le signe du nombre affiché"""
        txt = self.display_label.cget("text")
        if txt != "0" and txt != "Erreur":
            if txt.startswith("-"):
                txt = txt[1:]
            else:
                txt = "-" + txt
            self.display_label.config(text=txt)
            self.expression = txt

    def _handle_parenthesis(self, value):
        """Gère les parenthèses"""
        if self.result_shown:
            self.expression = ""
            self.result_shown = False
        
        self.expression += value
        self.operation_label.config(text=self.expression)

    def _handle_operator(self, value):
        """Gère les opérateurs (+, -, ×, ÷)"""
        # Remplacer l'opérateur précédent si présent
        if self.expression and self.expression[-1] in "+-×÷^":
            self.expression = self.expression[:-1]
        
        self.expression += value
        self.display_label.config(text="0")
        self.operation_label.config(text=self.expression)
        self.result_shown = False

    def _handle_decimal(self):
        """Gère le point décimal"""
        current = self.display_label.cget("text")
        
        if "." not in current:
            if current == "0":
                self.display_label.config(text="0.")
                self.expression += "0."
            else:
                self.display_label.config(text=current + ".")
                self.expression += "."

    def _handle_digit(self, value):
        """Gère l'entrée d'un chiffre"""
        if self.result_shown:
            self.expression = value
            self.display_label.config(text=value)
            self.operation_label.config(text=self.expression)
            self.result_shown = False
            return
        
        current = self.display_label.cget("text")
        
        if current == "0":
            self.display_label.config(text=value)
        else:
            self.display_label.config(text=current + value)
        
        self.expression += value
        self.operation_label.config(text=self.expression)