""" This module contains a bunch of composable functions which help facilitate specialized iteration patterns. """

__version__ = '0.0.0'
__author__  = 'Drew A. French'
__email__   = 'rectangletangle@gmail.com'
__url__     = 'github.com/rectangletangle'

import itertools
import collections

__all__ = ['windowed', 'chunked', 'chopped', 'head', 'tail', 'skipped', 'truncated', 'paired', 'united', 'flattened',
           'generates']

def windowed(iterable, size, step=1, partial=False):
    """ This function yields a tuple of a given size, then steps forward. If the step is smaller than the size, the
        function yields "overlapped" tuples. If the <partial> argument is true the remaining tuples shorter than <size>
        at the end of iterable will be also yielded. """

    if size == 0:
        pass # Quickly yields nothing for this special case.

    elif size == 1 and step == 1:
        # An efficient implementation for this particular special case.

        for item in iterable:
            yield (item,)
    else:
        # The general case.

        window = ()
        overshoot = 0
        for item in iterable:

            if overshoot < 0:
                overshoot += 1
            else:
                window += (item,)

            length = len(window)

            if length == size:
                yield window

                overshoot = length - step
                if overshoot > 0:
                    overshoot = 0

                window = window[step:]

        if partial:
            while len(window):
                yield window
                window = window[step:]

def chunked(iterable, size, partial=False):
    """ This breaks up an iterable into multiple chunks (tuples) of a specific size. """

    return windowed(iterable, size=size, step=size, partial=partial)

def chopped(iterable, size):
    """ This removes undersized chunks at the end of an iterable below a certain size. """

    if size > 0:
        for chunk in iterable:
            try:
                chunk[size - 1] # "Easier to ask for forgiveness than permission," style length testing!
            except IndexError:
                break
            else:
                yield chunk

def _amount_error(amount):
    return ValueError('The amount <{}> must be <None> or an integer greater than -1.'.format(repr(amount)))

def head(iterable, amount):
    """ Iterate over the first few items in an iterable. """

    if amount is not None and not isinstance(amount, int):
        raise _amount_error(amount)
    else:
        try:
            return itertools.islice(iterable, amount)
        except ValueError:
            raise _amount_error(amount)

def tail(iterable, amount):
    """ Iterate over the last few items in an iterable. """

    raise NotImplementedError

def skipped(iterable, amount):
    """ Iterate over all but the first few items in an iterable. """

    if amount is not None and not isinstance(amount, int):
        raise _amount_error(amount)
    else:
        try:
            return itertools.islice(iterable, amount, None)
        except ValueError:
            raise _amount_error(amount)

def truncated(iterable, amount):
    """ Iterate over all but the last few items in an iterable. """

    # todo: use normal slice when possible

    if amount is None:
        for item in iterable:
            yield item
    elif amount < 0 or not isinstance(amount, int):
        raise _amount_error(amount)
    else:
        queue   = collections.deque()
        append  = queue.append
        popleft = queue.popleft

        for item in iterable:
            append(item)

            if len(queue) > amount:
                yield popleft()

def paired(iterable):
    """ Chunk an iterable into overlapping pairs. """

    return windowed(iterable, size=2, step=1)

def united(paired):
    """ Reunite the items from a paired iterable. """

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
    """ Flatten a nested iterable. """

    if basecase is None:
        def basecase(iterable):
            try:
                iterable.__iter__
            except AttributeError:
                return True
            else:
                return False

    if basecase(iterable):
        item = iterable
        yield item
    else:
        for item in iterable:
            for nested in flattened(item, basecase=basecase):
                yield nested

def generates(generator, default=None):
    """ If a generator doesn't generate anything, i.e., it's empty, this returns the <default> (<None>), otherwise this
        returns an equivalent generator. """

    iterable = iter(generator)

    try:
        first = next(iterable)
    except StopIteration:
        return default
    else:
        return itertools.chain((first,), iterable)
