iterlib
======
This library provides composable generator functions which facilitate fancy
iteration patterns with Python.

## Usage:
```python
import iterlib

print(list(iterlib.paired([0, 1, 2, 3])))
# prints [(0, 1), (1, 2), (2, 3)]

print(list(iterlib.chunked([0, 1, 2, 3, 4, 5], 3)))
# prints [(0, 1, 2), (3, 4, 5)]

print(list(iterlib.windowed([0, 1, 2, 3, 4, 5], size=3, step=2, trail=True)))
# prints [(0, 1, 2), (2, 3, 4), (4, 5)]

print(list(iterlib.truncated((i for i in range(6)), 2)))
# prints [0, 1, 2, 3]
```

## Dependencies:
* Python 2.7 - 3.x

## Installation:
```bash
$ python setup.py install
```
