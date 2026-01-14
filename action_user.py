from math_tree import evaluate_simple
import ast

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


def leave():
    out = input("Pour quitter taper q ou Entrée pour continuer vos calculs.")
    return out.lower() == "q"