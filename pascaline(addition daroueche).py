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
