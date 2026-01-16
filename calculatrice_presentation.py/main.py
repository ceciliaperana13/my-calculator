"""
Point d'entrée principal de l'application calculatrice
"""

import tkinter as tk
from calculator_ui import Calculator


def main():
    """Lance l'application calculatrice"""
    window = tk.Tk()
    Calculator(window)
    window.mainloop()


if __name__ == "__main__":
    main()