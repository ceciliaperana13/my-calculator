def priority(op):
    if op in ("+", "-"):
        return 1
    if op in ("*", "/"):
        return 2
    return 0
()

def tokenize(expression):
    tokens = []
    number = ""

    for char in expression:
        if char.isdigit() or char == ".":
            number += char
        elif char in "+-*/()":
            if number != "":
                tokens.append(float(number))
                number = ""
            tokens.append(char)
        elif char == " ":
            continue
        else:
            raise ValueError(f"Invalid character: {char}")

    if number != "":
        tokens.append(float(number))

    return tokens
