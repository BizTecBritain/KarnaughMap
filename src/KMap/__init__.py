"""Dependency-free library to create Karnaugh Map objects which can be solved and manipulated.
To see info on the mapper use help(KMap.Mapper) or help(KMap.KarnaughMap)
To see info on the GUI use help(KMap.GUI) or help(KMap.App)

Classes:

    KarnaughMap
    App
    WindowManager

Functions:

    KarnaughMap.reset(self: _KMap) -> None
    KarnaughMap.create_map(self: _KMap, tot_input: int = None, expression: str = None) -> (bool) success
    KarnaughMap.print(self: _KMap) -> (None)
    KarnaughMap.to_string(self: _KMap) -> (str) reader-friendly table
    @staticmethod KarnaughMap.get_tot_variables(expression: str) -> (Union[int, None]) total number of variables
    KarnaughMap.solve_map(self: _KMap) -> (str) simplified binary logic representation of map

    App.rescale(self: _App, _: Optional[Event] = None) -> (None)
    App.rounded_rect(self: _App, x: int, y: int, w: int, h: int, c: int, grid: bool = True) -> (None)
    App.toggle_geom(self: _App, _: Optional[Event] = None) -> (None)
    App.toggle_fullscreen(self: _App, _: Optional[Event] = None) -> (None)
    App.toggle_mode(self: _App, button: _ToggleButton = None) -> (None)
    App.toggle_state(self: _App, state: int, button: _ToggleButton = None) -> (None)
    App.solve(self: _App, _: Optional[Event] = None) -> (None)
    App.flash_groups(self: _App, index: int) -> (None)
    App.change_map(self: _App, event: Event) -> (None)
    App.solve_from_mod_map(self: _App) -> (None)
    App.reset_old_map(self: _App) -> (None)

    @staticmethod WindowManager.open_credits() -> (None)
    @staticmethod WindowManager.open_help() -> (None)
    @staticmethod WindowManager.open_settings(window: _App) -> (None)
    @staticmethod WindowManager.start_GUI() -> (None)

Misc variables:

    __all__
    __author__
    __version__
    supported_from

Other Info:
    To easily run the GUI run the method KMap.WindowManager.start_GUI()
"""

__all__ = ["KarnaughMap", "App", "WindowManager"]
__author__ = "Alexander Bisland"
__version__ = "1.6.2"
supported_from = "3.8.1"

from .Mapper import KarnaughMap
from .GUI import App, WindowManager
