from __future__ import annotations

import curses
import time
from typing import TYPE_CHECKING, overload

if TYPE_CHECKING:
    from typing import Optional, Tuple


class Gadgets:
    def __init__(self, text_delay: float = 0.1) -> None:
        self.text_delay: float = text_delay

    @overload
    def text(
        self,
        win: curses.window,
        text: str,
        *,
        rel_pos: Tuple[float, float] = ...,
        pos: None = ...,
    ) -> None: ...

    @overload
    def text(
        self,
        win: curses.window,
        text: str,
        *,
        rel_pos: None = ...,
        pos: Tuple[int, int] = ...,
    ) -> None: ...

    def text(
        self,
        win: curses.window,
        text: str,
        *,
        rel_pos: Optional[Tuple[float, float]] = None,
        pos: Optional[Tuple[int, int]] = None,
    ) -> None:
        for char in text:
            if rel_pos:
                height, width = win.getmaxyx()
                pos = (round(width * rel_pos[0]), round(height * rel_pos[1]))
