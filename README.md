# pyfzf

## Forked Changes:

This doesn't write to a temporary file before prompting, it communicates with the subprocess directly given any iterator, sending lines as they're processed.

It also lets you send any `fzf` CLI options as args/kwargs, or decorate a function which returns an iterator to use as fzf input (see below for examples)

##### A python wrapper for _junegunn_'s [fzf](https://github.com/junegunn/fzf).

![](https://raw.githubusercontent.com/nk412/pyfzf/master/pyfzf.gif)

## Requirements

- Python 3.6+
- [`fzf`](https://github.com/junegunn/fzf)

_Note_: `fzf` must be installed and available on `$PATH`.

## Installation

    pip install pyfzf_iter

## Usage

```python
from pyfzf.pyfzf import FzfPrompt

fzf = FzfPrompt()
fzf = FzfPrompt(default_options="--reverse")
```

If `fzf` is not available on PATH, you can specify a location

```python
fzf = FzfPrompt('/path/to/fzf')
```

Simply pass a sequence of items to the prompt function to invoke `fzf`

```python
fzf.prompt(range(0,10))
```

You can pass additional positional arguments to `fzf`.

```python
fzf.prompt(range(0,10), '--multi', '--cycle')
fzf.prompt(range(0,50), 'multi', 'cycle', height='20%')
fzf.prompt(range(0,50), 'x', 'i', 'm', '--tac')
```

Items are streamed to the `fzf` process one line at a time, you can pass
any sort of iterator or generator as the first argument. For example, a file object,
or a glob of files to search for, displaying a preview:

```python
fzf.prompt(open("README.md"), "-m", delimiter="")

from pathlib import Path
fzf.prompt(Path(".").rglob("*.md"), "-m", r"--preview='cat {}'")
```

Items are delimited with `\n` by default, you can also change the delimiter (useful for multiline items):

```python
>>> fzf.prompt(["5\n10", "15\n20"], '--read0', '-m', delimiter='\0')
['15\n20']
```

You can also wrap a decorate a function with `wrap`, which then runs `fzf` when you call the function:

```python
from pyfzf import FzfPrompt

fzf = FzfPrompt()

@fzf.wrap("--tac")
def items(n: int):
    return range(n)

# prompts you to pick one of the items with fzf
items(n=50)
```
