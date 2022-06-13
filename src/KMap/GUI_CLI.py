"""Create a GUI to solve and manipulate Karnaugh Maps from the command line

Functions:

    cli() -> (None)

Misc variables:

    __all__
    __author__
    __version__
    supported_from
"""

__all__ = ["cli"]
__author__ = "Alexander Bisland"
__version__ = "1.2.1"
supported_from = "3.8.1"

from KMap import GUI


def cli() -> None:
    """Create the GUI

        Parameters:
            (None)

        Returns:
            Nothing (None): Null
    """
    GUI.WindowManager.start_GUI()


if __name__ == "__main__":
    cli()
