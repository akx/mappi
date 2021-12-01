import itertools
import random
import time
from typing import Optional, Tuple, List, Set

from mappi.models import MappiFunction, Result, Context


def test_func(
    context: Context,
    func: MappiFunction,
) -> Optional[Result]:
    values = {
        name: context.generate_value()
        for name in func.variables
    }
    try:
        vals = {
            x: func.func(x, **values) % context.output_range
            for x in context.input_values
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
    seen_exprs: Set[str] = set()
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
                if (
                    not results
                    or result.score < results[-1].score
                    and result.substituted_expression not in seen_exprs
                ):
                    print("FOUND:", result.format())
                    results.append(result)
                    seen_exprs.add(result.substituted_expression)
                elif context.print_all:
                    print(".....", result.format())
        except KeyboardInterrupt:
            print()
            return (results, True)
    return (results, False)
