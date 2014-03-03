iterlib
======
This library provides composable generator functions which facilitate fancy
iteration patterns with Python.

## Usage:
The library's utility is best shown through example.

Although lists are used for input in most of the functions below, the functions
were purposely designed to work with any object that has an `__iter__` method. 
This allows the functions to operate on a wide variety of Python objects, not 
just those that support the slice notation.
```python
import iterlib

print(list(iterlib.paired([0, 1, 2, 3])))
# prints [(0, 1), (1, 2), (2, 3)]

print(list(iterlib.chunked([0, 1, 2, 3, 4, 5], 3)))
# prints [(0, 1, 2), (3, 4, 5)]

print(list(iterlib.windowed([0, 1, 2, 3, 4, 5], size=3, step=2, partial=True)))
# prints [(0, 1, 2), (2, 3, 4), (4, 5)]

print(list(iterlib.windowed(list(range(7)), size=2, step=3, partial=False)))
# prints [(0, 1), (3, 4)]

print(list(iterlib.truncated((i for i in range(6)), 2)))
# prints [0, 1, 2, 3]

nested = [[[0]], [1, [2]], [3]]
print(list(iterlib.flattened(nested)))
# prints [0, 1, 2, 3]
```

## Dependencies:
This library supports both Python version 2 and 3 with a single source.
* Python 2.7 - 3.x

## Installation:
```bash
$ python setup.py install
```
