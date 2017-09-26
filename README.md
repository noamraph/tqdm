tqdm
====

Instantly make your loops show a progress meter - just wrap any iterator with "tqdm(iterator)", and you're done!

Note: an actively developed version is here: https://github.com/tqdm/tqdm

![ScreenShot](https://i.imgur.com/he9Aw5C.gif)

tqdm (read ta<i>qa</i>dum, تقدّم) means "progress" in arabic.

As of now, `tqdm` module provides two simple iterator functions

* `tqdm`: A wrapper over user provided wrapper function
* `trange`: A wrapper over python's standard range function()

Example:

```python
from tqdm import tqdm, trange
from time import sleep

# simple example of see how tqdm display works
for i in tqdm(range(100), desc='example1'):
    sleep(0.1)
    if i // 10 == 0:
        print(i)

# using tqdm's wrapper for range.
for i in trange(100, desc='example2'):
    sleep(0.1)
    if i // 10 == 0:
        print(i)
print('Example: Started,....completed!')

```

Here's the doc:

```python
def tqdm(iterable, desc='', total=None, leave=False, mininterval=0.5, miniters=1):
    """
    Get an iterable object, and return an iterator which acts exactly like the
    iterable, but prints a progress meter and updates it every time a value is
    requested.
    'desc' can contain a short string, describing the progress, that is added
    in the beginning of the line.
    'total' can give the number of expected iterations. If not given,
    len(iterable) is used if it is defined.
    If leave is False, tqdm deletes its traces from screen after it has finished
    iterating over all elements.
    If less than mininterval seconds or miniters iterations have passed since
    the last progress meter update, it is not updated again.
    """

def trange(*args, **kwargs):
    """A shortcut for writing tqdm(xrange)"""
    return tqdm(xrange(*args), **kwargs)
```

