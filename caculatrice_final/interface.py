
import tkinter as tk
from config import COLORS, BUTTON_LAYOUT, OPERATORS, SPECIAL_FUNCTIONS
from calcul_engine import CalculEngine
from historique import HistoriqueManager


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

                #style de boutons
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

            case "(" | ")":
                if self.result_shown:
                    self.expression = ""
                    self.result_shown = False

                self.expression += value
                self.operation_label.config(text=self.expression)

            case "√":
                try:
                    current = float(self.display_label.cget("text"))
                    if current < 0:
                        raise ValueError

                    result = self.engine.format_number(current ** 0.5)
                    self.display_label.config(text=result)
                    self.expression = result
                    self.operation_label.config(text=result)
                    self.result_shown = True
                except Exception:
                    self.display_label.config(text="Erreur")
                    self.expression = ""
                    self.result_shown = True

            case "%":
                try:
                    current = float(self.display_label.cget("text"))
                    result = self.engine.format_number(current / 100)
                    self.display_label.config(text=result)
                    self.expression = result
                    self.operation_label.config(text=self.expression)
                    self.result_shown = True
                except Exception:
                    self.display_label.config(text="Erreur")
                    self.expression = ""
                    self.result_shown = True

            case "+" | "-" | "×" | "÷":
                self.result_shown = False
                if self.expression and self.expression[-1] in "+-×÷":
                    self.expression = self.expression[:-1]
                self.expression += value
                self.operation_label.config(text=self.expression)
                self.display_label.config(text="0")

            case ".":
                current = self.display_label.cget("text")
                if "." not in current:
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
                if current == "0":
                    self.display_label.config(text=value)
                else:
                    self.display_label.config(text=current + value)

                self.expression += value
                self.operation_label.config(text=self.expression)