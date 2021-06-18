import argparse
import ast
import json
from typing import List, Any

from mappi.finder import find_results
from mappi.models import MappiFunction, Context
from mappi.presets import PRESET_FUNCTIONS


def parse_input_values(s: str) -> List[Any]:
    try:
        return list(json.loads(s))
    except ValueError:
        pass
        try:
            return list(ast.literal_eval(s))
        except ValueError:
            raise ValueError(
                "Unable to interpret input values as JSON or Python expression",
            )


def get_functions(
    functions: List[str], default_functions: bool = False
) -> List[MappiFunction]:
    function_map = {}
    if default_functions:
        function_map.update(PRESET_FUNCTIONS)
    for func in functions:
        if func in PRESET_FUNCTIONS:
            function_map[func] = PRESET_FUNCTIONS[func]
        else:
            function_map[func] = func
    return [MappiFunction.parse(name, func) for (name, func) in function_map.items()]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True, type=parse_input_values)
    ap.add_argument("--strict-order", action="store_true", default=False)
    ap.add_argument("--function", dest="functions", nargs="*", default=[])
    ap.add_argument("--default-functions", action="store_true")
    ap.add_argument("--var-min", type=int, default=0)
    ap.add_argument("--var-max", type=int, default=255)
    ap.add_argument("--time-limit", type=float, default=30)
    args = ap.parse_args()
    context = Context(
        functions=get_functions(
            args.functions, default_functions=args.default_functions
        ),
        input_values=args.input,
        output_range=len(args.input),
        var_min=args.var_min,
        var_max=args.var_max,
        time_limit=args.time_limit,
        strict_order=args.strict_order,
    )
    if not context.functions:
        ap.error("No functions (use --function or --default-functions)")

    print(f"Input values: {context.input_values}")
    print(f"Output range: 0..{context.output_range - 1}")
    print(f"Using {len(context.functions)} functions")

    results, interrupted = find_results(context)

    if results:
        result = results[-1]
        print("=== BEST RESULT ===")
        print("Original:  ", result.func.expr)
        print("Expression:", result.substituted_expression)
        print("Mapping:   ", result.mapping)
    else:
        print("No results :(")
