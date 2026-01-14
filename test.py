# Method DRY test

# AST Abstract Syntax Tree or Arbre de Syntaxe Abstraite is the method that Python use for understand the code
import ast

# Operator has the functions who make the samething that the symbols mathematic
import operator

# Import Pynput
from pynput import keyboard

# Import datetime
from datetime import datetime


with open("log_calculatrice.txt", "a") as f:
    f.write(
        f"--- Session débutée le {datetime.now().strftime('%d/%m/%Y à %H:%M:%S')} ---\n"
    )


# --- Log Config ---
def on_press(key):
    try:
        # On récupère l'heure actuelle au format HH:MM:SS
        heure = datetime.now().strftime("%H:%M:%S")

        with open("log_calculatrice.txt", "a") as f:
            if hasattr(key, "char") and key.char is not None:
                # On écrit : [14:30:05] Touche: a
                f.write(f"[{heure}] Touche: {key.char}\n")
            elif key == keyboard.Key.enter:
                f.write(f"[{heure}] Touche: ENTREE\n")
            elif key == keyboard.Key.space:
                f.write(f"[{heure}] Touche: ESPACE\n")
            # On peut ignorer le reste pour ne pas polluer le fichier
    except Exception:
        pass

    # Launch of the listener in mode "not-blocking"


listener = keyboard.Listener(on_press=on_press)
listener.start()

# Defined the tools allowed (very secure)
OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
}


def evaluate_simple(node):
    """Recursive calcul for the mathematic tree"""
    if isinstance(node, ast.Constant):
        return node.value
    elif isinstance(node, ast.BinOp):
        return OPERATORS[type(node.op)](
            evaluate_simple(node.left), evaluate_simple(node.right)
        )
    raise ValueError("Expression not supported")


# the function for choose the digits and the numbers


def user_input(message):
    while True:
        writing = input(message)
        try:
            # ast.parse transform "(5+5)" in an structure that Python understand
            tree = ast.parse(writing, mode="eval")
            return float(evaluate_simple(tree.body))
        except (SyntaxError, KeyError, ValueError, AttributeError):
            print("Erreur : Entrez un nombre ou une expression valide.")


# the function for choose the symbols


def symbol_input(message):
    sign = "+", "*", "/", "-", "**"
    try:
        while True:
            seizure = input(message)
            if seizure in sign:
                return seizure
    except:
        print(
            "Erreur : le caractère n'est pas un symbole accepté, veuillez choisir entre (+, -, /, * ou **)  ."
        )


# The functions for the treatments of the types of the operations


def treatment(val1, val2):
    return val1 + val2


def treatmentmul(val1, val2):
    return val1 * val2


def treatmentdiv(val1, val2):
    return val1 / val2


def treatmentsub(val1, val2):
    return val1 - val2


def treatmentpower(val1, val2):
    return val1**val2


# The function for leave with letter q lower


def leave():
    out = input("Pour quitter taper q ou Entrée pour continuer vos calculs.")
    return out.lower() == "q"


# the loop main


def main():
    while True:
        # the display of the welcome sentence
        print("-------------| CALCULATRICE PASCALINE v1.0 |-----------------")
        print(
            "-------------| Pour quitter taper Q minuscule à la fin de votre calcul |--------------"
        )
        print(
            "-------------| Si vous souhaitez continuer vos calculs à la fin de la boucle taper Entrée |------------------"
        )

        # the choice the numbers and the symbols
        nombre1 = user_input("Entrez un chiffre ou nombre :")
        operation = symbol_input("Choisissez un symbole + | * | / | - | ** :")
        nombre2 = user_input("Entrez un chiffre ou nombre :")
        # the loop try, for verify if the variable operation is / and nombre2 is 0,
        # if is that the user need choose an other digit or number

        while operation == "/" and nombre2 == 0:
            print("Erreur, 0 n'est pas un diviseur")
            nombre2 = user_input("Entrez un chiffre ou nombre valide :")

        # the conditions for the operations related with their symbols
        if operation == "+":
            print(treatment(nombre1, nombre2))
        if operation == "*":
            print(treatmentmul(nombre1, nombre2))
        if operation == "/":
            print(treatmentdiv(nombre1, nombre2))
        if operation == "-":
            print(treatmentsub(nombre1, nombre2))
        if operation == "**":
            print(treatmentpower(nombre1, nombre2))

        # It's for stop the loop while with the lower letter q or continue with Enter
        if leave():
            print("Merci d'avoir utiliser la Calculatrice Pascaline v1.0")
            # Stop the listener cleanly at the end
            listener.stop()
            break


# activation of the loop
main()
