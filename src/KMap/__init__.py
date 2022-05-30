"""Dependency-free library to create Karnaugh Map objects which can be solved and manipulated.
To see info on the mapper use help(KMap.Mapper) or help(KMap.KarnaughMap)

Classes:

    KarnaughMap

Functions:

    KarnaughMapObject.create_map(tot_input=None, expression=None) -> (bool) success
    KarnaughMapObject.print(object, file) -> (None)
    KarnaughMapObject.to_string(object, file) -> (str) reader-friendly table
    KarnaughMap.get_tot_variables(expression: str) -> (Union[int, None]) total number of variables
    KarnaughMapObject.solve_map(self: object) -> (str) simplified binary logic representation of map

Misc variables:

    __all__
    __author__
    __version__
    supported_from
"""

__all__ = ["KarnaughMap"]
__author__ = "Alexander Bisland"
__version__ = "1.5.1"
supported_from = "3.8.1"

from .Mapper import KarnaughMap
from .GUI import App
