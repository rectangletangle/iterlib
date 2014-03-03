
import unittest

from iterlib import windowed, chunked, chopped, head, tail, skipped, truncated, paired, united, flattened, generates

class _TestIter(unittest.TestCase):
    def assert_iter_equal(self, iterable, list_):
        self.assertEqual(list(iterable), list_)

class TestWindowed(_TestIter):
    def test_empty(self):
        for size in [0, 1, 234]:
            for null in [0, None, -1]:
                windows = [windowed(range(size), null),
                           windowed(range(size), null, null),
                           windowed(range(size), null, 1),
                           windowed(range(size), 1, null)]

                for window in windows:
                    self.assert_iter_equal(window, [])

        windows = [windowed(range(0), 1),
                   windowed(range(0), 3, 2),
                   windowed(range(0), 30000, 2312)]

        for window in windows:
            self.assert_iter_equal(window, [])

    def test_single(self):
        self.assert_iter_equal(windowed(range(1), 1), [(0,)])
        self.assert_iter_equal(windowed(range(1), 2), [])
        self.assert_iter_equal(windowed(range(1), 1, 2), [(0,)])

    def test_windows_of_one(self):
        self.assert_iter_equal(windowed(range(6), 1), [(0,), (1,), (2,), (3,), (4,), (5,)])

    def test_partial(self):
        self.assert_iter_equal(windowed(range(4), 3, partial=True), [(0, 1, 2), (1, 2, 3), (2, 3), (3,)])
        self.assert_iter_equal(windowed(range(4), 3, 2, partial=True), [(0, 1, 2), (2, 3)])
        self.assert_iter_equal(windowed(range(4), 3, 3, partial=True), [(0, 1, 2), (3,)])
        self.assert_iter_equal(windowed(range(7), 3, 5, partial=True), [(0, 1, 2), (5, 6)])

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

        self.assert_iter_equal(windowed(range(7), 3, 4), [(0, 1, 2), (4, 5, 6)])
        self.assert_iter_equal(windowed(range(8), 3, 4), [(0, 1, 2), (4, 5, 6)])
        self.assert_iter_equal(windowed(range(11), 3, 4), [(0, 1, 2), (4, 5, 6), (8, 9, 10)])

class TestChunked(_TestIter):
    def test_empty(self):
        chunks = [chunked(range(0), 0),
                  chunked(range(0), -1),
                  chunked(range(0), None),
                  chunked(range(0), 3),
                  chunked(range(0), 3, partial=True)]

        for chunk in chunks:
            self.assert_iter_equal(chunk, [])

    def test_single(self):
        self.assert_iter_equal(chunked(range(1), 1), [(0,)])
        self.assert_iter_equal(chunked(range(1), 2), [])

    def test_partial(self):
        self.assert_iter_equal(chunked(range(4), 3, partial=True), [(0, 1, 2), (3,)])
        self.assert_iter_equal(chunked(range(2), 3, partial=True), [(0, 1)])

    def test_no_partial(self):
        self.assert_iter_equal(chunked(range(7), 3), [(0, 1, 2), (3, 4, 5)])
        self.assert_iter_equal(chunked(range(6), 3), [(0, 1, 2), (3, 4, 5)])
        self.assert_iter_equal(chunked(range(2), 3), [])

class TestChopped(_TestIter):
    def test_empty(self):
        for value in [-1, None, 0, 1]:
            self.assert_iter_equal(chopped(paired(range(0)), value), [])

    def test_values(self):
        for value in [-1, 1, 10]:
            for input_ in [-1, None, 0]:
                self.assert_iter_equal(chopped(paired(range(value)), input_), [])

    def test_chop_partial(self):
        size = 3
        self.assert_iter_equal(chopped(windowed(range(4), size, 1, partial=True), size), [(0, 1, 2), (1, 2, 3)])
        self.assert_iter_equal(chopped(chunked(range(7), size, partial=True), size), [(0, 1, 2), (3, 4, 5)])

class _CommonLimitTests:
    def test_empty(self):
        for input_ in [None, 0, 1, 12]:
            self.assert_iter_equal(self.function(range(0), input_), [])

    def test_exceptions(self):
        self.assertRaises(ValueError, lambda: list(self.function(range(0), -1)))
        self.assertRaises(ValueError, lambda: list(self.function(range(313), -1)))
        self.assertRaises(ValueError, lambda: list(self.function(range(0), 23.123)))

    def test_other(self, outputs):
        for input_, output in zip([None, 0, 1, 2], outputs):
            self.assert_iter_equal(self.function(range(10), input_), output)

