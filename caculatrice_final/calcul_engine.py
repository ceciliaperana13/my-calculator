
class CalculEngine:
    """Moteur de calcul pour évaluer les expressions mathématiques"""
    
    @staticmethod
    def format_number(num: float) -> str:
        """Formate un nombre pour l'affichage"""
        if num % 1 == 0:
            return str(int(num))
        return f"{round(num, 3):.3f}".rstrip("0").rstrip(".")

    @staticmethod
    def tokenize(expr: str):
        """Découpe l'expression en tokens"""
        tokens = []
        number = ""
        i = 0

        while i < len(expr):
            c = expr[i]

            if c.isdigit() or c == ".":
                number += c

            elif c == "-" and (i == 0 or expr[i-1] in "+-×÷("):
                number += c  # signe négatif

            else:
                if number:
                    tokens.append(number)
                    number = ""
                tokens.append(c)

            i += 1

        if number:
            tokens.append(number)

        return tokens

    @staticmethod
    def to_rpn(tokens):
        
        priority = {"+": 1, "-": 1, "×": 2, "÷": 2}
        output = []
        stack = []

        for t in tokens:
            if t.replace(".", "", 1).lstrip("-").isdigit():
                output.append(t)

            elif t == "(":
                stack.append(t)

            elif t == ")":
                while stack and stack[-1] != "(":
                    output.append(stack.pop())
                stack.pop()  # retire "("

            else:  # opérateur
                while (
                    stack
                    and stack[-1] != "("
                    and priority.get(stack[-1], 0) >= priority[t]
                ):
                    output.append(stack.pop())
                stack.append(t)

        while stack:
            output.append(stack.pop())

        return output

    @staticmethod
    def evaluate_rpn(rpn):
       
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
                    if b == 0:
                        raise ZeroDivisionError
                    stack.append(a / b)
        return CalculEngine.format_number(stack[0])

    @staticmethod
    def evaluer(expression: str) -> str:
        """Évalue une expression mathématique complète"""
        tokens = CalculEngine.tokenize(expression)
        rpn = CalculEngine.to_rpn(tokens)
        return CalculEngine.evaluate_rpn(rpn)