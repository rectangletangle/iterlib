iterlib
======
This library provides composable generator functions which facilitate fancy
iteration patterns with Python. By separating out the iteration related logic,
many algorithms can be expressed in a far more clean and understandable way.
Resulting in improved readability and maintainability.

## Usage:
The library's utility is best shown through example.
```python
import iterlib

# Overlapping pairs `[(0, 1), (1, 2), (2, 3)]`
print(list(iterlib.paired([0, 1, 2, 3])))

# Non-overlapping chunks `[(0, 1, 2), (3, 4, 5)]`
print(list(iterlib.chunked([0, 1, 2, 3, 4, 5], 3)))

# The `windowed` function allows for a substantial amount of control over
# iteration. The `partial` argument determines if undersized trailing chunks
# are yielded. This prints `[(0, 1, 2), (2, 3, 4), (4, 5)]`.
print(list(iterlib.windowed([0, 1, 2, 3, 4, 5], size=3, step=2, partial=True)))

# This prints `[(0, 1), (3, 4)]`
print(list(iterlib.windowed(range(7), size=2, step=3, partial=False)))

# A flattened list `[0, 1, 2, 3]`
nested = [[[0]], [1, [2]], [3]]
print(list(iterlib.flattened(nested)))

# Notice that the input to `truncated` is a generator, internally the function
# does not convert the input into a list, saving memory. Yet items at the end
# are still removed. This prints `[0, 1, 2, 3]`.
print(list(iterlib.truncated((i for i in range(6)), 2)))
```
Although lists are used for input in most of the examples above, the functions
were purposely designed to work with any object that has an `__iter__` method.
This allows the functions to operate on a wide variety of Python objects, not
just those that support the slice notation.

## Dependencies:
This library supports both Python versions 2 and 3 with a single mutually
intelligible source.
* Python 2.7 - 3.x

## Installation:
```bash
$ python setup.py install
```
