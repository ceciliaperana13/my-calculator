"""
Configuration de la calculatrice
"""

COLORS = {
    "light_gray": "#D4D4D2",
    "black": "#1C1C1C",
    "dark_gray": "#505050",
    "blue": "#043A5C",
    "white": "#FFFFFF",
    "display_gray": "#888888",
    "red": "#C41E3A",
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

# Limites d'affichage
MAX_DECIMAL_PLACES = 6
MAX_DISPLAY_LENGTH = 10  # Longueur maximale avant notation scientifique
MAX_HISTORY_ENTRIES = 50