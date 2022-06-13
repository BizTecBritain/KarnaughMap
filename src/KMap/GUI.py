"""Create a GUI to solve and manipulate Karnaugh Maps.

Classes:

    Public:
        App
        WindowManager
    Private:
        _ToggleButton
        _SettingsApp
        _CreditsApp
        _HelpApp

Functions:

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
"""

__all__ = ["App", "WindowManager"]
__author__ = "Alexander Bisland"
__version__ = "3.4.1"
supported_from = "3.8.1"

from tkinter import Tk, Button, Canvas, PhotoImage, Label, Frame, Entry, Spinbox, Misc, Event
from typing import TypeVar, Optional, Callable
from .Mapper import KarnaughMap
import os
import configparser

_App = TypeVar("_App", bound="App")
_ToggleButtonVar = TypeVar("_ToggleButtonVar", bound="_ToggleButton")
_SettingsAppVar = TypeVar("_SettingsAppVar", bound="_SettingsApp")
_CreditsAppVar = TypeVar("_CreditsAppVar", bound="_CreditsApp")
_HelpAppVar = TypeVar("_HelpAppVar", bound="_HelpApp")


class _ToggleButton(Canvas):
    """Widget Inherting methods from canvas that represents a toggle button

    Functions:

        _ToggleButton.get_state(self: _ToggleButtonVar) -> (int) position of the button - 0 or 1

    Class variables:

        Public:
            self.master    - the master (parent) widget/window of this widget
            self.state = 0 - value depicting the state/position of the toggle button
        Private:
            self._day
            self._night
            self._button
    """
    def __init__(self: _ToggleButtonVar, master: Optional[Misc], command: Optional[Callable] = None,
                 file0: str = "night.gif", file1: str = "day.gif", default: int = 0, *args, **kwargs) -> None:
        """Constructor for the class

            Parameters:
                self (_ToggleButtonVar):      The instantiated object
                master (Optional[Misc]):      The master (parent) widget/window of this widget
                command (Optional[Callable]): A command to call on the change of state of this toggle button
                file0 (str):                  Path to file for 0 (off) image
                file1 (str):                  Path to file for 1 (on) image
                default (int):                Whether to start on 0 (off) or 1 (on)

            Returns:
                Nothing (None): Null
        """
        super().__init__(master, *args, **kwargs)
        self.master = master

        # get the images
        dir_path = os.path.dirname(os.path.realpath(__file__))
        self._day = PhotoImage(master=master, file=dir_path + "\\" + file1)
        self._night = PhotoImage(master=master, file=dir_path + "\\" + file0)
        self._button = Label(self, image=self._day, borderwidth=0, highlightthickness=0)
        self._button.pack()

        self._button.bind('<Button>', self._animate, add='+')
        self._button.bind('<Button>', command, add='+')

        self.state = 0
        if default:
            self._animate()

    def _animate(self: _ToggleButtonVar, _: Optional[Event] = None) -> None:
        """Change the images of the button to the alternate state

            Parameters:
                self (_ToggleButtonVar): The instantiated object
                _ (Optional[Event]):     The event data passed by bind function (Unused)

            Returns:
                Nothing (None): Null
        """
        curent_img = self._night
        if self.state:
            curent_img = self._day
        self._button.config(image=curent_img)
        self.state = int(not self.state)

    def get_state(self: _ToggleButtonVar) -> int:
        """Get the state of the button

            Parameters:
                self (_ToggleButtonVar): The instantiated object

            Returns:
                state (int): Position of the button 0 or 1
        """
        return self.state


class WindowManager:
    """Static class to open windows based on private classes

    Functions:

        @staticmethod WindowManager.open_credits() -> (None)
        @staticmethod WindowManager.open_help() -> (None)
        @staticmethod WindowManager.open_settings(window: _App) -> (None)
        @staticmethod WindowManager.start_GUI() -> (None)

    Class variables:

        (None)
    """
    @staticmethod
    def open_credits() -> None:
        """Create the credits window

            Parameters:
                (None)

            Returns:
                Nothing (None): Null
        """
        credits_window = Tk()
        _CreditsApp(credits_window)
        credits_window.mainloop()

    @staticmethod
    def open_help() -> None:
        """Create the help window

            Parameters:
                (None)

            Returns:
                Nothing (None): Null
        """
        help_window = Tk()
        _HelpApp(help_window)
        help_window.mainloop()

    @staticmethod
    def open_settings(window: _App) -> None:
        """Create the settings window

            Parameters:
                (None)

            Returns:
                Nothing (None): Null
        """
        settings_window = Tk()
        _SettingsApp(settings_window, window)
        settings_window.mainloop()

    @staticmethod
    def start_GUI() -> None:
        """Create the main GUI window

            Parameters:
                (None)

            Returns:
                Nothing (None): Null
        """
        root = Tk()
        App(root)
        root.mainloop()


