def priority(op):
    # Return operator precedence
    if op in ("+", "-"):
        return 1
    if op in ("*", "/"):
        return 2
    return 0


def tokenize(expression):
    # Convert the input string into a list of numbers and operators
    tokens = []
    number = ""

    for char in expression:
        # Build multi-digit (or decimal) numbers
        if char.isdigit() or char == ".":
            number += char

        # Handle operators and parentheses
        elif char in "+-*/()":
            if number != "":
                tokens.append(float(number))
                number = ""
            tokens.append(char)

        # Ignore spaces
        elif char == " ":
            continue

        # Invalid character
        else:
            raise ValueError(f"Invalid character: {char}")

    # Append the last number if it exists
    if number != "":
        tokens.append(float(number))

    return tokens
