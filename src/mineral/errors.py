from __future__ import annotations

from typing import TYPE_CHECKING

from .window import Window

if TYPE_CHECKING:
    from typing import Any, Optional


class BaseError(Exception):
    r"""The base class to all Mineral errors."""

    def __init__(
        self, *args: Any, last_state: Optional[Window] = None, **kwargs: Any
    ) -> None:
        super().__init__(*args)

        self.last_state: Optional[Window] = last_state
        for key, value in kwargs.items():
            setattr(self, key, value)


class WindowError(BaseError):
    r"""Raised when an operation is done over an invalid state."""


class WindowLoadError(BaseError):
    r"""Raised when an error occurs in loading / unloading a state."""
