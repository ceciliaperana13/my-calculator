# AST Abstract Syntax Tree or Arbre de Syntaxe Abstraite is the method that Python use for understand the code
import ast

# Operator has the functions who make the samething that the symbols mathematic
import operator


# Defined the tools allowed (very secure)
OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
}


def evaluate_simple(node):
    """Recursive calcul for the mathematic tree"""
    if isinstance(node, ast.Constant):
        return node.value
    elif isinstance(node, ast.BinOp):
        return OPERATORS[type(node.op)](
            evaluate_simple(node.left), evaluate_simple(node.right)
        )
    raise ValueError("Expression not supported")