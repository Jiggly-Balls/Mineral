from __future__ import annotations

import curses
import time
from typing import TYPE_CHECKING, overload

if TYPE_CHECKING:
    from typing import Any, Literal, Optional, Sequence, Union

from .types import Colour, ReturnType


class Console:
    UP: tuple[int, int, int] = (450, 259, 119)
    DOWN: tuple[int, int, int] = (456, 258, 115)
    ENTER: int = 10
    SPACE: int = 32
    BACKSPACE: int = 10

    def __init__(
        self,
        def_option_colour: Colour,
        def_option_bg: Colour,
        def_text_colour: Colour,
        def_text_bg: Colour,
        def_text_end: str = "",
        line_wrap: int = 80,
        text_delay: float = 0.02,
        max_input_char: int = 30,
    ) -> None:
        self.option_colour = def_option_colour
        self.option_bg = def_option_bg
        self.text_end = def_text_end
        self.text_colour = def_text_colour
        self.text_bg = def_text_bg
        self.line_wrap = line_wrap
        self.text_delay = text_delay
        self.max_input_char = max_input_char

        curses.initscr()
        curses.start_color()

    def _max_wrap(self, win: Any) -> int:
        _, max_cols = win.getmaxyx()
        if self.line_wrap < 0:
            return max_cols
        return min(max_cols, self.line_wrap)

    def text_terminal(
        self,
        text: str,
        text_colour: Optional[Colour] = None,
        text_bg: Optional[Colour] = None,
        text_end: Optional[str] = None,
        text_delay: Optional[int] = None,
    ) -> None:
        def main(stdscr: Any) -> Any:
            stdscr.erase()
            column = 0
            row = 0

            text_colour_ = text_colour or self.text_colour
            text_bg_ = text_bg or self.text_bg
            text_end_ = text_end or self.text_end
            text_delay_ = text_delay or self.text_delay

            curses.init_pair(1, text_colour_.value, text_bg_.value)

            for letter in text:
                if letter == "\n":
                    row += 1
                    column = 0
                    continue
                stdscr.addstr(row, column, letter, curses.color_pair(1))
                column += 1
                stdscr.refresh()
                time.sleep(text_delay_)

            if text_end_:
                stdscr.addstr(f"\n\n{text_end_}")
            stdscr.refresh()
            stdscr.getch()

        curses.wrapper(main)

    @overload
    def input_terminal(
        self,
        prompt: str,
        decode_input: Literal[False],
    ) -> bytes: ...

    @overload
    def input_terminal(
        self,
        prompt: str,
        decode_input: Literal[True] = ...,
    ) -> str: ...

    def input_terminal(
        self,
        prompt: str,
        decode_input: bool = True,
    ) -> Union[str, bytes]:
        def main(stdscr: Any) -> Any:
            stdscr.erase()
            column = 0
            row = 0

            text_colour_ = self.text_colour
            text_bg_ = self.text_bg
            text_delay_ = self.text_delay
            max_input_char_ = self.max_input_char

            curses.init_pair(1, text_colour_.value, text_bg_.value)

            for letter in prompt:
                if column == self._max_wrap(stdscr):
                    row += 1
                    column = 0

                if letter == "\n":
                    row += 1
                    column = 0
                    continue
                stdscr.addstr(row, column, letter, curses.color_pair(1))
                column += 1
                stdscr.refresh()
                time.sleep(text_delay_)

            curses.echo()
            user_input = stdscr.getstr(row, column, max_input_char_)
            if decode_input:
                return user_input.decode()
            return user_input

        return curses.wrapper(main)

    def option_terminal(
        self,
        text: str,
        options: Sequence[str],
        return_type: tuple[ReturnType] = (ReturnType.INDEX,),
        text_colour: Optional[Colour] = None,
        text_bg: Optional[Colour] = None,
        option_colour: Optional[Colour] = None,
        option_bg: Optional[Colour] = None,
        text_delay: Optional[int] = None,
    ) -> Union[int, str, tuple[int, str]]:
        def main(stdscr: Any) -> Any:
            choice = 0
            option_row = 2

            text_colour_ = text_colour or self.text_colour
            text_bg_ = text_bg or self.text_bg
            option_colour_ = option_colour or self.option_colour
            option_bg_ = option_bg or self.option_bg
            text_delay_ = text_delay or self.text_delay

            curses.init_pair(1, text_colour_.value, text_bg_.value)
            curses.init_pair(2, option_colour_.value, option_bg_.value)

            stdscr.erase()
            text_col = 0
            text_row = 0
            formatted_text = ""

            for letter in text:
                formatted_text += letter

                if text_col == self._max_wrap(stdscr):
                    text_row += 1
                    text_col = 0
                    option_row += 1
                    formatted_text += "\n"

                if letter == "\n":
                    text_row += 1
                    text_col = 0
                    option_row += 1
                    continue

                stdscr.addstr(text_row, text_col, letter, curses.color_pair(1))
                text_col += 1
                stdscr.refresh()
                time.sleep(text_delay_)

            while True:
                stdscr.erase()
                stdscr.addstr(0, 0, formatted_text, curses.color_pair(1))

                for index, option in enumerate(options):
                    if index == choice:
                        stdscr.addstr(
                            option_row + index,
                            2,
                            "> " + option + " <",
                            curses.A_STANDOUT,
                        )
                    else:
                        stdscr.addstr(
                            option_row + index, 2, option, curses.color_pair(2)
                        )

                stdscr.refresh()
                user_input = stdscr.getch()

                if user_input in self.UP:
                    choice -= 1
                    choice = len(options) - 1 if choice < 0 else choice

                elif user_input in self.DOWN:
                    choice += 1
                    choice = 0 if choice > len(options) - 1 else choice

                elif user_input == self.ENTER:
                    break

            map_ = {
                ReturnType.INDEX: choice,
                ReturnType.LITERAL: options[choice],
            }

            if len(return_type) == 1:
                return map_[return_type[0]]
            return (map_[return_type[0]], map_[return_type[1]])

        return curses.wrapper(main)
