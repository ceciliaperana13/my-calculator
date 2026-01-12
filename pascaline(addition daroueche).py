# addition
def addition():
    val1 = float(input("Choisissez un chiffre ou nombre :"))
    val2 = float(input("Choisissez un deuxieme chiffre ou nombre :"))
    result = val1 + val2
    print(result)
try:
        val1 = float(input("Choisissez un chiffre ou nombre :"))
        val2 = float(input("Choisissez un deuxieme chiffre ou nombre :"))
except:
      print("Erreur veuillez entrer un chiffre ou nombre")

addition()
