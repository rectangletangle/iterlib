""" This module contains a bunch of functions which facilitate specialized iteration patterns. """


import itertools
import collections

__all__ = ['windowed', 'chunked', 'chop', 'generates', 'truncated', 'paired', 'united', 'flattened']

def windowed(iterable, size, step=1, trail=False):
    """ This function yields a tuple of a given size, then steps forward. If the step is smaller than the size, the
        function yields "overlapped" tuples. """

    if size == 1 and step == 1:
        # A more efficient implementation for this particular special case.
        for item in iterable:
            yield (item,)
    else:
        window = ()
        for item in iterable:
            window += (item,)

            if len(window) == size:
                yield window
                window = window[step:]

        if trail:
            while len(window):
                yield window
                window = window[step:]

def chunked(iterable, size, trail=False):
    """ This breaks up an iterable into multiple chunks (tuples) of a specific size. """

    return windowed(iterable, size=size, step=size, trail=trail)

def chop(iterable, size):
    """ This removes any chunks at the end of an iterable, below a certain size. """

    if size > 0:
        for chunk in iterable:
            try:
                chunk[size-1] # Easier to Ask for Forgiveness Than Permission, style length testing
            except IndexError:
                break
            else:
                yield chunk

def generates(generator, default=None):
    """ If a generator doesn't generate anything this returns the <default> (None), otherwise this returns an
        equivalent generator. """

    iterable = iter(generator)

    try:
        first = next(iterable)
    except StopIteration:
        return default
    else:
        return itertools.chain((first,), iterable)

def truncated(iterable, amount):
    """ This allows for iteration over all but the last couple of items in an iterable. """

    queue   = collections.deque()
    append  = queue.append
    popleft = queue.popleft

    for item in iterable:
        append(item)

        if len(queue) > amount:
            yield popleft()

def paired(iterable):
    return windowed(iterable, size=2, step=1)

def united(paired):
    """ This can be used to efficiently undo the effects of the <paired> function on an iterable. """

    paired = iter(paired)

    try:
        first, second = next(paired)
    except (StopIteration, ValueError):
        pass
    else:
        yield first
        yield second
        for first, second in paired:
            yield second

def flattened(iterable, basecase=None):
    if basecase is None:
        def basecase(iterable):
            return not hasattr(iterable, '__iter__')

    if not basecase(iterable):
        for item in iterable:
            yield from flattened(item, basecase=basecase)
    else:
        item = iterable
        yield item

