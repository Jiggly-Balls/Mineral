from __future__ import annotations

from typing import TYPE_CHECKING

from .types import MISSING

if TYPE_CHECKING:
    from typing import Any, List, Optional

    from .state import State
    from .window_manager import WindowManager


class Window:
    """The Window class which works as an individual screen.

    :attributes:
        window_name: :class:`str`
            The name of the Window. Has to be unique among other windows.
        manager: :class:`WindowManager`
            The manager to which the Window is binded to.
    """

    window_name: str = MISSING
    manager: WindowManager = MISSING
    states: List[State] = []

    def __init_subclass__(cls, *, window_name: Optional[str] = None) -> None:
        cls.window_name = window_name or cls.__name__

    def add_state(self, state: State) -> None:
        Window.states.append(state)
    
    def remove_state(self, state: State) -> None:
        Window.states.remove(state)

    def on_setup(self) -> None:
        r"""This listener is only called once while being loaded into the ``WindowManager``.
        This is also called when reloading the Window.
        """
        pass

    def on_enter(self, prevous_window: Optional[Window]) -> None:
        r"""This listener is called once when a Window has been switched and is
        entering the current Window.

        :param prevous_window:
            | The Window that was running previously. If there are no previous windows,
            | ``None`` is passed
        """
        pass

    def on_leave(self, next_window: Window) -> None:
        r"""This listener is called once when the Window has been switched and is exiting
        the current one.

        :param next_window:
            | The next Window that is going to be applied.
        """
        pass

    def update(self, *args: Any) -> None:
        r"""The update process of the window. The main logic of the app must reside in the
        State instead of the Window.

        :param \*args:
            | The arguments to be passed on to the update counter.
        """
        pass