class _CreditsApp:
    """Create a window to display the credits.

    Functions:

        (None)

    Class variables:

        (None)
    """
    def __init__(self: _CreditsAppVar, master: Tk) -> None:
        """Constructor for the class

            Parameters:
                self (_CreditsAppVar): The instantiated object
                master (Tk):           The master (parent) window of this app

            Returns:
                Nothing (None): Null
        """
        master.title("Credits")
        master.geometry("250x50")
        master.resizable(width=False, height=False)
        master.lift()
        master.focus_force()

        Label(master, text="Credits:\nThis utility is created by Alexander Bisland\n"
                           "Copyrighted BizTecBritain All rights reserved").pack()


class _HelpApp:
    """Create a window to display help information.

    Functions:

        (None)

    Class variables:

        (None)
    """
    def __init__(self: _HelpAppVar, master: Tk) -> None:
        """Constructor for the class

            Parameters:
                self (_HelpAppVar): The instantiated object
                master (Tk):        The master (parent) window of this app

            Returns:
                Nothing (None): Null
        """
        master.title("Help")
        master.geometry("350x200")
        master.resizable(width=False, height=False)
        master.lift()
        master.focus_force()

        Label(master, text="Help:\nJust type your equation and press solve\n\n"
                           "Aesthetical Help:\nToggle light and dark mode in settings\n\n"
                           "Also in settings:\nGroup Change: when set to automatic each group will be shown\n"
                           "without user input\n"
                           "Modify Map: Ability to modify the map just by clicking on it\n\n"
                           "Copyrighted BizTecBritain All rights reserved").pack()


