import sys
from pyfzf import FzfPrompt

# dummy executable path
D = sys.executable

# make sure options
def tests_parsing_options() -> None:

    assert ["--read0"] == FzfPrompt(D, ("--read0")).options
    assert ["--read0"] == FzfPrompt(D, "read0").options
    assert ["-x"] == FzfPrompt(D, "-x").options
    assert ["-x"] == FzfPrompt(D, "x").options
    assert ["--preview"] == FzfPrompt(D, "--preview").options
    assert ["--preview"] == FzfPrompt(D, "--preview").options
    assert ["-x", "--reverse"] == FzfPrompt(D, ("x", "--reverse")).options
    assert ["-x", "--reverse"] == FzfPrompt(D, ("x", "reverse")).options
    assert ["-x", "--reverse"] == FzfPrompt(D, ("-x", "reverse")).options
    assert ["-x", "--height=20%"] == FzfPrompt(D, ["-x", ["height", "20%"]]).options
    assert ["-x", "--layout=reverse-list"] == FzfPrompt(D, ["-x", ("layout", "reverse-list")]).options
    assert ["-x", "--marker=\'\"\'"] == FzfPrompt(D, ["-x", ("marker", '"')]).options
    assert ["-x", "-i", "-m", "--tac"] == FzfPrompt(D, ['x', 'i', 'm', '--tac']).options
