from __future__ import annotations

import curses
from typing import TYPE_CHECKING

from .screen.window import Window
from .types import MISSING
from .utils import FileLogger

if TYPE_CHECKING:
    from typing import Any

    from .screen.window_manager import WindowManager


class App:
    def __init__(
        self, manager: WindowManager, min_height: int = 20, min_width: int = 20
    ) -> None:
        self.manager: WindowManager = manager
        self.screen: curses.window = MISSING

        self.min_height: int = min_height
        self.min_width: int = min_width
        self.error_text: str = "Minimum terminal size required: {}x{}"
        # First placeholder for min_width
        # Second placeholder for min_height

        self.logger: FileLogger = FileLogger("curse_of_terminal.log")

    def _pre_update(self) -> bool:
        key = self.screen.getch()

        if key == curses.KEY_RESIZE:
            curses.resize_term(0, 0)
            self.screen.clear()

        height, width = self.screen.getmaxyx()
        # self.logger.file_log(f"{height=} {width=}")

        if height < self.min_height or width < self.min_width:
            self.screen.clear()
            text = self.error_text.format(self.min_width, self.min_height)

            x = (width - len(text)) // 2 if width > len(text) else 0
            y = height // 2
            try:
                self.screen.addstr(y, x, text)
            except curses.error:
                pass

            try:
                self.screen.refresh()
            except curses.error:
                pass

            return False
        return True

    def run(self, *args: Any) -> None:
        def run_wrapper(stdscr: curses.window) -> None:
            if self.manager.current_window is None:
                raise RuntimeError("No window has been set to run.")

            self.screen = stdscr
            Window.screen = stdscr

            while self.manager.is_running:
                self.screen.nodelay(True)
                continue_update = self._pre_update()
                self.screen.nodelay(False)

                if continue_update:
                    if self.manager.global_on_update:
                        self.manager.global_on_update(self.manager)
                    try:
                        self.screen.refresh()
                    except curses.error:
                        pass

                    self.manager.current_window.on_update(*args)

        curses.wrapper(run_wrapper)
