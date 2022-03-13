pyfzf
=====

![](https://img.shields.io/badge/license-MIT-green.svg?style=flat)
![https://pypi.python.org/pypi/pyfzf](https://img.shields.io/pypi/dm/pyfzf.svg?style=flat)
   
##### A python wrapper for *junegunn*'s awesome [fzf](https://github.com/junegunn/fzf).

![](https://raw.githubusercontent.com/nk412/pyfzf/master/pyfzf.gif)

Requirements
------------

* Python 3.6+
* [`fzf`](https://github.com/junegunn/fzf)

*Note*: `fzf` must be installed and available on PATH.

Installation
------------
	pip install pyfzf

Usage
-----

    >>> from pyfzf.pyfzf import FzfPrompt
    >>> fzf = FzfPrompt()
    >>> fzf = FzfPrompt(default_options="--reverse")

If `fzf` is not available on PATH, you can specify a location

    >>> fzf = FzfPrompt('/path/to/fzf')

Simply pass a list of options to the prompt function to invoke `fzf`.

    >>> fzf.prompt(range(0,10))

You can pass additional arguments to `fzf` as a second argument

    >>> fzf.prompt(range(0,10), '--multi --cycle')

If given a sequence of arguments or keyword arguments, it can construct the corresponding arguments:

    >>> fzf.prompt(range(0,50), 'multi', 'cycle', height='20%')
    >>> fzf.prompt(range(0,50), 'x', 'i', 'm', '--tac')

Items are streamed to the `fzf` process one line at a time, you can pass
any sort of iterator or generator as the first argument. For example, a file object,
or a glob of files to search for, displaying a preview:

```python
    >>> fzf.prompt(open("README.md"), "-x", delimiter="")

    >>> from pathlib import Path
    >>> fzf.prompt(Path(".").rglob("*.md"), "-x", r"--preview='cat {}'")
```

Items are delimited with `\n` by default, you can also change the delimiter (useful for multiline items):

```python
>>> fzf.prompt(["5\n10", "15\n20"], '--read0', '-m', delimiter='\0')
['15\n20']
```

License
-------
MIT

Thanks
------
@brookite for adding Windows support in v0.3.0