class _SettingsApp:
    """Create a window to change the settings.

    Functions:

        _SettingsApp._save_data(self: _SettingsAppVar) -> (None)
        _SettingsApp.toggle_mode(self: _SettingsAppVar, _: Optional[Event] = None, init: bool = False) -> (None)
        _SettingsApp.toggle_auto(self: _SettingsAppVar, _: Optional[Event] = None) -> (None)
        _SettingsApp.toggle_modify(self: _SettingsAppVar, _: Optional[Event] = None) -> (None)

    Class variables:

        Public:
            self.master   - the master (parent) widget/window of this widget
            self.main_app - the main_app that the settings will apply to (must contain a class variable called states)
        Private:
            self._config
            self._frame
            self._day_night_btn
            self._day_night_btn_label
            self._auto_groups_btn
            self._auto_groups_btn_label
            self._modify_map_btn
            self._modify_map_btn_label
            self._credits
            self._close
    """
    def __init__(self: _SettingsAppVar, master: Tk, main_app: _App) -> None:
        """Constructor for the class

            Parameters:
                self (_SettingsAppVar): The instantiated object
                master (Tk):            The master (parent) window of this app
                main_app (_App):        The main app to change the settings for

            Returns:
                Nothing (None): Null
        """
        self.master = master
        self.master.title("Settings")
        self.master.geometry("250x150")
        self.master.resizable(width=False, height=False)
        self.master.lift()
        self.master.focus_force()
        self.main_app = main_app

        # set up config parser and create file to store data in
        self._config = configparser.ConfigParser()
        if os.path.exists(os.getenv('LOCALAPPDATA') + '\\KMap\\GUI.ini'):
            self._config.read(os.getenv('LOCALAPPDATA') + '\\KMap\\GUI.ini')
        if not os.path.exists(os.getenv('LOCALAPPDATA') + '\\KMap'):
            os.mkdir(os.getenv('LOCALAPPDATA') + '\\KMap')
        self.master.protocol("WM_DELETE_WINDOW", self._save_data)

        self._frame = Frame(self.master)
        self._frame.pack(anchor="nw", padx=3, pady=3)

        # create _ToggleButtons and buttons to open credits and close window
        self._day_night_btn = _ToggleButton(self._frame, self.toggle_mode, default=main_app.states[0])
        self._day_night_btn.grid(row=0, column=0)
        if main_app.states[0]:
            self._day_night_btn_label = Label(self._frame, text="Dark Mode Enabled")
        else:
            self._day_night_btn_label = Label(self._frame, text="Light Mode Enabled")
        self._day_night_btn_label.grid(row=0, column=1, sticky="w")

        self._auto_groups_btn = _ToggleButton(self._frame, self.toggle_auto, "on.gif", "off.gif", main_app.states[1])
        self._auto_groups_btn.grid(row=1, column=0)
        if main_app.states[1]:
            self._auto_groups_btn_label = Label(self._frame, text="Automatic Group Change")
        else:
            self._auto_groups_btn_label = Label(self._frame, text="Manual Group Change")
        self._auto_groups_btn_label.grid(row=1, column=1, sticky="w")

        self._modify_map_btn = _ToggleButton(self._frame, self.toggle_modify, "on.gif", "off.gif", main_app.states[2])
        self._modify_map_btn.grid(row=2, column=0)
        if main_app.states[2]:
            self._modify_map_btn_label = Label(self._frame, text="Modify Map Enabled")
        else:
            self._modify_map_btn_label = Label(self._frame, text="Modify Map Disabled")
        self._modify_map_btn_label.grid(row=2, column=1, sticky="w")

        self._credits = Button(self.master, text="Credits", command=WindowManager.open_credits)
        self._credits.pack(pady=3)
        self._close = Button(self.master, text="Close Window", command=self._save_data)
        self._close.pack(pady=3)

        self.toggle_mode(init=True)

    def _save_data(self: _SettingsAppVar) -> None:
        """Save the settings data for next time app opens

            Parameters:
                self (_SettingsAppVar): The instantiated object

            Returns:
                Nothing (None): Null
        """
        with open(os.getenv('LOCALAPPDATA') + '\\KMap\\GUI.ini', 'w') as configfile:
            self._config['SETTINGS'] = {'Mode': self.main_app.states[0],
                                        'Auto': self.main_app.states[1],
                                        'Modify': self.main_app.states[2]}
            self._config.write(configfile)
        self.master.destroy()

    def toggle_mode(self: _SettingsAppVar, _: Optional[Event] = None, init: bool = False) -> None:
        """Toggle the mode of the main app to light/dark

            Parameters:
                self (_SettingsAppVar): The instantiated object
                _ (Optional[Event]):    The event data passed by bind function (Unused)
                init (bool):            Whether the call is to initialise the button or if it has actually been clicked

            Returns:
                Nothing (None): Null
        """
        if not init:
            self.main_app.toggle_mode(self._day_night_btn)
        if self.main_app.states[0]:
            # toggle light dark for current settings app first as well as main app
            self._day_night_btn_label.configure(text="Dark Mode Enabled")
            self.master.configure(bg="#121212")
            self._frame.configure(bg="#121212")
            self._day_night_btn_label.configure(fg="white", bg="#121212")
            self._auto_groups_btn_label.configure(fg="white", bg="#121212")
            self._modify_map_btn_label.configure(fg="white", bg="#121212")
            self._auto_groups_btn.grid_forget()
            self._auto_groups_btn = _ToggleButton(self._frame, self.toggle_auto, "ondark.png", "offdark.png",
                                                  self.main_app.states[1])
            self._auto_groups_btn.grid(row=1, column=0)
            self._modify_map_btn.grid_forget()
            self._modify_map_btn = _ToggleButton(self._frame, self.toggle_modify, "ondark.png", "offdark.png",
                                                 self.main_app.states[2])
            self._modify_map_btn.grid(row=2, column=0)
            self._credits.configure(bg="purple", fg="white")
            self._close.configure(bg="purple", fg="white")
        else:
            self._day_night_btn_label.configure(text="Light Mode Enabled")
            self.master.configure(bg="SystemButtonFace")
            self._frame.configure(bg="SystemButtonFace")
            self._day_night_btn_label.configure(fg="black", bg="SystemButtonFace")
            self._auto_groups_btn_label.configure(fg="black", bg="SystemButtonFace")
            self._modify_map_btn_label.configure(fg="black", bg="SystemButtonFace")
            self._auto_groups_btn.grid_forget()
            self._auto_groups_btn = _ToggleButton(self._frame, self.toggle_auto, "on.gif", "off.gif",
                                                  self.main_app.states[1])
            self._auto_groups_btn.grid(row=1, column=0)
            self._modify_map_btn.grid_forget()
            self._modify_map_btn = _ToggleButton(self._frame, self.toggle_modify, "on.gif", "off.gif",
                                                 self.main_app.states[2])
            self._modify_map_btn.grid(row=2, column=0)
            self._credits.configure(bg="lightblue", fg="black")
            self._close.configure(bg="lightblue", fg="black")

    def toggle_auto(self: _SettingsAppVar, _: Optional[Event] = None) -> None:
        """Toggle the mode of the main app to manual/automatic group change

            Parameters:
                self (_SettingsAppVar): The instantiated object
                _ (Optional[Event]):    The event data passed by bind function (Unused)

            Returns:
                Nothing (None): Null
        """
        self.main_app.toggle_state(1, self._auto_groups_btn)
        if self.main_app.states[1]:
            self._auto_groups_btn_label.configure(text="Automatic Group Change")
        else:
            self._auto_groups_btn_label.configure(text="Manual Group Change")

    def toggle_modify(self: _SettingsAppVar, _: Optional[Event] = None) -> None:
        """Toggle the mode of the main app to modify map disabled/enabled

            Parameters:
                self (_SettingsAppVar): The instantiated object
                _ (Optional[Event]):    The event data passed by bind function (Unused)

            Returns:
                Nothing (None): Null
        """
        self.main_app.toggle_state(2, self._modify_map_btn)
        if self.main_app.states[2]:
            self._modify_map_btn_label.configure(text="Modify Map Enabled")
        else:
            self._modify_map_btn_label.configure(text="Modify Map Disabled")


