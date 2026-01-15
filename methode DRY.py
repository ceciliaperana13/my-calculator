
# La méthode du **"Chef d'orchestre"** (souvent appelée fonction `main`) est la manière la plus professionnelle d'organiser un code. '
# 'Imaginez que chaque fonction est un ouvrier spécialisé : l'un sait mesurer, l'autre sait couper, '
# 'et le chef d'orchestre leur donne des ordres dans le bon ordre.

# Voici une explication détaillée de comment cela fonctionne pour votre calculatrice :

### 1. On sépare les tâches (Les ouvriers)

# Au lieu d'avoir un seul gros bloc de code, on crée des petites fonctions qui ne font **qu'une seule chose**.


# Ouvrier 1 : Sa seule mission est de récupérer un nombre proprement
def recuperer_entree(message):
    while True:
        try:
            # On utilise float(input()) pour avoir un nombre
            return float(input(message))
        except ValueError:
            print("Erreur : Ce n'est pas un nombre valide.")

# Ouvrier 2 : Sa seule mission est de faire le calcul
def addition(a, b):
    return a + b



### 2. On crée le Chef d'Orchestre (La fonction `main`)

# C'est elle qui va **lier** les ouvriers. Elle prend le résultat de l'un pour le donner à l'autre.

def main():
    print("--- Bienvenue dans ma calculatrice ---")
    
    # Étape 1 : Le chef demande à l'ouvrier 1 de travailler
    nombre1 = recuperer_entree("Entrez votre premier chiffre : ")
    nombre2 = recuperer_entree("Entrez votre deuxième chiffre : ")
    
    # Étape 2 : Le chef donne ces chiffres à l'ouvrier 2 (le calcul)
    resultat = addition(nombre1, nombre2)
    
    # Étape 3 : Le chef affiche le résultat final
    print(f"Le résultat de l'addition est : {resultat}")



### 3. On lance la machine

# À la fin de votre fichier, il suffit d'appeler `main()` pour que tout commence.

# python
# On appelle le chef pour qu'il commence le travail
main()

### Pourquoi est-ce que c'est "lié" ?

# Le lien se fait par les **arguments** et le **`return`** :

# 1. **Le `return` :** C'est la manière dont une fonction "tend" un objet à celui qui l'a appelée. `recuperer_entree` "tend" le nombre au chef d'orchestre.
# 2. **L'argument :** C'est la manière dont le chef "donne" un objet à une fonction. Le chef "donne" `nombre1` et `nombre2` à la fonction `addition`.

# ### Les 3 grands avantages pour vous :

# * **Lisibilité :** En lisant juste la fonction `main`, on comprend tout ce que fait le programme en 5 secondes.
# * **Réutilisation :** Si vous voulez ajouter une soustraction, vous créez juste une fonction `soustraction(a, b)` et vous l'ajoutez dans le `main`. Pas besoin de tout réécrire.
# * **Débogage :** Si le calcul est faux, vous savez que c'est la fonction `addition` qu'il faut réparer. Si le programme plante quand on tape du texte, c'est la fonction `recuperer_entree`.

# **Est-ce que cette logique de "donner et recevoir" des données entre les fonctions est plus claire pour vous ?**