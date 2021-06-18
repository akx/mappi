# mappi

Mappi finds (Python – portability not guaranteed) expressions that map a given range of input values
(likely integers) to a linear output range.

The output of the expressions generated are unspecified for any other input value.

## usage

Requires Python 3.7+.

Spend up to 5 seconds finding a function that maps [10, 32, 35] to 0..2:

```shell
$ python3 -m mappi --default-functions --input 10,32,35 --time-limit=5

=== BEST RESULT ===
Original:   (x << a) & b
Expression: (x & 9) % 3
Mapping:    {10: 2, 32: 0, 35: 1}
```

Spend up to 5 seconds finding a function that maps [1,3,5,7,19] to 0..4 in the same order:

```shell
$ python3 -m mappi --default-functions --input 1,3,5,7,19 --time-limit=5 --strict-order

=== BEST RESULT ===
Original:   x*a+b
Expression: (x*3+2) % 5
Mapping:    {1: 0, 3: 1, 5: 2, 7: 3, 19: 4}
```
