PRESET_FUNCTIONS = {
    "abc": "(x << a) & b ^ c",
    "ab": "(x << a) & b",
    "x+a-b": "x+a-b",
    "x+a+b": "x+a+b",
    "x*a+b": "x*a+b",
    "x*a-b": "x*a-b",
    "xorshift2": "x ^ x << a ^ (x ^ x << a) >> b",
    "xorshift3": "x ^ (x << a) >> b",
    "xorshift": "x ^ (x << a) ^ ((x ^ (x << a)) >> b) ^ ((x ^ (x << a) ^ ((x ^ (x << a)) >> b)) << c)",
}
