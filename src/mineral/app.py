from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .screen.window_manager import WindowManager


class App:
    def __init__(self, manager: WindowManager) -> None:
        self.manager = manager

    def run(self) -> None:
        if self.manager.current_window is None:
            raise RuntimeError("No window has been set to run.")
        
        while self.manager.is_running:
            self.manager.current_window.update()

