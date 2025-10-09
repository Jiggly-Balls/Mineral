from __future__ import annotations

import curses
from typing import TYPE_CHECKING, overload

from .types import MISSING

if TYPE_CHECKING:
    from typing import Optional, Tuple


class Text:
    @overload
    def __init__(
        self,
        win: curses.window,
        text: str,
        text_delay: int = 200,
        auto_start: bool = True,
        rel_auto_adjust: bool = True,
        *,
        rel_pos: Tuple[float, float] = ...,
        pos: None = ...,
    ) -> None: ...

    @overload
    def __init__(
        self,
        win: curses.window,
        text: str,
        text_delay: int = 200,
        auto_start: bool = True,
        rel_auto_adjust: bool = True,
        *,
        rel_pos: None = ...,
        pos: Tuple[int, int] = ...,
    ) -> None: ...

    def __init__(
        self,
        win: curses.window,
        text: str,
        text_delay: int = 200,
        auto_start: bool = True,
        rel_auto_adjust: bool = True,
        *,
        rel_pos: Optional[Tuple[float, float]] = None,
        pos: Optional[Tuple[int, int]] = None,
    ) -> None:
        self.win: curses.window = win
        self.text: str = text
        self.text_delay: int = text_delay
        self.rel_auto_adjust: bool = rel_auto_adjust
        self.rel_pos: Optional[Tuple[float, float]] = rel_pos
        self.pos: Tuple[int, int] = pos or MISSING
        
        self.running: bool = False
        self.finished: bool = False

        if auto_start and not self.finished:
            self.start()
    
    def _calculate_rel_pos(self) -> None:
        if self.rel_pos:
            height, width = self.win.getmaxyx()
            if self.rel_auto_adjust:
                width -= len(self.text)
            self.pos = (round(width * self.rel_pos[0]), round(height * self.rel_pos[1]))
    
    def start(self) -> None:
        self.running = True

        if self.text_delay > 0:
            for char in self.text:
                self._calculate_rel_pos()
                column, row = self.pos

                if char == "\n":
                    row += 1
                    column = 0
                    continue
                self.win.addstr(row, column, char)
                column += 1
                self.win.refresh()

        else:
            self.final_draw()
        
        self.running = False
        self.finished = True
    
    def final_draw(self) -> None:
        self.running = True

        self._calculate_rel_pos()
        column, row = self.pos
        self.win.addstr(row, column, self.text)

        self.running = False