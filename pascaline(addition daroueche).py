#addition
def addition():
    result = val1 + val2
    print(result)

while True:
    try:
        val1 = float(input("Choisissez un chiffre ou nombre : "))
        val2 = float(input("Choisissez un deuxième chiffre ou nombre : "))
        break
    except:
        print("Erreur : veuillez entrer un chiffre ou un nombre.")

addition()



# probleme recontré :
# lors de l'ajout de la fonction try/except, la saisie se faisait 4 fois
# 2 fois dans la fonction et 2 fois dans la fonction try/except
# solution : laisser seulement la saisie dans la fonction try/Except 