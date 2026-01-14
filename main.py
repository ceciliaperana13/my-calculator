from action_user import user_input, symbol_input, leave
from treatment import (
    treatment,
    treatmentmul,
    treatmentdiv,
    treatmentsub,
    treatmentpower,
)
from history import listener


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
