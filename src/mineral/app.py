from __future__ import annotations

import curses
from typing import TYPE_CHECKING

from .screen.window import Window
from .types import MISSING

if TYPE_CHECKING:
    from typing import Any

    from .screen.window_manager import WindowManager


class App:
    def __init__(self, manager: WindowManager) -> None:
        self.manager: WindowManager = manager
        self.screen: curses.window = MISSING  # curses.initscr()

        # Window.screen = self.screen
        #
        # if colours:
        #     curses.start_color()
        #     curses.use_default_colors()
        # curses.noecho()

    def pre_update(self) -> bool:
        return True

    def run(self, *args: Any) -> None:
        def wrapper_run(window: curses.window) -> None:
            self.screen = window
            Window.screen = window

            if self.manager.current_window is None:
                raise RuntimeError("No window has been set to run.")

            while self.manager.is_running:
                continue_update = self.pre_update()
                if continue_update:
                    if self.manager.global_on_update:
                        self.manager.global_on_update(self.manager)
                    self.manager.current_window.on_update(*args)

        curses.wrapper(wrapper_run)
