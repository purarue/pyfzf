#!/usr/bin/env python

import shlex
import subprocess
from shutil import which
from functools import wraps
from typing import Optional, Sequence, Any, Union, Iterable, List, Iterator


# constants
FZF_URL = "https://github.com/junegunn/fzf"


# types
# either just a string like "--reverse --bold"
# or a sequence (list or tuple) of keys or key value pairs
# e.g. ("--no-mouse", "-m", ("--height, 50))
FzfOptions = Sequence[Union[str, Sequence[str]]]
InputSequence = Union[Sequence[Any], Iterable[Any], Iterator[Any]]


class FzfPrompt:
    def __init__(
        self, executable_path: Optional[str] = None, default_options: FzfOptions = ()
    ):
        if executable_path:
            self.executable_path = executable_path
        elif not which("fzf") and not executable_path:
            raise SystemError(f"Cannot find 'fzf' installed on PATH. ({FZF_URL})")
        else:
            self.executable_path = "fzf"

        self.options: List[str] = self.__class__.parse_options(default_options)

    def __repr__(self) -> str:
        return f'FzfPrompt(executable_path={self.executable_path}, default_options={repr(" ".join(self.options))})'

    @staticmethod
    def key_to_option(key: str) -> str:
        if key.startswith("-") or key.startswith("+"):
            # user passed something like --preview or +x already, dont prepend hyphens
            return key
        else:
            # compute fzf shell option
            if len(key) == 1:
                # e.g. x --> -x
                return f"-{key}"
            else:
                # e.g. preview -> --preview
                return f"--{key}"

    @staticmethod
    def parse_options(options: FzfOptions) -> List[str]:
        """Parses arbitrary options to a list of options for fzf"""
        if isinstance(options, str):
            if options.strip() == "":
                return []
            # if user passed a string with no spaces, try to add hyphens
            if " " not in options:
                return [FzfPrompt.key_to_option(options)]
            else:
                # assume the user passed a constructed string of options
                return [options]
        else:
            computed_options = []
            for opt in options:
                key: str
                value: Optional[str] = None
                # user passed single item
                if isinstance(opt, str):
                    if opt.strip() == "":
                        continue
                    key = opt
                elif isinstance(opt, Sequence):
                    if len(opt) != 2:
                        raise TypeError(
                            f'Expected a tuple or list with two items, received {len(opt)} "{opt}"'
                        )
                    if not isinstance(opt[0], str):
                        raise TypeError(f"Expected a str key, received {opt[0]}")
                    key = opt[0]
                    value = str(opt[1])  # use could pass something else, e.g. int
                else:
                    raise TypeError(
                        f'Expected a str or a sequence of options, e.g., ["-x", ("height", "40%")], received {opt}'
                    )

                if value is not None and value.strip():
                    # e.g. --info=default --margin="TRBL"
                    # shlex.quote to prevent double quotes from breaking command
                    computed_options.append(
                        f"{FzfPrompt.key_to_option(key)}={shlex.quote(value)}"
                    )
                else:
                    # option without a value, e.g. --reverse,
                    computed_options.append(FzfPrompt.key_to_option(key))
            return computed_options

    def prompt(
        self,
        choices: Union[Sequence[Any], Iterable[Any], Iterator[Any]],
        *args: FzfOptions,
        delimiter: str = "\n",
        encoding="utf-8",
        **kwargs: Any,
    ) -> Any:

        # combine args/kwargs into fzf options
        opts_raw: List[Any] = list(args)
        for k, v in kwargs.items():
            opts_raw.append((k, v))

        # parse into options
        opts = self.__class__.parse_options(opts_raw)

        # add any options set on the Fzf instance
        opts.extend(self.options)
        options = " ".join(opts)

        selected_text: str = ""
        selection = []

        # spawn a process and send lines one at a time
        # https://stackoverflow.com/a/69397677
        fzf_process = subprocess.Popen(
            shlex.split(f"{self.executable_path} {options}"),
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            encoding=encoding,
        )
        assert fzf_process.stdin is not None, "Fatal error creating input stream"
        try:
            for item in choices:
                sitem = str(item)  # iterator could be anything, convert to string
                fzf_process.stdin.write(sitem)
                fzf_process.stdin.write(delimiter)
        except BrokenPipeError:
            pass
        stdout, _ = fzf_process.communicate()
        if stdout != "":
            selected_text = stdout

        # can't split by '', default to newlines if misconfigured
        use_delimiter = "\n" if delimiter == "" else delimiter

        if selected_text:
            selection = selected_text.rstrip("\n").split(use_delimiter)

        return selection

    def wrap(self, *opt_args, **opt_kwargs):
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                items = func(*args, **kwargs)
                return self.prompt(items, *opt_args, **opt_kwargs)

            return wrapper

        return decorator