class App:
    """Main GUI to display the Karnaugh map and contain a UI to communicate with it

    Functions:

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

    Class variables:

        Public:
            self.kmap = KarnaughMap(raise_error=True, debug=False)  - KarnaughMap object to solve the users input
            self.solution = ""                                      - the solution to the map
            self.groups = []                                        - the seperate groups that make up the solution
            self.states = [0, 0, 0]                                 - the settings (Changed by _SettingsApp):
                                                                          light/dark mode
                                                                          manual/automatic group change
                                                                          modify map disabled/enabled
            self.widget_fg = ""                                     - colour of the fg of widgets
            self.main_bg = ""                                       - colour of the main apps bg
            self.widget_bg = ""                                     - colour of the bg of widgets
            self.canvas_bg = ""                                     - colour of the canvas where the map is drawn
            self.expression_fg = ""                                 - colour of the expression and solution text
            self.highlight_bg = ""                                  - colour of the squares on the map that are
                                                                      highlighted
            self.font_size = 20                                     - font size of text (scaled with window)
            self.cur_group = 0                                      - index of current group being displayed
            self.modified = False                                   - boolean to show if the map has been modified
            self.reset_table = ""                                   - the data that was shown by the map before it was
                                                                      modified
            self.master                                             - the master (parent) widget/window of this widget
        Private:
            self._job = None
            self._geom = '640x360+0+0'
            self._open_settings
            self._open_help
            self._canvas
            self._result_frame
            self._result_frame_widgets = []
            self._input_frame
            self._expression_entry
            self._solve_button
            self._slider_frame
            self._slider
            self._slider_label
            self._next_group
            self._error_message
            self._solve_from_map
            self._reset_map

    Other data:

        Order of operations: BNAO
        Only tested up to 4 variables
    """
    def __init__(self: _App, master: Tk) -> None:
        """Constructor for the class

            Parameters:
                self (_App): The instantiated object
                master (Tk): The master (parent) window of this app

            Returns:
                Nothing (None): Null
        """
        self.kmap = KarnaughMap(raise_error=True, debug=False)
        self.solution = ""
        self.groups = []
        self.states = [0, 0, 0]
        self.widget_fg = ""
        self.main_bg = ""
        self.widget_bg = ""
        self.canvas_bg = ""
        self.expression_fg = ""
        self.highlight_bg = ""
        self.font_size = 20
        self.cur_group = 0
        self.modified = False
        self.reset_table = ""
        self._job = None
        self._geom = '640x360+0+0'

        # try to read config data if it exists to reimport old settings
        config = configparser.ConfigParser()
        if os.path.exists(os.getenv('LOCALAPPDATA') + '\\KMap\\GUI.ini'):
            config.read(os.getenv('LOCALAPPDATA') + '\\KMap\\GUI.ini')
            try:
                self.states[0] = int(config["SETTINGS"]["Mode"])
                self.states[1] = int(config["SETTINGS"]["Auto"])
                self.states[2] = int(config["SETTINGS"]["Modify"])
            except KeyError:
                pass

        self.master = master
        self.master.title("Karnaugh Map")
        self.master.geometry(self._geom)
        self.master.state('zoomed')
        self.master.bind('<Escape>', self.toggle_geom)
        self.master.bind('<F11>', self.toggle_fullscreen)

        self._open_settings = Button(self.master, text="Settings", command=lambda: WindowManager.open_settings(self))
        self._open_settings.place(x=4, y=3)

        self._open_help = Button(self.master, text="Help", command=WindowManager.open_help)
        self._open_help.pack(pady=3, padx=4, anchor="e")

        self._canvas = Canvas(self.master, width=500, height=500, bd=0, highlightthickness=0)
        self._canvas.pack(pady=3)
        self._canvas.bind("<Button-1>", self.change_map)

        self._result_frame = Frame(self._canvas)
        self._result_frame.pack(pady=3)
        self._result_frame_widgets = []

        self._input_frame = Frame(self.master)
        self._input_frame.pack()
        self._expression_entry = Entry(self._input_frame, highlightthickness=2)
        self._expression_entry.grid(column=0, row=0, padx=2)
        self._expression_entry.bind('<Return>', self.solve)
        self._solve_button = Button(self._input_frame, text='Solve', command=self.solve)
        self._solve_button.grid(column=1, row=0, padx=2)
        self._expression_entry.focus_set()

        self._slider_frame = Frame(self.master)
        self._slider = Spinbox(self._slider_frame, from_=1, to=10, width=3)
        self._slider.delete(0, "end")
        self._slider.insert(0, "5")
        self._slider.grid(column=1, row=0)
        self._slider_label = Label(self._slider_frame, text="Speed: ", width=7)
        self._slider_label.grid(column=0, row=0)

        self._next_group = Button(self.master, text="Next Group", command=lambda: self.flash_groups(self.cur_group + 1))

        self._error_message = Label(self.master, fg="red")

        self._solve_from_map = Button(self.master, text="Solve From Map", command=self.solve_from_mod_map)
        self._reset_map = Button(self.master, text="Reset Map", command=self.reset_old_map)

        self.toggle_mode()
        self.master.bind("<Configure>", self.rescale)
        self.rescale()

    def rescale(self: _App, _: Optional[Event] = None) -> None:
        """Rescale all the font sizes as the window size changes then redraw the map with self.rescale()

            Parameters:
                self (_App):         The instantiated object
                _ (Optional[Event]): The event data passed by bind function (Unused)

            Returns:
                Nothing (None): Null
        """
        height = self.master.winfo_height()
        width = self.master.winfo_width()
        # calculate font width based on width or height depending on which is smaller
        self.font_size = str((width if width < height else height) // 50)
        self._canvas.configure(width=width * 0.8, height=height * 0.65)
        self._expression_entry.configure(font=(None, int(self.font_size)))
        self._solve_button.configure(font=(None, int(self.font_size)))
        self._next_group.configure(font=(None, int(self.font_size)))
        self._solve_from_map.configure(font=(None, int(self.font_size)))
        self._reset_map.configure(font=(None, int(self.font_size)))
        self._error_message.configure(font=(None, int(self.font_size)))
        self._slider.configure(font=(None, int(self.font_size)))
        self._slider_label.configure(font=(None, int(self.font_size)))
        element: Label
        for element in self._result_frame.winfo_children():
            element.configure(font="Times {} bold".format(int(int(self.font_size) * 1.5)))
        self.rounded_rect(0, 0, int(width * 0.8 - 1), int(height * 0.65 - 1), 15)

    def rounded_rect(self: _App, x: int, y: int, w: int, h: int, c: int, grid: bool = True) -> None:
        """Change the images of the button to the alternate state

            Parameters:
                self (_App): The instantiated object
                x (int):     The x position of the top left of the canvas
                y (int):     The y position of the top left of the canvas
                w (int):     The width of the canvas
                h (int):     The height of the canvas
                c (int):     The radius of the corners
                grid (bool): Whether to draw the map or not

            Returns:
                Nothing (None): Null
        """
        self._canvas.delete("all")  # delete everything on the canvas
        # corners are drawn as 2 seperate pieces, a pieslice which has the centre filled and an arc for a border
        self._canvas.create_arc(x, y, x + 2 * c, y + 2 * c, start=90, extent=90, style="pieslice", fill=self.canvas_bg,
                                outline=self.canvas_bg)
        self._canvas.create_arc(x, y, x + 2 * c, y + 2 * c, start=90, extent=90, style="arc", outline=self.widget_fg)
        self._canvas.create_arc(x + w - 2 * c, y + h - 2 * c, x + w, y + h, start=270, extent=90, style="pieslice",
                                fill=self.canvas_bg, outline=self.canvas_bg)
        self._canvas.create_arc(x + w - 2 * c, y + h - 2 * c, x + w, y + h, start=270, extent=90, style="arc",
                                outline=self.widget_fg)
        self._canvas.create_arc(x + w - 2 * c, y, x + w, y + 2 * c, start=0, extent=90, style="pieslice",
                                fill=self.canvas_bg, outline=self.canvas_bg)
        self._canvas.create_arc(x + w - 2 * c, y, x + w, y + 2 * c, start=0, extent=90, style="arc",
                                outline=self.widget_fg)
        self._canvas.create_arc(x, y + h - 2 * c, x + 2 * c, y + h, start=180, extent=90, style="pieslice",
                                fill=self.canvas_bg, outline=self.canvas_bg)
        self._canvas.create_arc(x, y + h - 2 * c, x + 2 * c, y + h, start=180, extent=90, style="arc",
                                outline=self.widget_fg)
        # rectangles are used to fill the centre with a colour
        self._canvas.create_rectangle(x + c, y, x + w - c, y + h, fill=self.canvas_bg, outline=self.canvas_bg)
        self._canvas.create_rectangle(x, y + c, x + w, y + h - c, fill=self.canvas_bg, outline=self.canvas_bg)
        # create the border
        self._canvas.create_line(x + c, y, x + w - c, y, fill=self.widget_fg)
        self._canvas.create_line(x + c, y + h, x + w - c, y + h, fill=self.widget_fg)
        self._canvas.create_line(x, y + c, x, y + h - c, fill=self.widget_fg)
        self._canvas.create_line(x + w, y + c, x + w, y + h - c, fill=self.widget_fg)
        # if possible draw the actual map
        if grid:
            try:
                # draw empty boxes
                num_columns = len(self.kmap.table) + 1
                num_rows = len(self.kmap.table[0]) + 1
                width, height = self._canvas.winfo_width(), self._canvas.winfo_height()
                box_size = (height * 0.7) // num_columns if width * (num_rows / num_columns) > height \
                    else (width * 0.7) // num_rows
                for column in range(1, num_columns):
                    box_y = column * box_size + (height // 2 - (box_size * num_columns // 2))
                    for row in range(1, num_rows):
                        box_x = row * box_size + (width // 2 - (box_size * num_rows // 2))
                        self._canvas.create_rectangle(box_x, box_y, box_x + box_size, box_y + box_size,
                                                      fill=self.widget_bg, outline=self.widget_fg)
                        self._canvas.create_text(box_x + box_size // 2, box_y + box_size // 2, fill=self.widget_fg,
                                                 text=self.kmap.table[column - 1][row - 1],
                                                 font="Times {} bold".format(self.font_size))
                # add values to boxes
                headings = KarnaughMap.VALUES[self.kmap.tot_input]
                for index, heading in enumerate(headings[0]):
                    box_y = height // 2 - (box_size * num_columns // 2)
                    box_x = (index + 1) * box_size + (width // 2 - (box_size * num_rows // 2))
                    self._canvas.create_text(box_x + box_size // 2, box_y + box_size // 2, text=heading,
                                             fill=self.widget_fg, font="Times {} bold".format(self.font_size))
                for index, heading in enumerate(headings[1]):
                    box_y = (index + 1) * box_size + (height // 2 - (box_size * num_columns // 2))
                    box_x = width // 2 - (box_size * num_rows // 2)
                    self._canvas.create_text(box_x + box_size // 2, box_y + box_size // 2, text=heading,
                                             fill=self.widget_fg, font="Times {} bold".format(self.font_size))
                # create headers
                rows = "".join(KarnaughMap.LETTERS[:len(KarnaughMap.VALUES[self.kmap.tot_input][0][0])])
                columns = "".join(KarnaughMap.LETTERS[len(KarnaughMap.VALUES[self.kmap.tot_input][0][0]):
                                                      len(KarnaughMap.VALUES[self.kmap.tot_input][0][0]) +
                                                      len(KarnaughMap.VALUES[self.kmap.tot_input][1][0])])
                letters_y = height // 2 - (box_size * num_columns // 2)
                letters_x = width // 2 - (box_size * num_rows // 2)
                self._canvas.create_text(letters_x + (3 * box_size) // 4, letters_y + box_size // 2, text=rows.upper(),
                                         fill=self.widget_fg, font="Times {} bold".format(self.font_size))
                self._canvas.create_text(letters_x + box_size // 2, letters_y + (3 * box_size) // 4,
                                         fill=self.widget_fg, text=columns.upper(),
                                         font="Times {} bold".format(self.font_size))

            except (ZeroDivisionError, IndexError):
                self.rounded_rect(x, y, w, h, c, False)

    def toggle_geom(self: _App, _: Optional[Event] = None) -> None:
        """Toggle betwwen fullscreen and not fullscreen

            Parameters:
                self (_App):         The instantiated object
                _ (Optional[Event]): The event data passed by bind function (Unused)

            Returns:
                Nothing (None): Null
        """
        if self.master.state() == 'zoomed':
            self.master.state('normal')
            self.master.geometry(self._geom)
        else:
            self.master.state('zoomed')

    def toggle_fullscreen(self: _App, _: Optional[Event] = None) -> None:
        """Toggle between true fullscreen (no taskbar) and not true fullscreen

            Parameters:
                self (_App):         The instantiated object
                _ (Optional[Event]): The event data passed by bind function (Unused)

            Returns:
                Nothing (None): Null
        """
        if self.master.attributes()[self.master.attributes().index('-fullscreen') + 1]:
            self.master.attributes('-fullscreen', False)
        else:
            self.master.attributes('-fullscreen', True)

    def toggle_mode(self: _App, button: _ToggleButton = None) -> None:
        """Toggle the mode between light and dark

            Parameters:
                self (_App):            The instantiated object
                button (_ToggleButton): The button that holds the data of which mode it is

            Returns:
                Nothing (None): Null
        """
        if button is None and self.states[0] == 1:
            self.widget_fg = "white"
            self.main_bg = "#121212"
            self.widget_bg = "purple"
            self.canvas_bg = "#343434"
            self.expression_fg = "magenta"
            self.highlight_bg = "#03DAC6"
            self.states[0] = 1
        elif button is None or not bool(button.get_state()):
            self.widget_fg = "black"
            self.main_bg = "SystemButtonFace"
            self.widget_bg = "lightblue"
            self.canvas_bg = "white"
            self.expression_fg = "darkblue"
            self.highlight_bg = "#A34C00"  # "#653594"
            self.states[0] = 0
        else:
            self.widget_fg = "white"
            self.main_bg = "#121212"
            self.widget_bg = "purple"
            self.canvas_bg = "#343434"
            self.expression_fg = "magenta"
            self.highlight_bg = "#03DAC6"
            self.states[0] = 1
        self.master.configure(bg=self.main_bg)
        self._canvas.configure(background=self.main_bg)
        self._input_frame.configure(background=self.main_bg)
        self._slider_frame.configure(background=self.main_bg)
        self._slider_label.configure(background=self.main_bg, foreground=self.widget_fg)
        self._solve_button.configure(background=self.widget_bg, foreground=self.widget_fg)
        self._solve_from_map.configure(background=self.widget_bg, foreground=self.widget_fg)
        self._reset_map.configure(background=self.widget_bg, foreground=self.widget_fg)
        self._next_group.configure(background=self.widget_bg, foreground=self.widget_fg)
        element: Label
        for element in self._result_frame.winfo_children():
            element.configure(background=self.canvas_bg, foreground=self.expression_fg)
        self._error_message.configure(background=self.main_bg)
        self._expression_entry.configure(background=self.widget_bg, foreground=self.widget_fg,
                                         highlightcolor=self.widget_fg, highlightbackground=self.widget_fg)
        self.rescale()

    def toggle_state(self: _App, state: int, button: _ToggleButton = None) -> None:
        """Toggle the any of the states between 0 and 1

            Parameters:
                self (_App):            The instantiated object
                state (int):            The state/setting to change
                button (_ToggleButton): The button that holds the data of which state it is

            Returns:
                Nothing (None): Null
        """
        if button is None or not bool(button.get_state()):
            self.states[state] = 0
        else:
            self.states[state] = 1

    def solve(self: _App, _: Optional[Event] = None) -> None:
        """Solve the map from the expression that has been entered

            Parameters:
                self (_App):         The instantiated object
                _ (Optional[Event]): The event data passed by bind function (Unused)

            Returns:
                Nothing (None): Null
        """
        # cancel the automatic group change
        if self._job is not None:
            self.master.after_cancel(self._job)
            self._job = None
        # clear error widget
        self._error_message.config(text="")
        self._error_message.pack_forget()
        self.kmap = KarnaughMap(raise_error=True, debug=False)
        if len(self._expression_entry.get()) != 0:
            self.reset_table = self._expression_entry.get()  # store expression for if map is modified
            try:
                self.kmap.create_map(expression=self._expression_entry.get())
                self.solution = self.kmap.solve_map()  # solve the map
                # create the solution text as seperate widgets so each group can be highlighted individually
                for element in self._result_frame.winfo_children():
                    element.grid_forget()
                self._result_frame_widgets = []
                self._result_frame_widgets.append(
                    Label(self._result_frame, text=self._expression_entry.get() + "=", padx=0, borderwidth=0,
                          background=self.canvas_bg, foreground=self.expression_fg))
                self._result_frame_widgets[-1].grid(row=0, column=0)
                for index, expression in enumerate(self.solution[1:-1].replace("v(", "").split(")")):
                    self._result_frame_widgets.append(Label(self._result_frame, background=self.canvas_bg,
                                                            borderwidth=0, text="(" + expression + ")",
                                                            foreground=self.expression_fg, padx=0))
                    self._result_frame_widgets[-1].grid(row=0, column=1 + 2 * index)
                    Label(self._result_frame, text="v", padx=0, borderwidth=0, background=self.canvas_bg,
                          foreground=self.expression_fg).grid(row=0, column=2 + 2 * index)
                self._result_frame.winfo_children()[-1].grid_forget()
                self._solve_from_map.pack_forget()
                self._reset_map.pack_forget()
                self.modified = False
                # show necessary buttons and spinbox
                if self.states[1]:
                    self._slider_frame.pack()
                    self._next_group.pack_forget()
                else:
                    if len(self.kmap.groups) > 1:
                        self._next_group.pack()
                    self._slider_frame.pack_forget()
                # copy answerto clipboard
                self.master.clipboard_clear()
                self.master.clipboard_append(self.solution)
                self._error_message.pack()
                self._error_message.config(text="Answer copied to clipboard")
                self.master.after(1500, lambda: (self._error_message.config(text=""),
                                                 self._error_message.pack_forget()))
                self.rescale()  # draw the map
                self._job = self.master.after(200, lambda: self.flash_groups(0))  # show the first group
            except (IndexError, ValueError) as e:
                self._error_message.pack()
                self._error_message.config(text="Invalid Statement!")
                print(e)

    def flash_groups(self: _App, index: int) -> None:
        """Highlight the groups in the map

            Parameters:
                self (_App): The instantiated object
                index (int): The index of the group to highlight

            Returns:
                Nothing (None): Null
        """
        if not self.modified:  # stop displaying groups if the map get modified
            self.cur_group = index
            # redraw the map part on the canvas but with the necessary parts in a different colour
            num_columns = len(self.kmap.table) + 1
            num_rows = len(self.kmap.table[0]) + 1
            width, height = self._canvas.winfo_width(), self._canvas.winfo_height()
            box_size = (height * 0.7) // num_columns if width * (num_rows / num_columns) > height \
                else (width * 0.7) // num_rows
            for column in range(1, num_columns):
                box_y = column * box_size + (height // 2 - (box_size * num_columns // 2))
                for row in range(1, num_rows):
                    box_x = row * box_size + (width // 2 - (box_size * num_rows // 2))
                    if len(self.kmap.groups) != 0:
                        if [row - 1, column - 1] in self.kmap.groups[index % len(self.kmap.groups)]:
                            colour = self.highlight_bg
                        else:
                            colour = self.widget_bg
                    else:
                        colour = self.widget_bg
                    self._canvas.create_rectangle(box_x, box_y, box_x + box_size, box_y + box_size, fill=colour,
                                                  outline=self.widget_fg)
                    self._canvas.create_text(box_x + box_size // 2, box_y + box_size // 2,
                                             text=self.kmap.table[column - 1][row - 1],
                                             fill=self.widget_fg, font="Times {} bold".format(self.font_size))
            # change the colour of the corresponding part of the solution text widget
            for position, expression_label in enumerate(self._result_frame_widgets):
                if len(self.kmap.groups) != 0:
                    if position == index % len(self.kmap.groups) + 1:
                        expression_label.configure(fg=self.highlight_bg)
                    else:
                        expression_label.configure(fg=self.expression_fg)
                else:
                    expression_label.configure(fg=self.expression_fg)
            self._canvas.update()
            # if auto group change is on schedule the next time that this function is called based of the speed spinbox
            if self.states[1]:
                # validate the speed first
                try:
                    speed = int(self._slider.get())
                except ValueError:
                    self._slider.delete(0, "end")
                    self._slider.insert(0, "5")
                    speed = 5
                speed = 10 if speed > 10 else speed
                speed = 1 if speed < 1 else speed
                speed = 11 - speed
                self._job = self.master.after(200 + 200 * speed, lambda: self.flash_groups(self.cur_group + 1))
        else:  # if someone has modified the map reset all the colours
            element: Label
            for element in self._result_frame.winfo_children():
                element.configure(background=self.canvas_bg, foreground=self.expression_fg)
            self.rescale()
            self._job = None

    def change_map(self: _App, event: Event) -> None:
        """Change the data shown in the map when it is clicked

            Parameters:
                self (_App):   The instantiated object
                event (Event): The event data passed by bind function

            Returns:
                Nothing (None): Null
        """
        if self.states[2]:  # if modify map is enabled
            if len(self.kmap.table) > 0:  # if there is a table
                click_x, click_y = event.x, event.y  # get the x and y co-ordinates of the user click on the canvas
                num_columns = len(self.kmap.table) + 1
                num_rows = len(self.kmap.table[0]) + 1
                width, height = self._canvas.winfo_width(), self._canvas.winfo_height()
                box_size = (height * 0.7) // num_columns if width * (num_rows / num_columns) > height \
                    else (width * 0.7) // num_rows
                # calculate the box that the user has clicked on
                row = int((click_x - (width // 2 - (box_size * num_rows // 2))) // box_size)
                column = int((click_y - (height // 2 - (box_size * num_columns // 2))) // box_size)
                # if the user has clicked on an actual square
                if 1 <= row <= num_rows - 1 and 1 <= column <= num_columns - 1:
                    # if the map has not yet been modified show the _solve_from_map and _reset_map buttons
                    if not self.modified:
                        self._solve_from_map.pack()
                        self._reset_map.pack()
                        self.modified = True
                    # change the value in the table in the KarnaughMap object
                    self.kmap.table[column - 1][row - 1] = int(not self.kmap.table[column - 1][row - 1])
                    # redraw the screen and reset colours
                    element: Label
                    for element in self._result_frame.winfo_children():
                        element.configure(background=self.canvas_bg, foreground=self.expression_fg)
                    self.rescale()
                    self._next_group.pack_forget()
                    self._slider_frame.pack_forget()

    def solve_from_mod_map(self: _App) -> None:
        """Solve the map from the modified map rather than the expression

            Parameters:
                self (_App): The instantiated object

            Returns:
                Nothing (None): Null
        """
        if self._job is not None:
            self.master.after_cancel(self._job)
            self._job = None
        self._error_message.config(text="")
        self._error_message.pack_forget()
        try:
            self.solution = self.kmap.solve_map()
            self.reset_table = self.solution
            for element in self._result_frame.winfo_children():
                element.grid_forget()
            self._result_frame_widgets = []
            self._result_frame_widgets.append(
                Label(self._result_frame, text="Solution: ", padx=0, borderwidth=0,
                      background=self.canvas_bg, foreground=self.expression_fg))
            self._result_frame_widgets[-1].grid(row=0, column=0)
            for index, expression in enumerate(self.solution[1:-1].replace("v(", "").split(")")):
                self._result_frame_widgets.append(Label(self._result_frame, background=self.canvas_bg, borderwidth=0,
                                                        text="(" + expression + ")", foreground=self.expression_fg,
                                                        padx=0))
                self._result_frame_widgets[-1].grid(row=0, column=1 + 2 * index)
                Label(self._result_frame, text="v", padx=0, borderwidth=0, background=self.canvas_bg,
                      foreground=self.expression_fg).grid(row=0, column=2 + 2 * index)
            self._result_frame.winfo_children()[-1].grid_forget()
            self._solve_from_map.pack_forget()
            self._reset_map.pack_forget()
            self.modified = False
            if self.states[1]:
                self._slider_frame.pack()
                self._next_group.pack_forget()
            else:
                self._next_group.pack()
                self._slider_frame.pack_forget()
            self.master.clipboard_clear()
            self.master.clipboard_append(self.solution)
            self._error_message.pack()
            self._error_message.config(text="Answer copied to clipboard")
            self.master.after(1500, lambda: (self._error_message.config(text=""), self._error_message.pack_forget()))
            self.rescale()
            self._job = self.master.after(200, lambda: self.flash_groups(0))
        except IndexError as e:
            self._error_message.pack()
            self._error_message.config(text="Invalid Statement!")
            print(e)

    def reset_old_map(self: _App) -> None:
        """Reset the map to its old state before modification

            Parameters:
                self (_App): The instantiated object

            Returns:
                Nothing (None): Null
        """
        self._expression_entry.delete(0, "end")
        self._expression_entry.insert(0, self.reset_table)
        self.solve()


if __name__ == "__main__":
    WindowManager.start_GUI()
