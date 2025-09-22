from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Optional

    from .types import Colour
    from .window import Window

__all__ = ("State",)


class State:
    def __init__(
        self, parent_window: Optional[Window] = None, border: Optional[Colour] = None
    ) -> None:
        self.parent_window = parent_window
        self.border = border

    def set_size(self, width: int, height: int) -> None: ...

    def set_rel_size(self, width: float, height: float) -> None: ...

    def set_pos(self, x: int, y: int) -> None: ...

    def set_rel_pos(self, x: float, y: float) -> None: ...

    def update(self) -> None: ...
