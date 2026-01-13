import tkinter as tk
from typing import Optional

# Configuration des couleurs
COLORS = {
    "light_gray": "#D4D4D2",
    "black": "#1C1C1C",
    "dark_gray": "#505050",
    "orange": "#FF9500",
    "white": "white",
    "display_gray": "#888888"
}

# Configuration des boutons
BUTTON_LAYOUT = [
    ["AC", "+/-", "%", "÷"], 
    ["7", "8", "9", "×"], 
    ["4", "5", "6", "-"],
    ["1", "2", "3", "+"],
    ["0", ".", "√", "="]
]

OPERATORS = {"+", "-", "×", "÷"}
SPECIAL_FUNCTIONS = {"AC", "+/-", "%"}

class Calculator:
    def __init__(self, window: tk.Tk):
        self.window = window
        self.a: str = "0"
        self.operator: Optional[str] = None
        self.b: Optional[str] = None
        
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
        """Crée les labels d'affichage"""
        # Affichage de l'opération en cours
        self.operation_label = tk.Label(
            self.frame, 
            text="", 
            font=("Arial", 20), 
            background=COLORS["black"], 
            foreground=COLORS["display_gray"], 
            anchor="e", 
            width=len(BUTTON_LAYOUT[0])
        )
        self.operation_label.grid(row=0, column=0, columnspan=len(BUTTON_LAYOUT[0]), sticky="we")
        
        # Affichage principal
        self.display_label = tk.Label(
            self.frame, 
            text="0", 
            font=("Arial", 45), 
            background=COLORS["black"],
            foreground=COLORS["white"], 
            anchor="e", 
            width=len(BUTTON_LAYOUT[0])
        )
        self.display_label.grid(row=1, column=0, columnspan=len(BUTTON_LAYOUT[0]), sticky="we")
    
    def _create_buttons(self):
        """Crée tous les boutons de la calculatrice"""
        for row_idx, row in enumerate(BUTTON_LAYOUT):
            for col_idx, value in enumerate(row):
                button = tk.Button(
                    self.frame, 
                    text=value, 
                    font=("Arial", 30),
                    width=len(BUTTON_LAYOUT[0]) - 1, 
                    height=1,
                    command=lambda v=value: self.button_clicked(v)
                )
                
                # Configuration des couleurs
                if value in SPECIAL_FUNCTIONS:
                    button.config(foreground=COLORS["black"], background=COLORS["light_gray"])
                elif value in OPERATORS or value == "=":
                    button.config(foreground=COLORS["white"], background=COLORS["orange"])
                else:
                    button.config(foreground=COLORS["white"], background=COLORS["dark_gray"])
                
                button.grid(row=row_idx + 2, column=col_idx)
    
    def _center_window(self):
        """Centre la fenêtre sur l'écran"""
        self.window.update()
        window_width = self.window.winfo_width()
        window_height = self.window.winfo_height()
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        
        x = int((screen_width / 2) - (window_width / 2))
        y = int((screen_height / 2) - (window_height / 2))
        
        self.window.geometry(f"{window_width}x{window_height}+{x}+{y}")
    
    def _update_operation_display(self):
        """Met à jour l'affichage de l'opération en cours"""
        if self.operator and self.a:
            self.operation_label.config(text=f"{self.a} {self.operator}")
        else:
            self.operation_label.config(text="")
    
    def _clear_all(self):
        """Réinitialise toutes les valeurs"""
        self.a = "0"
        self.operator = None
        self.b = None
        self._update_operation_display()
    
    @staticmethod
    def _format_number(num: float) -> str:
        """Formate un nombre en supprimant les décimales inutiles (max 3 décimales)"""
        if num % 1 == 0:
            return str(int(num))
        else:
            # Arrondir à 3 décimales maximum
            rounded = round(num, 3)
            # Supprimer les zéros inutiles à la fin
            return f"{rounded:.3f}".rstrip('0').rstrip('.')
    
    def _calculate(self) -> str:
        """Effectue le calcul en fonction de l'opérateur"""
        num_a = float(self.a)
        num_b = float(self.b)
        
        match self.operator:
            case "+":
                return self._format_number(num_a + num_b)
            case "-":
                return self._format_number(num_a - num_b)
            case "×":
                return self._format_number(num_a * num_b)
            case "÷":
                if num_b == 0:
                    return "Erreur"
                return self._format_number(num_a / num_b)
            case _:
                return "0"
    
    def button_clicked(self, value: str):
        """Gère les clics sur les boutons"""
        match value:
            case "=":
                if self.a and self.operator:
                    self.b = self.display_label.cget("text")
                    result = self._calculate()
                    
                    # Afficher l'opération complète
                    self.operation_label.config(text=f"{self.a} {self.operator} {self.b} =")
                    self.display_label.config(text=result)
                    
                    # Préparer pour la prochaine opération
                    self.a = result
                    self.operator = None
                    self.b = None
            
            case "+" | "-" | "×" | "÷":
                if not self.operator:
                    self.a = self.display_label.cget("text")
                    self.display_label.config(text="0")
                    self.b = "0"
                
                self.operator = value
                self._update_operation_display()
            
            case "AC":
                self._clear_all()
                self.display_label.config(text="0")
            
            case "+/-":
                current = float(self.display_label.cget("text"))
                result = self._format_number(current * -1)
                self.display_label.config(text=result)
            
            case "%":
                current = float(self.display_label.cget("text"))
                result = self._format_number(current / 100)
                self.display_label.config(text=result)
            
            case "√":
                current = float(self.display_label.cget("text"))
                if current < 0:
                    self.display_label.config(text="Erreur")
                else:
                    result = self._format_number(current ** 0.5)
                    self.display_label.config(text=result)
            
            case ".":
                current_text = self.display_label.cget("text")
                if "." not in current_text:
                    self.display_label.config(text=current_text + ".")
            
            case "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9":
                current_text = self.display_label.cget("text")
                if current_text == "0":
                    self.display_label.config(text=value)
                else:
                    self.display_label.config(text=current_text + value)

# Lancement de l'application
if __name__ == "__main__":
    window = tk.Tk()
    calculator = Calculator(window)
    window.mainloop()