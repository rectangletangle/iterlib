

import unittest

from iterlib import windowed, chunked, chop, paired, united, truncated, flattened

class _TestIter(unittest.TestCase):
    def assert_iter_equal(self, iterable, list_):
        self.assertEqual(list(iterable), list_)

class TestWindowed(_TestIter):
    def test_empty(self):
        self.assert_iter_equal(windowed(range(0), 1), [])
        self.assert_iter_equal(windowed(range(0), 3, 2), [])
        self.assert_iter_equal(windowed(range(0), 30000, 2312), [])

    def test_single(self):
        self.assert_iter_equal(windowed(range(1), 1), [(0,)])
        self.assert_iter_equal(windowed(range(1), 2), [])
        self.assert_iter_equal(windowed(range(1), 1, 2), [(0,)])

    def test_windows_of_one(self):
        self.assert_iter_equal(windowed(range(6), 1), [(0,), (1,), (2,), (3,), (4,), (5,)])

    def test_trail(self):
        self.assert_iter_equal(windowed(range(4), 3, trail=True), [(0, 1, 2), (1, 2, 3), (2, 3), (3,)])
        self.assert_iter_equal(windowed(range(4), 3, 2, trail=True), [(0, 1, 2), (2, 3)])
        self.assert_iter_equal(windowed(range(4), 3, 3, trail=True), [(0, 1, 2), (3,)])

    def test_evenly_divisible(self):
        self.assert_iter_equal(windowed(range(6), 3, 3), [(0, 1, 2), (3, 4, 5)])
        self.assert_iter_equal(windowed(range(9), 3, 3), [(0, 1, 2), (3, 4, 5), (6, 7, 8)])

    def test_not_evenly_divisible(self):
        correct = [(0, 1, 2), (3, 4, 5)]
        self.assert_iter_equal(windowed(range(7), 3, 3), correct)
        self.assert_iter_equal(windowed(range(8), 3, 3), correct)

    def test_overlapping(self):
        self.assert_iter_equal(windowed(range(6), 3, 2), [(0, 1, 2), (2, 3, 4)])
        self.assert_iter_equal(windowed(range(7), 3, 2), [(0, 1, 2), (2, 3, 4), (4, 5, 6)])

class TestChunked(_TestIter):
    ...

##    ut.assert_equal(list(chunked(range(7), 3)), [(0, 1, 2), (3, 4, 5)] )
##    ut.assert_equal(list(chunked(range(6), 3)), [(0, 1, 2), (3, 4, 5)] )
##    ut.assert_equal(list(chunked(range(2), 3)), []                     )
##    ut.assert_equal(list(chunked(range(0), 3)), []                     )
##
##    ut.assert_equal(list(chunked(range(4), 3, trail=True)), [(0, 1, 2), (3,)])
##    ut.assert_equal(list(chunked(range(2), 3, trail=True)), [(0, 1)])
##
##    size = 3
##    ut.assert_equal(list(chop(windowed(range(4), size, 1), size)), [(0, 1, 2), (1, 2, 3)] )
##    ut.assert_equal(list(chop(chunked(range(7), size), size)),     [(0, 1, 2), (3, 4, 5)] )
##    ut.assert_equal(list(chop(paired([0]), 1)), [])
##    ut.assert_equal(list(chop(paired([0]), 0)), [])
##    ut.assert_equal(list(chop(paired([0]), -1)), [])
##
##    def generates_something () :
##        i = 0
##        while True :
##            yield i
##            i += 1
##
##    def generates_nothing () :
##        for _ in () :
##            yield
##
##    ut.assert_true(generates(generates_nothing()) is None)
##    ut.assert_doesnt_raise(lambda : next(generates(generates_something())), StopIteration)
##    ut.assert_doesnt_raise(lambda : next(generates_something()), StopIteration)
##    ut.assert_raises(lambda : next(generates_nothing()), StopIteration)
##
##    ut.assert_equal(list(truncated([], 1)),          []              )
##    ut.assert_equal(list(truncated(range(4), 1)),    [0, 1, 2]       )
##    ut.assert_equal(list(truncated(range(10), 4)),   list(range(6))  )
##    ut.assert_equal(list(truncated(range(10), 0)),   list(range(10)) )
##    ut.assert_equal(list(truncated(range(10), -1)),  list(range(10)) )
##    ut.assert_equal(list(truncated(range(10), -34)), list(range(10)) )
##    ut.assert_equal(list(truncated(range(10), 34)),  []              )
##    ut.assert_equal(list(truncated(range(10), 10)),  []              )
##
##    ut.assert_equal(list(paired([])),       []                               )
##    ut.assert_equal(list(paired([0])),      []                               )
##    ut.assert_equal(list(paired(range(4))), [(0, 1), (1, 2), (2, 3)]         )
##    ut.assert_equal(list(paired(range(5))), [(0, 1), (1, 2), (2, 3), (3, 4)] )
##
##    ut.assert_equal(list(united(paired([]))),        []              )
##    ut.assert_equal(list(united(paired([0]))),       []              )
##    ut.assert_equal(list(united(paired([0, 1]))),    [0, 1]          )
##    ut.assert_equal(list(united(paired(range(3)))),  list(range(3))  )
##    ut.assert_equal(list(united(paired(range(12)))), list(range(12)) )
##
##    ut.assert_equal(list(flattened([])),                     []           )
##    ut.assert_equal(list(flattened([[], [[], []]])),         []           )
##    ut.assert_equal(list(flattened([[[0]], [1, [2]], [3]])), [0, 1, 2, 3] )
##    ut.assert_equal(list(flattened([[(0,)], [(1,), [], []], (2,)],
##                                   basecase=lambda iterable : isinstance(iterable, tuple))),
##                    [(0,), (1,), (2,)])


if __name__ == '__main__':
    unittest.main()

