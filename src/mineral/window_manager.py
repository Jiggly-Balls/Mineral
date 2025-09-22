from __future__ import annotations

import importlib
import inspect
from typing import TYPE_CHECKING

from .errors import WindowError, WindowLoadError
from .window import Window

if TYPE_CHECKING:
    from collections.abc import Callable
    from inspect import Signature
    from typing import Any, Dict, NoReturn, Optional, Tuple, Type


_GLOBAL_ON_SETUP_ARGS: int = 1
_GLOBAL_ON_ENTER_ARGS: int = 2
_GLOBAL_ON_LEAVE_ARGS: int = 2
_KW_CONSIDER: Tuple[str, str] = ("VAR_KEYWORD", "KEYWORD_ONLY")


class WindowManager:
    """The Window Manager used for managing multiple Window(s).

    :param window:
        The main game window.

    :attributes:
        is_running: :class:`bool`
            A bool for controlling the game loop. ``True`` by default.
    """

    def __init__(self) -> None:
        Window.manager = self

        self.is_running: bool = True

        self._global_on_setup: Optional[Callable[[Window], None]] = None
        self._global_on_enter: Optional[
            Callable[[Window, Optional[Window]], None]
        ] = None
        self._global_on_leave: Optional[
            Callable[[Optional[Window], Window], None]
        ] = None

        self._windows: Dict[str, Window] = {}
        self._current_window: Optional[Window] = None
        self._last_window: Optional[Window] = None

    def _get_kw_args(self, signature: Signature) -> int:
        amount = 0
        for param in signature.parameters.values():
            if param.kind in _KW_CONSIDER:
                amount += 1
        return amount

    def _get_pos_args(self, signature: Signature) -> int:
        amount = 0
        for param in signature.parameters.values():
            if param.kind not in _KW_CONSIDER:
                amount += 1
        return amount

    @property
    def current_window(self) -> Optional[Window]:
        """The current window if applied. Will be ``None`` otherwise.

        .. note::
            This is a read-only attribute. To change windows use
            ``WindowManger.change_window`` instead.
        """
        return self._current_window

    @current_window.setter
    def current_window(self, _: Any) -> NoReturn:
        raise ValueError(
            "Cannot overwrite the current window. Use `WindowManager.change_window` instead."
        )

    @property
    def global_on_enter(
        self,
    ) -> Optional[Callable[[Window, Optional[Window]], None]]:
        """The global on_enter listener called right before a window's on_enter listener.

        .. note::
            This has to be assigned before changing the windows.

        The first argument passed to the function is the current window and the second
        is the previous window which may be ``None``.

        Example for a ``global_on_enter`` function-

        .. code-block:: python

            def global_on_enter(
                current_window: Window, previous_window: None | Window
            ) -> None:
                if previous_window:
                    print(
                        f"GLOBAL ENTER - Entering {current_window.window_name} from {previous_window.window_name}"
                    )
        """
        return self._global_on_enter

    @global_on_enter.setter
    def global_on_enter(
        self, value: Callable[[Window, Optional[Window]], None]
    ) -> None:
        on_enter_signature = inspect.signature(value)
        pos_args = self._get_pos_args(on_enter_signature)
        kw_args = self._get_kw_args(on_enter_signature)

        if (
            len(on_enter_signature.parameters) != _GLOBAL_ON_ENTER_ARGS
            or kw_args != 0
        ):
            raise TypeError(
                f"Expected {_GLOBAL_ON_ENTER_ARGS} positional argument(s) only "
                f"for the function to be assigned to global_on_enter. "
                f"Instead got {pos_args} positional argument(s)"
                + (
                    f" and {kw_args} keyword argument(s)."
                    if kw_args > 0
                    else "."
                )
            )

        self._global_on_enter = value

    @property
    def global_on_leave(
        self,
    ) -> Optional[Callable[[Optional[Window], Window], None]]:
        """The global on_leave listener called right before a window's on_leave listener.

        .. note::
            This has to be assigned before changing the windows.

        The first argument passed to the function is the current window which may be
        ``None`` and the second is the next window to take place.

        Example for a ``global_on_leave`` function-

        .. code-block:: python

            def global_on_leave(
                current_window: None | Window, next_window: Window
            ) -> None:
                if current_window:
                    print(
                        f"GLOBAL LEAVE - Leaving {current_window.window_name} to {next_window.window_name}"
                    )
        """
        return self._global_on_leave

    @global_on_leave.setter
    def global_on_leave(
        self, value: Callable[[Optional[Window], Window], None]
    ) -> None:
        on_leave_signature = inspect.signature(value)
        pos_args = self._get_pos_args(on_leave_signature)
        kw_args = self._get_kw_args(on_leave_signature)

        if (
            len(on_leave_signature.parameters) != _GLOBAL_ON_LEAVE_ARGS
            or kw_args != 0
        ):
            raise TypeError(
                f"Expected {_GLOBAL_ON_LEAVE_ARGS} positional argument(s) only "
                f"for the function to be assigned to global_on_leave. "
                f"Instead got {pos_args} positional argument(s)"
                + (
                    f" and {kw_args} keyword argument(s)."
                    if kw_args > 0
                    else "."
                )
            )

        self._global_on_leave = value

    @property
    def global_on_setup(self) -> Optional[Callable[[Window], None]]:
        """The global ``on_setup`` function for all windows.

        .. note::
            This has to be assigned before loading the windows into the manager.

        The first argument passed to the function is the current window which has been
        setup.

        Example for a ``global_on_setup`` function-

        .. code-block:: python

            def global_setup(window: Window) -> None:
                print(f"GLOBAL SETUP - Setting up window: {window.window_name}")
        """
        return self._global_on_setup

    @global_on_setup.setter
    def global_on_setup(self, value: Callable[[Window], None]) -> None:
        on_setup_signature = inspect.signature(value)
        pos_args = self._get_pos_args(on_setup_signature)
        kw_args = self._get_kw_args(on_setup_signature)

        if (
            len(on_setup_signature.parameters) != _GLOBAL_ON_SETUP_ARGS
            or kw_args != 0
        ):
            raise TypeError(
                f"Expected {_GLOBAL_ON_SETUP_ARGS} positional argument(s) only "
                f"for the function to be assigned to global_on_setup. "
                f"Instead got {pos_args} positional argument(s)"
                + (
                    f" and {kw_args} keyword argument(s)."
                    if kw_args > 0
                    else "."
                )
            )

        self._global_on_setup = value

    @property
    def last_window(self) -> Optional[Window]:
        """The last window object if any. Will be ``None`` otherwise

        .. note::
            This is a read-only attribute.
        """
        return self._last_window

    @last_window.setter
    def last_window(self, _: Any) -> NoReturn:
        raise ValueError("Cannot overwrite the last window.")

    @property
    def window_map(self) -> Dict[str, Window]:
        """A dictionary copy of all the window names mapped to their respective instance.

        .. note::
            This is a read-only attribute.
        """
        return self._windows.copy()

    @window_map.setter
    def window_map(self, _: Any) -> NoReturn:
        raise ValueError("Cannot overwrite the window map.")

    def change_window(self, window_name: str) -> None:
        """Changes the current window and updates the last window. This method executes
        the ``on_leave`` & ``on_enter`` window & global listeners.

        :param window_name:
            | The name of the Window you want to switch to.

        :raises:
            :exc:`WindowError`
                | Raised when the window name doesn't exist in the manager.
        """

        if window_name not in self._windows:
            raise WindowError(
                f"Window `{window_name}` isn't present from the available windows: "
                f"`{', '.join(self.window_map.keys())}`.",
                last_window=self._last_window,
            )

        self._last_window = self._current_window
        self._current_window = self._windows[window_name]
        if self._global_on_leave:
            self._global_on_leave(self._last_window, self._current_window)

        if self._last_window:
            self._last_window.on_leave(self._current_window)

        if self._global_on_enter:
            self._global_on_enter(self._current_window, self._last_window)
        self._current_window.on_enter(self._last_window)

    def connect_window_hook(self, path: str, **kwargs: Any) -> None:
        r"""Calls the hook function of the window file.

        :param path:
            | The path to the Window file containing the hook function to be called.
        :param \**kwargs:
            | The keyword arguments to be passed to the hook function.

        :raises:
            :exc:`WindowError`
                | Raised when the hook function was not found in the window file to be loaded.
        """

        window = importlib.import_module(path)
        hook_func = window.__dict__.get("hook")
        if hook_func is None:
            raise WindowError(
                "\nAn error occurred in loading Window Path-\n"
                f"`{path}`\n"
                "`hook` function was not found in window file to load.\n",
                last_window=self._last_window,
                **kwargs,
            )

        hook_func(**kwargs)

    def load_windows(
        self, *windows: Type[Window], force: bool = False, **kwargs: Any
    ) -> None:
        r"""Loads the Windows into the WindowManager.

        :param windows:
            | The Windows to be loaded into the manager.

        :param force:
            | Default ``False``.
            |
            | Loads the Window regardless of whether the Window has already been loaded or not
            | without raising any internal error.

            .. warning::
              If set to ``True`` it may lead to unexpected behavior.

        :param \**kwargs:
            | The keyword arguments to be passed to the Window's subclass on instantiation.

        :raises:
            :exc:`WindowLoadError`
                | Raised when the window has already been loaded.
                | Only raised when ``force`` is set to ``False``.

            :exc:`WindowError`
                | Raised when the passed argument(s) is not subclassed from ``Window``.
        """

        for window in windows:
            if not issubclass(window, Window):
                raise WindowError(
                    "The passed argument(s) is not a subclass of Window.",
                    last_window=self._last_window,
                    **kwargs,
                )

            if not force and window.window_name in self._windows:
                raise WindowLoadError(
                    f"Window: {window.window_name} has already been loaded.",
                    last_window=self._last_window,
                    **kwargs,
                )

            self._windows[window.window_name] = window(**kwargs)
            if self._global_on_setup:
                self._global_on_setup(self._windows[window.window_name])
            self._windows[window.window_name].on_setup()

    def reload_window(
        self, window_name: str, force: bool = False, **kwargs: Any
    ) -> Window:
        r"""Reloads the specified Window. A short hand to ``WindowManager.unload_window`` &
        ``WindowManager.load_window``.

        :param window_name:
            | The ``Window`` name to be reloaded.

        :param force:
            | Default ``False``.
            |
            | Reloads the Window even if it's an actively running Window without
            | raising any internal error.

            .. warning::
              If set to ``True`` it may lead to unexpected behavior.

        :param \**kwargs:
            | The keyword arguments to be passed to the
            | ``WindowManager.unload_window`` & ``WindowManager.load_window``.

        :returns:
            | Returns the newly made :class:`Window` instance.

        :raises:
            :exc:`WindowLoadError`
                | Raised when the window has already been loaded.
                | Only raised when ``force`` is set to ``False``.
        """

        deleted_cls = self.unload_window(
            window_name=window_name, force=force, **kwargs
        )
        self.load_windows(deleted_cls, force=force, **kwargs)
        return self._windows[window_name]

    def unload_window(
        self, window_name: str, force: bool = False, **kwargs: Any
    ) -> Type[Window]:
        r"""Unloads the ``Window`` from the ``WindowManager``.

        :param window_name:
            | The Window to be loaded into the manager.

        :param force:
            | Default ``False``.
            |
            | Unloads the Window even if it's an actively running Window without raising any
            | internal error.

            .. warning::
              If set to ``True`` it may lead to unexpected behavior.

        :param \**kwargs:
            | The keyword arguments to be passed on to the raised errors.

        :returns:
            | The :class:`Window` class of the deleted Window name.

        :raises:
            :exc:`WindowLoadError`
                | Raised when the window doesn't exist in the manager to be unloaded.

            :exc:`WindowError`
                | Raised when trying to unload an actively running Window.
                | Only raised when ``force`` is set to ``False``.
        """

        if window_name not in self._windows:
            raise WindowLoadError(
                f"Window: {window_name} doesn't exist to be unloaded.",
                last_window=self._last_window,
                **kwargs,
            )

        elif (
            not force
            and self._current_window is not None
            and window_name == self._current_window.window_name
        ):
            raise WindowError(
                "Cannot unload an actively running window.",
                last_window=self._last_window,
                **kwargs,
            )

        cls_ref = self._windows[window_name].__class__
        del self._windows[window_name]
        return cls_ref
