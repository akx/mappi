import ast
from typing import Set


def get_expression_variables(expr: str) -> Set[str]:
    variables = set()
    t = ast.parse(expr, "<expr>", "eval")
    for node in ast.walk(t):
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
            variables.add(node.id)
    return variables
