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
        *,
        rel_pos: Optional[Tuple[float, float]] = None,
        pos: Optional[Tuple[int, int]] = None,
    ) -> None:
        self.win: curses.window = win
        self.text: str = text
        self.text_delay: int = text_delay
        self.rel_pos: Optional[Tuple[float, float]] = rel_pos
        self.pos: Tuple[int, int] = pos or MISSING
        self.running: bool = False

        if auto_start:
            self.start()
    
    def start(self) -> None:
        self.running = True

        for char in self.text:
            if self.rel_pos:
                height, width = self.win.getmaxyx()
                self.pos = round(width * self.rel_pos[0]), round(height * self.rel_pos[1])
