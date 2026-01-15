
# Point d'entrée de l'application

import tkinter as tk
from interface import Calculator


def main():
    """Fonction principale pour lancer l'application"""
    window = tk.Tk()
    Calculator(window)
    window.mainloop()


if __name__ == "__main__":
    main()