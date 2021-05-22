from ansi_escapes import ansiEscapes


def test_ansi_escapes():
    assert ansiEscapes.BEL == '\u0007'