class _CommonOuterTests(_CommonLimitTests):
    def test_single(self):
        for input_, correct in [(0, []), (1, [0]), (2, [0])]:
            self.assert_iter_equal(self.function(range(1), input_), correct)

class TestHead(_CommonOuterTests, _TestIter):
    def function(self, *args, **kw):
        return head(*args, **kw)

    def test_other(self):
        lst = list(range(10))
        _CommonOuterTests.test_other(self, [lst, [], lst[:1], lst[:2]])

class TestTail(_CommonOuterTests, _TestIter):
    def function(self, *args, **kw):
        return tail(*args, **kw)

    def test_other(self):
        lst = list(range(10))
        _CommonOuterTests.test_other(self, [lst, [], lst[-1:], lst[-2:]])

class _CommonInnerTests(_CommonLimitTests):
    def test_single(self):
        for input_, correct in [(0, [0]), (1, []), (2, [])]:
            self.assert_iter_equal(self.function(range(1), input_), correct)

class TestSkipped(_CommonInnerTests, _TestIter):
    def function(self, *args, **kw):
        return skipped(*args, **kw)

    def test_other(self):
        lst = list(range(10))
        _CommonInnerTests.test_other(self, [lst, lst, lst[1:], lst[2:]])

class TestTruncated(_CommonInnerTests, _TestIter):
    def function(self, *args, **kw):
        return truncated(*args, **kw)

    def test_other(self):
        lst = list(range(10))
        _CommonInnerTests.test_other(self, [lst, lst, lst[:-1], lst[:-2]])

class _CommonPairedTests:
    def test_empty(self):
        self.assert_iter_equal(self.function(range(0)), [])

    def test_single(self):
        self.assert_iter_equal(self.function(range(1)), [])

class TestPaired(_CommonPairedTests, _TestIter):
    def function(self, *args, **kw):
        return paired(*args, **kw)

    def test_other(self):
        self.assert_iter_equal(paired(range(3)), [(0, 1), (1, 2)])
        self.assert_iter_equal(paired(range(4)), [(0, 1), (1, 2), (2, 3)])
        self.assert_iter_equal(paired(range(5)), [(0, 1), (1, 2), (2, 3), (3, 4)])

class TestUnited(_CommonPairedTests, _TestIter):
    def function(self, *args, **kw):
        return united(paired(*args, **kw))

    def test_other(self):
        self.assert_iter_equal(united(paired([0, 1])),    [0, 1])
        self.assert_iter_equal(united(paired(range(3))),  list(range(3)))
        self.assert_iter_equal(united(paired(range(12))), list(range(12)))

class TestFlattened(_TestIter):
    def test_empty(self):
        self.assert_iter_equal(flattened(range(0)), [])

    def test_nested(self):
        self.assert_iter_equal(flattened([[], [[], []]]), [])
        self.assert_iter_equal(flattened([[[0]], [1, [2]], [3]]), [0, 1, 2, 3])
        self.assert_iter_equal(flattened([[{0}], (), [1, ([2],), []], [3]]),
                               [0, 1, 2, 3])

    def test_basecase(self):

        def basecase(iterable):
            return isinstance(iterable, tuple)

        self.assert_iter_equal(flattened([[(0,)], [(1,), [], []], (2,)], basecase=basecase), [(0,), (1,), (2,)])

class TestGenerates(_TestIter):
    def test_generates_nothing(self):

        def generates_nothing():
            for _ in ():
                yield

        self.assertIs(generates(generates_nothing()), None)
        self.assertRaises(StopIteration, lambda : next(generates_nothing()))

    def test_generates_single(self):

        def generates_single():
            yield 'foo'

        self.assert_iter_equal(generates(generates_single()), ['foo'])

    def test_generates_something(self):

        def generates_something():
            i = 0
            while True:
                yield i
                i += 1

        self.assert_iter_equal(head(generates(generates_something()), 4), [0, 1, 2, 3])

if __name__ == '__main__':
    unittest.main()

