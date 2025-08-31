import curses
from enum import Enum, auto
from typing import TypeAlias


class Colour(Enum):
    BLACK = curses.COLOR_BLACK
    BLUE = curses.COLOR_BLUE
    CYAN = curses.COLOR_CYAN
    GREEN = curses.COLOR_GREEN
    MAGENTA = curses.COLOR_MAGENTA
    RED = curses.COLOR_RED
    WHITE = curses.COLOR_WHITE
    YELLOW = curses.COLOR_YELLOW


Color: TypeAlias = Colour


class ReturnType(Enum):
    INDEX = auto()
    LITERAL = auto()
