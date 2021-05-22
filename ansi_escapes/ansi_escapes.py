from os import environ as env
import platform
import os

ESC = '\u001B['
OSC = '\u001B]'
BEL = '\u0007'
SEP = ';'
isTerminalApp = env.get('TERM_PROGRAM') == 'Apple_Terminal'


def cursorTo(x, y=None):
    if y is None:
        return ESC + str(int(x + 1)) + 'G'

    return ESC + str(int(y + 1)) + ';' + str(int(x + 1)) + 'H'


def cursorMove(x, y=None):
    returnValue = ''

    if x < 0:
        returnValue += ESC + str(int(-x)) + 'D'
    elif x > 0:
        returnValue += ESC + str(int(x)) + 'C'

    if y < 0:
        returnValue += ESC + str(int(-y)) + 'A'
    elif y > 0:
        returnValue += ESC + str(int(y)) + 'B'

    return returnValue


def cursorUp(count=1):
    return ESC + str(int(count)) + 'A'


def cursorDown(count=1):
    return ESC + str(int(count)) + 'B'


def cursorForward(count=1):
    return ESC + str(int(count)) + 'C'


def cursorBackward(count=1):
    return ESC + str(int(count)) + 'D'


cursorLeft = ESC + 'G'
cursorSavePosition = '\u001B7' if isTerminalApp else ESC + 's'
cursorRestorePosition = '\u001B8' if isTerminalApp else ESC + 'u'
cursorGetPosition = ESC + '6n'
cursorNextLine = ESC + 'E'
cursorPrevLine = ESC + 'F'
cursorHide = ESC + '?25l'
cursorShow = ESC + '?25h'


def eraseLines(count):
    clear = ""

    for i in range(count):
        clear += eraseLine + cursorUp() if (i < count - 1) else ''

    if count != 0:
        clear += cursorLeft

    return clear


eraseEndLine = ESC + 'K'
eraseStartLine = ESC + '1K'
eraseLine = ESC + '2K'
eraseDown = ESC + 'J'
eraseUp = ESC + '1J'
eraseScreen = ESC + '2J'
scrollUp = ESC + 'S'
scrollDown = ESC + 'T'

clearScreen = '\u001Bc'

if platform.system() == 'Windows':
    clearTerminal = '{}{}0f'.format(eraseScreen, ESC)
    # 1. Erases the screen (Only done in case '2' is not supported)
    # 2. Erases the whole screen including scrollback buffer
    # 3. Moves cursor to the top-left position
    # More info: https://www.real-world-systems.com/docs/ANSIcode.html
else:
    clearTerminal = '{}{}3J{}H'.format(eraseScreen, ESC, ESC)

beep = BEL


def link(text, url):
    return ''.join([
        OSC,
        '8',
        SEP,
        SEP,
        url,
        BEL,
        text,
        OSC,
        '8',
        SEP,
        SEP,
        BEL
    ])


class ITerm:
    def setCwd(self, cwd=None):
        if cwd is None:
            cwd = os.getcwd()
        return '{}50;CurrentDir={}{}'.format(OSC, cwd, BEL)

    def annotation(self, message: str, x=None, y=None, length=None, isHidden=False):
        returnValue = '{}1337;'.format(OSC)

        hasX = x is not None
        hasY = y is not None
        if (hasX or hasY) and not (hasX and hasY and length is not None):
            raise TypeError('`x`, `y` and `length` must be defined when `x` or `y` is defined')

        message = message.replace('|', '')

        returnValue += 'AddHiddenAnnotation=' if isHidden else 'AddAnnotation='

        if length is not None and length > 0:
            returnValue += '|'.join([message, str(length), str(x), str(y)] if hasX else [str(length), str(message)])
        else:
            returnValue += message

        return returnValue + BEL

    def notify(self, message: str):
        return '{}9;{}{}'.format(OSC, message, BEL)


iTerm = ITerm()
