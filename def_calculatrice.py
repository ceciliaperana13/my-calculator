def priority(op):
    # Return operator priority
    if op in ("+", "-"):
        return 1
    if op in ("*", "/"):
        return 2
    return 0


def tokenize(expression):
    # Convert the input string into a list of numbers and operators
    tokens = []
    number = ""
    prev_char = None

    for char in expression:
        # Build multi-digit (or decimal) numbers
        if char.isdigit() or char == ".":
            number += char

        # Handle negative numbers (unary minus)
        elif char == "-" and (prev_char is None or prev_char in "+-*/("):
            number += char

        # Handle operators and parentheses
        elif char in "+*/()":
            if number != "":
                tokens.append(float(number))
                number = ""
            tokens.append(char)

        # Ignore spaces
        elif char == " ":
            pass

        # Invalid character
        else:
            raise ValueError(f"Invalid character: {char}")

        prev_char = char

    # Append the last number if it exists
    if number != "":
        tokens.append(float(number))

    return tokens


def infix_to_postfix(tokens):
    # Convert infix expression to postfix (Reverse Polish Notation)
    output = []
    stack = []

    for token in tokens:
        # If token is a number, add it to the output
        if isinstance(token, float):
            output.append(token)

        # If token is an operator
        elif token in "+-*/":
            while (stack and stack[-1] != "(" and
                   priority(stack[-1]) >= priority(token)):
                output.append(stack.pop())
            stack.append(token)

        # If token is an opening parenthesis
        elif token == "(":
            stack.append(token)

        # If token is a closing parenthesis
        elif token == ")":
            while stack and stack[-1] != "(":
                output.append(stack.pop())
            if not stack:
                raise ValueError("Closing parenthesis without opening one.")
            stack.pop()  # Remove "(" from stack

    # Pop remaining operators from the stack
    while stack:
        if stack[-1] == "(":
            raise ValueError("Opening parenthesis without closing one.")
        output.append(stack.pop())

    return output


def evaluate_postfix(postfix):
    # Evaluate a postfix expression
    stack = []

    for token in postfix:
        # Push numbers onto the stack
        if isinstance(token, float):
            stack.append(token)
        else:
            # An operator needs two operands
            if len(stack) < 2:
                raise ValueError("Invalid expression.")

            b = stack.pop()
            a = stack.pop()

            # Perform the operation
            if token == "+":
                stack.append(a + b)
            elif token == "-":
                stack.append(a - b)
            elif token == "*":
                stack.append(a * b)
            elif token == "/":
                if b == 0:
                    raise ZeroDivisionError("Division by zero is not allowed.")
                stack.append(a / b)

    # Final result should be the only value left
    if len(stack) != 1:
        raise ValueError("Invalid expression.")

    return stack[0]


def calculator():
    # Main calculator function
    try:
        expression = input("Enter a mathematical expression: ")
        tokens = tokenize(expression)
        postfix = infix_to_postfix(tokens)
        result = evaluate_postfix(postfix)

        # Display result without .0 if it is an integer
        if result.is_integer():
            print("Result:", int(result))
        else:
            print("Result:", result)

    except Exception as error:
        print("Error:", error)


calculator()
