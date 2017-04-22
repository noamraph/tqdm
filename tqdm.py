"""Source file for tqdm functionality."""

import sys
import time

__all__ = ['tqdm', 'trange']


def format_interval(t):
    """To convert time duration into a readablie format."""
    mins, s = divmod(int(t), 60)
    h, m = divmod(mins, 60)
    if h:
        return '%d:%02d:%02d' % (h, m, s)
    else:
        return '%02d:%02d' % (m, s)


def format_meter(n, total, elapsed):
    """To display progress on screen.

    Args:
        n - number of finished iterations
        total - total number of iterations, or None
        elapsed - number of seconds passed since start

    Returns:
        A string with detailing the progress of work or if job is completed
        then its shows the stats for completes work. These Details include
        time elapsed, approx time left to complete job and also number of
        iteration processed per second.
    """
    if n > total:
        total = None

    elapsed_str = format_interval(elapsed)
    rate = '%5.2f' % (n / elapsed) if elapsed else '?'

    if total:
        frac = float(n) / total

        n_bars = 10
        bar_length = int(frac * n_bars)
        bar = '#' * bar_length + '-' * (n_bars - bar_length)

        percentage = '%3d%%' % (frac * 100)

        left_str = format_interval(elapsed / n * (total - n)) if n else '?'

        return '|%s| %d/%d %s [elapsed: %s left: %s, %s iters/sec]' % (
            bar, n, total, percentage, elapsed_str, left_str, rate)

    else:
        return '%d [elapsed: %s, %s iters/sec]' % (n, elapsed_str, rate)


class StatusPrinter(object):
    def __init__(self, file):
        self.file = file
        self.last_printed_len = 0

    def print_status(self, s):
        self.file.write('\r' + s + ' ' * max(self.last_printed_len - len(s), 0))
        self.file.flush()
        self.last_printed_len = len(s)


def tqdm(iterable, desc='', total=None, leave=False, file=sys.stderr, mininterval=0.5, miniters=1):
    """A wrapper over user input iterator to show progress and time elapsed details.

    Note: This wrapper does not change the functionality of the iterator output
     and only displaying simple progress meter. Every time the input iterator
     is being called, the progress meter keeps updating progress.

    Args:
        iterable: user input iterator
        desc(optional): A short description, to display during the progress.
                This input is shown at beginning of the line of the progress.
        total(optional): User can give the number of expected iterations.
                If not given, len(iterable) is used if it is defined.
        file(optional): A file-like object to output the progress message to.
        leave(optional): If leave is False(default), tqdm deletes its traces
                 from screen after it has finished iterating over all elements.
        miniters(optional): for how many iteraitons progress to be displayed.
                If the limit is passed, no futher progress is displayed.
        mininterval(optional): for how many seconds progress to be displayed.
                If the limit is passed, no futher progress is displayed.
    """
    if total is None:
        try:
            total = len(iterable)
        except TypeError:
            total = None

    prefix = desc + ': ' if desc else ''

    sp = StatusPrinter(file)
    sp.print_status(prefix + format_meter(0, total, 0))

    start_t = last_print_t = time.time()
    last_print_n = 0
    n = 0
    for obj in iterable:
        yield obj
        # Now the object was created and processed, so we can print the meter.
        n += 1
        if n - last_print_n >= miniters:
            # We check the counter first, to reduce the overhead of time.time()
            cur_t = time.time()
            if cur_t - last_print_t >= mininterval:
                sp.print_status(prefix + format_meter(n, total, cur_t - start_t))
                last_print_n = n
                last_print_t = cur_t

    if not leave:
        sp.print_status('')
        sys.stdout.write('\r')
    else:
        if last_print_n < n:
            cur_t = time.time()
            sp.print_status(prefix + format_meter(n, total, cur_t - start_t))
        file.write('\n')


def trange(*args, **kwargs):
    """A wrapper function, combining tqdm functionality on range(xrange in py2).

    All the `args` provided will be given to `range` as input and
     `kwargs` key word arguments goes to `tqdm` main function as input.

    Example:
    ---------------------------------------------------------------------------------
    Using standard `range` function as iterator for tqdm.
    >>> import time, tqdm
    >>> for i in tqdm.tqdm(range(1, 100, 2), desc='tqdm & range'):
    ...     time.sleep(0.1)
    ...
    tqdm & range: |######----| 30/50  60% [elapsed: 00:03 left: 00:02,  9.76 iters/sec]
    >>>

    Using tdqm.trange function directly instead of .

    >>> for i in tqdm.trange(1, 100, 2, desc='trange'):
    ...     time.sleep(0.1)
    ...

    trange: |########--| 40/50  80% [elapsed: 00:04 left: 00:01,  9.71 iters/sec]
    """
    try:
        f = xrange
    except NameError:
        f = range

    return tqdm(f(*args), **kwargs)
