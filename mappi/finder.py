import itertools
import random
import time
from typing import Optional, Tuple, List

from mappi.models import MappiFunction, Result, Context


def test_func(
    context: Context,
    func: MappiFunction,
) -> Optional[Result]:
    values = {
        name: random.randint(context.var_min, context.var_max)
        for name in func.variables
    }
    try:
        vals = {
            x: func.func(x, **values) % context.output_range for x in context.input_values
        }
    except ZeroDivisionError:
        return None
    if len(set(vals.values())) == context.output_range:
        substituted_expression = f"({func.substitute(values)}) % {context.output_range}"
        verify_func = eval(f"lambda x: {substituted_expression}")
        is_ordered = all(
            verify_func(iv) == i for (i, iv) in enumerate(context.input_values)
        )
        if context.strict_order and not is_ordered:
            return None
        assert len(set(verify_func(iv) for iv in context.input_values)) == len(
            context.input_values
        )
        return Result(
            score=len(substituted_expression),
            func=func,
            substituted_expression=substituted_expression,
            mapping=vals.copy(),
            is_ordered=is_ordered,
        )
    return None


def find_results(context: Context) -> Tuple[List[Result], bool]:
    results: List[Result] = []
    last_print_time = init_time = time.time()
    for attempt in itertools.count():
        try:
            if attempt % 100 == 0:
                now = time.time()
                if now - init_time > context.time_limit:
                    print("Time limit reached.")
                    break
                if now - last_print_time > 1:
                    last_print_time = now
                    print(
                        f"{attempt} attempts, {len(results)} candidates found in {now - init_time:.2f}s ..."
                    )

            result = test_func(
                context,
                random.choice(context.functions),
            )
            if result:
                if not results or result.score < results[-1].score:
                    print("FOUND:", result.format())
                    results.append(result)
        except KeyboardInterrupt:
            print()
            return (results, True)
    return (results, False)
