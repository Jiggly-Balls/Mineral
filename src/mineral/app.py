from __future__ import annotations

import curses
from typing import TYPE_CHECKING

from .screen.window import Window
from .utils import FileLogger

if TYPE_CHECKING:
    from typing import Any

    from .screen.window_manager import WindowManager


class App:
    def __init__(self, manager: WindowManager, min_height: int = 20, min_width: int = 20) -> None:
        self.manager: WindowManager = manager
        self.screen: curses.window = curses.initscr()
        Window.screen = self.screen

        curses.cbreak()
        curses.noecho()
        self.screen.keypad(True)
        curses.start_color()
        curses.use_default_colors()

        self.min_height = min_height
        self.min_width = min_width

        self.logger = FileLogger("curse_of_terminal.log")

    def pre_update(self) -> bool:
        key = self.screen.getch()

        if key == curses.KEY_RESIZE:
            curses.resize_term(0, 0)
            self.screen.clear()
        
        height, width = self.screen.getmaxyx()
        # self.logger.file_log(f"{height=} {width=}")

        if height < self.min_height or width < self.min_width:
            self.screen.clear()
            text = f"Minimum terminal size required: {self.min_width}x{self.min_height}"

            x = (width - len(text)) // 2 if width > len(text) else 0
            y = height // 2 if height > 0 else 0
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
        if self.manager.current_window is None:
            raise RuntimeError("No window has been set to run.")

        while self.manager.is_running:
            self.screen.nodelay(True)
            continue_update = self.pre_update()
            self.screen.nodelay(False)

            if continue_update:
                if self.manager.global_on_update:
                    self.manager.global_on_update(self.manager)
                try:
                    self.screen.refresh()
                except curses.error:
                    pass

                self.manager.current_window.on_update(*args)

