import dataclasses
import re
from typing import Callable, Set, Dict, Any, List

from mappi.utils import get_expression_variables


@dataclasses.dataclass(frozen=True)
class MappiFunction:
    name: str
    expr: str
    func: Callable
    variables: Set[str]

    @classmethod
    def parse(cls, name: str, expr: str) -> "MappiFunction":
        variables = get_expression_variables(expr)
        if "x" not in variables:
            raise RuntimeError(f"Expression {expr} does not use variable x")
        variables.discard("x")
        other_args = ", ".join(sorted(variables))
        func = eval(f"lambda x, {other_args}: {expr}")
        return MappiFunction(name=name, expr=expr, func=func, variables=variables)

    def substitute(self, values: Dict[str, Any]) -> str:
        expr = self.expr
        for name, value in values.items():
            expr = expr.replace(name, str(value))
        while True:
            old_expr = expr
            # simplify out meaningless operations
            expr = re.sub(r"\s*(?:\||<<|\+|-|^)\s*0", "", expr)
            # simplify out simple parens
            expr = re.sub(r"\(([a-z]+)\)", r"\1", expr)
            if old_expr == expr:
                break
        return expr


@dataclasses.dataclass(frozen=True)
class Result:
    score: int
    func: MappiFunction
    substituted_expression: str
    mapping: dict
    is_ordered: bool

    def format(self) -> str:
        s = f"{self.substituted_expression} mapping {self.mapping}"
        if self.is_ordered:
            s += " (ordered)"
        return s


@dataclasses.dataclass
class Context:
    functions: List[MappiFunction]
    input_values: List[Any]
    output_range: int
    var_min: int
    var_max: int
    time_limit: float
    strict_order: bool
    print_all: bool
