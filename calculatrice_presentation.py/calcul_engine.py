"""
Moteur de calcul pour la calculatrice
"""

from config import MAX_DECIMAL_PLACES, MAX_DISPLAY_LENGTH


class CalculEngine:
    """Moteur de calcul avec évaluation d'expressions"""
    
    def format_number(self, num):
        """Formate un nombre pour l'affichage avec limitation à 10 caractères"""
        # Si c'est un entier
        if num % 1 == 0:
            result = str(int(num))
        else:
            result = f"{round(num, 3):.3f}".rstrip("0").rstrip(".")
        
        # Si le résultat dépasse 10 caractères, utiliser notation scientifique
        if len(result) > MAX_DISPLAY_LENGTH:
            # Notation scientifique avec 3 décimales maximum
            return f"{num:.3e}"
        
        return result
        

    def _tokenize(self, expr):
        """Convertit une expression en tokens"""
        tokens, number, i = [], "", 0
        
        while i < len(expr):
            c = expr[i]
            
            # Gestion du signe négatif
            if c == "-" and (i == 0 or expr[i-1] in "+-×÷(^"):
                if i + 1 < len(expr) and expr[i+1] == "(":
                    tokens.extend(["0", "-"])
                else:
                    number += c
            elif c.isdigit() or c == ".":
                number += c
            else:
                if number:
                    tokens.append(number)
                    number = ""
                tokens.append(c)
            i += 1
        
        if number:
            tokens.append(number)
        
        return tokens

    def _to_rpn(self, tokens):
        """Convertit les tokens en notation polonaise inversée (RPN)"""
        priority = {"+": 1, "-": 1, "×": 2, "÷": 2, "^": 3}
        output, stack = [], []

        for t in tokens:
            if t.replace(".", "", 1).lstrip("-").isdigit():
                output.append(t)
            elif t == "(":
                stack.append(t)
            elif t == ")":
                while stack and stack[-1] != "(":
                    output.append(stack.pop())
                stack.pop()
            else:
                while (stack and stack[-1] != "(" and 
                       priority.get(stack[-1], 0) >= priority.get(t, 0)):
                    output.append(stack.pop())
                stack.append(t)

        while stack:
            output.append(stack.pop())
        
        return output

    def _evaluate_rpn(self, rpn):
        """Évalue une expression en notation polonaise inversée"""
        stack = []
        
        for t in rpn:
            if t.replace(".", "", 1).lstrip("-").isdigit():
                stack.append(float(t))
            else:
                b, a = stack.pop(), stack.pop()
                
                if t == "+":
                    stack.append(a + b)
                elif t == "-":
                    stack.append(a - b)
                elif t == "×":
                    stack.append(a * b)
                elif t == "÷":
                    stack.append(a / b)
                elif t == "^":
                    stack.append(a ** b)
        
        return self.format_number(stack[0])

    def evaluer(self, expression):
        """Évalue une expression mathématique complète"""
        tokens = self._tokenize(expression)
        rpn = self._to_rpn(tokens)
        return self._evaluate_rpn(rpn)