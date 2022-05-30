"""Create a GUI to solve and manipulate Karnaugh Maps.

Classes:

    Public:
        App
    Private:
        _ToggleButton
        _SettingsApp
        _CreditsApp
        _HelpApp

Functions:

    App.

Misc variables:

    __all__
    __author__
    __version__
    supported_from
"""

__all__ = ["App"]
__author__ = "Alexander Bisland"
__version__ = "3.3.2"
supported_from = "3.8.1"

from tkinter import Tk, Button, Canvas, PhotoImage, Label, Frame, Entry, Spinbox, Misc, Event
from typing import TypeVar, Optional, Callable
from src.KMap import KarnaughMap
import os
import configparser

_App = TypeVar("_App", bound="App")
_ToggleButtonVar = TypeVar("_ToggleButtonVar", bound="_ToggleButton")
_SettingsAppVar = TypeVar("_SettingsAppVar", bound="_SettingsApp")
_CreditsAppVar = TypeVar("_CreditsAppVar", bound="_CreditsApp")
_HelpAppVar = TypeVar("_HelpAppVar", bound="_HelpApp")


class _ToggleButton(Canvas):
    def __init__(self: _ToggleButtonVar, master: Optional[Misc], command: Optional[Callable] = None,
                 file0: str = "night.gif", file1: str = "day.gif", default: int = 0, *args, **kwargs) -> None:
        super().__init__(master, *args, **kwargs)
        self.master = master

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
        curent_img = self._night
        if self.state:
            curent_img = self._day
        self._button.config(image=curent_img)
        self.state = int(not self.state)

    def get_state(self: _ToggleButtonVar) -> int:
        return self.state


class WindowManager:
    @staticmethod
    def open_credits() -> None:
        credits_window = Tk()
        _CreditsApp(credits_window)
        credits_window.mainloop()

    @staticmethod
    def open_help() -> None:
        help_window = Tk()
        _HelpApp(help_window)
        help_window.mainloop()

    @staticmethod
    def open_settings(window: _App) -> None:
        settings_window = Tk()
        _SettingsApp(settings_window, window)
        settings_window.mainloop()

    @staticmethod
    def start_GUI() -> None:
        root = Tk()
        App(root)
        root.mainloop()


class _CreditsApp:
    def __init__(self: _CreditsAppVar, master: Tk) -> None:
        master.title("Credits")
        master.geometry("250x50")
        master.resizable(width=False, height=False)
        master.lift()
        master.focus_force()

        Label(master, text="Credits:\nThis utility is created by Alexander Bisland\n"
                           "Copyrighted BizTecBritain All rights reserved").pack()


class _HelpApp:
    def __init__(self: _HelpAppVar, master: Tk) -> None:
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
    def __init__(self: _SettingsAppVar, master: Tk, main_app: _App) -> None:
        self.master = master
        self.master.title("Settings")
        self.master.geometry("250x150")
        self.master.resizable(width=False, height=False)
        self.master.lift()
        self.master.focus_force()
        self.main_app = main_app
        self.config = configparser.ConfigParser()
        if os.path.exists(os.getenv('LOCALAPPDATA') + '\\KMap\\GUI.ini'):
            self.config.read(os.getenv('LOCALAPPDATA') + '\\KMap\\GUI.ini')
        if not os.path.exists(os.getenv('LOCALAPPDATA') + '\\KMap'):
            os.mkdir(os.getenv('LOCALAPPDATA') + '\\KMap')
        self.master.protocol("WM_DELETE_WINDOW", self._save_data)

        self.frame = Frame(self.master)
        self.frame.pack(anchor="nw", padx=3, pady=3)

        self.day_night_btn = _ToggleButton(self.frame, self.toggle_mode, default=main_app.states[0])
        self.day_night_btn.grid(row=0, column=0)
        if main_app.states[0]:
            self.day_night_btn_label = Label(self.frame, text="Dark Mode Enabled")
        else:
            self.day_night_btn_label = Label(self.frame, text="Light Mode Enabled")
        self.day_night_btn_label.grid(row=0, column=1, sticky="w")

        self.auto_groups_btn = _ToggleButton(self.frame, self.toggle_auto, "on.gif", "off.gif", main_app.states[1])
        self.auto_groups_btn.grid(row=1, column=0)
        if main_app.states[1]:
            self.auto_groups_btn_label = Label(self.frame, text="Automatic Group Change")
        else:
            self.auto_groups_btn_label = Label(self.frame, text="Manual Group Change")
        self.auto_groups_btn_label.grid(row=1, column=1, sticky="w")

        self.modify_map_btn = _ToggleButton(self.frame, self.toggle_modify, "on.gif", "off.gif", main_app.states[2])
        self.modify_map_btn.grid(row=2, column=0)
        if main_app.states[2]:
            self.modify_map_btn_label = Label(self.frame, text="Modify Map Enabled")
        else:
            self.modify_map_btn_label = Label(self.frame, text="Modify Map Disabled")
        self.modify_map_btn_label.grid(row=2, column=1, sticky="w")

        self.credits = Button(self.master, text="Credits", command=WindowManager.open_credits)
        self.credits.pack(pady=3)
        self.close = Button(self.master, text="Close Window", command=self._save_data)
        self.close.pack(pady=3)

        self.toggle_mode(init=True)

    def _save_data(self: _SettingsAppVar) -> None:
        with open(os.getenv('LOCALAPPDATA') + '\\KMap\\GUI.ini', 'w') as configfile:
            self.config['SETTINGS'] = {'Mode': self.main_app.states[0],
                                       'Auto': self.main_app.states[1],
                                       'Modify': self.main_app.states[2]}
            self.config.write(configfile)
        self.master.destroy()

    def toggle_mode(self: _SettingsAppVar, _: Optional[Event] = None, init: bool = False) -> None:
        if not init:
            self.main_app.toggle_mode(self.day_night_btn)
        if self.main_app.states[0]:
            self.day_night_btn_label.configure(text="Dark Mode Enabled")
            self.master.configure(bg="#121212")
            self.frame.configure(bg="#121212")
            self.day_night_btn_label.configure(fg="white", bg="#121212")
            self.auto_groups_btn_label.configure(fg="white", bg="#121212")
            self.modify_map_btn_label.configure(fg="white", bg="#121212")
            self.auto_groups_btn.grid_forget()
            self.auto_groups_btn = _ToggleButton(self.frame, self.toggle_auto, "ondark.png", "offdark.png",
                                                 self.main_app.states[1])
            self.auto_groups_btn.grid(row=1, column=0)
            self.modify_map_btn.grid_forget()
            self.modify_map_btn = _ToggleButton(self.frame, self.toggle_modify, "ondark.png", "offdark.png",
                                                self.main_app.states[2])
            self.modify_map_btn.grid(row=2, column=0)
            self.credits.configure(bg="purple", fg="white")
            self.close.configure(bg="purple", fg="white")
        else:
            self.day_night_btn_label.configure(text="Light Mode Enabled")
            self.master.configure(bg="SystemButtonFace")
            self.frame.configure(bg="SystemButtonFace")
            self.day_night_btn_label.configure(fg="black", bg="SystemButtonFace")
            self.auto_groups_btn_label.configure(fg="black", bg="SystemButtonFace")
            self.modify_map_btn_label.configure(fg="black", bg="SystemButtonFace")
            self.auto_groups_btn.grid_forget()
            self.auto_groups_btn = _ToggleButton(self.frame, self.toggle_auto, "on.gif", "off.gif",
                                                 self.main_app.states[1])
            self.auto_groups_btn.grid(row=1, column=0)
            self.modify_map_btn.grid_forget()
            self.modify_map_btn = _ToggleButton(self.frame, self.toggle_modify, "on.gif", "off.gif",
                                                self.main_app.states[2])
            self.modify_map_btn.grid(row=2, column=0)
            self.credits.configure(bg="lightblue", fg="black")
            self.close.configure(bg="lightblue", fg="black")

    def toggle_auto(self: _SettingsAppVar, _: Optional[Event] = None) -> None:
        self.main_app.toggle_state(1, self.auto_groups_btn)
        if self.main_app.states[1]:
            self.auto_groups_btn_label.configure(text="Automatic Group Change")
        else:
            self.auto_groups_btn_label.configure(text="Manual Group Change")

    def toggle_modify(self: _SettingsAppVar, _: Optional[Event] = None) -> None:
        self.main_app.toggle_state(2, self.modify_map_btn)
        if self.main_app.states[2]:
            self.modify_map_btn_label.configure(text="Modify Map Enabled")
        else:
            self.modify_map_btn_label.configure(text="Modify Map Disabled")


class App:
    def __init__(self: _App, master: Tk) -> None:
        self.kmap = KarnaughMap(raise_error=False, debug=False)
        self.solution = ""
        self.groups = []
        self.states = [0, 0, 0]
        self.colour1 = ""
        self.colour2 = ""
        self.colour3 = ""
        self.colour4 = ""
        self.colour5 = ""
        self.colour6 = ""
        self.font_size = 20
        self.cur_group = 0
        self.modified = False
        self.reset_table = ""
        self._job = None
        self._geom = '640x360+0+0'

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

        self.open_settings = Button(self.master, text="Settings", command=lambda: WindowManager.open_settings(self))
        self.open_settings.place(x=4, y=3)

        self.open_help = Button(self.master, text="Help", command=WindowManager.open_help)
        self.open_help.pack(pady=3, padx=4, anchor="e")

        self.canvas = Canvas(self.master, width=500, height=500, bd=0, highlightthickness=0)
        self.canvas.pack(pady=3)
        self.canvas.bind("<Button-1>", self.change_map)

        self.result_frame = Frame(self.canvas)
        self.result_frame.pack(pady=3)
        self.result_frame_widgets = []

        self.input_frame = Frame(self.master)
        self.input_frame.pack()
        self.expression_entry = Entry(self.input_frame, highlightthickness=2)
        self.expression_entry.grid(column=0, row=0, padx=2)
        self.expression_entry.bind('<Return>', self.solve)
        self.solve_button = Button(self.input_frame, text='Solve', command=self.solve)
        self.solve_button.grid(column=1, row=0, padx=2)
        self.expression_entry.focus_set()

        self.slider_frame = Frame(self.master)
        self.slider = Spinbox(self.slider_frame, from_=1, to=10, width=3)
        self.slider.delete(0, "end")
        self.slider.insert(0, "5")
        self.slider.grid(column=1, row=0)
        self.slider_label = Label(self.slider_frame, text="Speed: ", width=7)
        self.slider_label.grid(column=0, row=0)

        self.next_group = Button(self.master, text="Next Group", command=lambda: self.flash_groups(self.cur_group + 1))

        self.error_message = Label(self.master, fg="red")

        self.solve_from_map = Button(self.master, text="Solve From Map", command=self.solve_from_mod_map)
        self.reset_map = Button(self.master, text="Reset Map", command=self.reset_old_map)

        self.toggle_mode()
        self.master.bind("<Configure>", self.rescale)
        self.rescale()

    def rescale(self: _App, _: Optional[Event] = None) -> None:
        height = self.master.winfo_height()
        width = self.master.winfo_width()
        self.font_size = str((width if width < height else height) // 50)
        self.canvas.configure(width=width * 0.8, height=height * 0.65)
        self.expression_entry.configure(font=(None, int(self.font_size)))
        self.solve_button.configure(font=(None, int(self.font_size)))
        self.next_group.configure(font=(None, int(self.font_size)))
        self.solve_from_map.configure(font=(None, int(self.font_size)))
        self.reset_map.configure(font=(None, int(self.font_size)))
        self.error_message.configure(font=(None, int(self.font_size)))
        self.slider.configure(font=(None, int(self.font_size)))
        self.slider_label.configure(font=(None, int(self.font_size)))
        for element in self.result_frame.winfo_children():
            element.configure(font="Times {} bold".format(int(int(self.font_size) * 1.5)))
        self.rounded_rect(0, 0, int(width * 0.8 - 1), int(height * 0.65 - 1), 15)

    def rounded_rect(self: _App, x: int, y: int, w: int, h: int, c: int, grid: bool = True) -> None:
        self.canvas.delete("all")
        self.canvas.create_arc(x, y, x + 2 * c, y + 2 * c, start=90, extent=90, style="pieslice", fill=self.colour4,
                               outline=self.colour4)
        self.canvas.create_arc(x, y, x + 2 * c, y + 2 * c, start=90, extent=90, style="arc", outline=self.colour1)
        self.canvas.create_arc(x + w - 2 * c, y + h - 2 * c, x + w, y + h, start=270, extent=90, style="pieslice",
                               fill=self.colour4, outline=self.colour4)
        self.canvas.create_arc(x + w - 2 * c, y + h - 2 * c, x + w, y + h, start=270, extent=90, style="arc",
                               outline=self.colour1)
        self.canvas.create_arc(x + w - 2 * c, y, x + w, y + 2 * c, start=0, extent=90, style="pieslice",
                               fill=self.colour4, outline=self.colour4)
        self.canvas.create_arc(x + w - 2 * c, y, x + w, y + 2 * c, start=0, extent=90, style="arc",
                               outline=self.colour1)
        self.canvas.create_arc(x, y + h - 2 * c, x + 2 * c, y + h, start=180, extent=90, style="pieslice",
                               fill=self.colour4, outline=self.colour4)
        self.canvas.create_arc(x, y + h - 2 * c, x + 2 * c, y + h, start=180, extent=90, style="arc",
                               outline=self.colour1)
        self.canvas.create_rectangle(x + c, y, x + w - c, y + h, fill=self.colour4, outline=self.colour4)
        self.canvas.create_rectangle(x, y + c, x + w, y + h - c, fill=self.colour4, outline=self.colour4)
        self.canvas.create_line(x + c, y, x + w - c, y, fill=self.colour1)
        self.canvas.create_line(x + c, y + h, x + w - c, y + h, fill=self.colour1)
        self.canvas.create_line(x, y + c, x, y + h - c, fill=self.colour1)
        self.canvas.create_line(x + w, y + c, x + w, y + h - c, fill=self.colour1)
        if grid:
            try:
                num_columns = len(self.kmap.table) + 1
                num_rows = len(self.kmap.table[0]) + 1
                width, height = self.canvas.winfo_width(), self.canvas.winfo_height()
                box_size = (height * 0.7) // num_columns if width * (num_rows / num_columns) > height \
                    else (width * 0.7) // num_rows
                for column in range(1, num_columns):
                    box_y = column * box_size + (height // 2 - (box_size * num_columns // 2))
                    for row in range(1, num_rows):
                        box_x = row * box_size + (width // 2 - (box_size * num_rows // 2))
                        self.canvas.create_rectangle(box_x, box_y, box_x + box_size, box_y + box_size,
                                                     fill=self.colour3, outline=self.colour1)
                        self.canvas.create_text(box_x + box_size // 2, box_y + box_size // 2, fill=self.colour1,
                                                text=self.kmap.table[column - 1][row - 1],
                                                font="Times {} bold".format(self.font_size))
                headings = KarnaughMap.VALUES[self.kmap.tot_input]
                for index, heading in enumerate(headings[0]):
                    box_y = height // 2 - (box_size * num_columns // 2)
                    box_x = (index + 1) * box_size + (width // 2 - (box_size * num_rows // 2))
                    self.canvas.create_text(box_x + box_size // 2, box_y + box_size // 2, text=heading,
                                            fill=self.colour1, font="Times {} bold".format(self.font_size))
                for index, heading in enumerate(headings[1]):
                    box_y = (index + 1) * box_size + (height // 2 - (box_size * num_columns // 2))
                    box_x = width // 2 - (box_size * num_rows // 2)
                    self.canvas.create_text(box_x + box_size // 2, box_y + box_size // 2, text=heading,
                                            fill=self.colour1, font="Times {} bold".format(self.font_size))
                rows = "".join(KarnaughMap.LETTERS[:len(KarnaughMap.VALUES[self.kmap.tot_input][0][0])])
                columns = "".join(KarnaughMap.LETTERS[len(KarnaughMap.VALUES[self.kmap.tot_input][0][0]):
                                                      len(KarnaughMap.VALUES[self.kmap.tot_input][0][0]) +
                                                      len(KarnaughMap.VALUES[self.kmap.tot_input][1][0])])
                letters_y = height // 2 - (box_size * num_columns // 2)
                letters_x = width // 2 - (box_size * num_rows // 2)
                self.canvas.create_text(letters_x + (3 * box_size) // 4, letters_y + box_size // 2, text=rows.upper(),
                                        fill=self.colour1, font="Times {} bold".format(self.font_size))
                self.canvas.create_text(letters_x + box_size // 2, letters_y + (3 * box_size) // 4, fill=self.colour1,
                                        text=columns.upper(), font="Times {} bold".format(self.font_size))

            except (ZeroDivisionError, IndexError):
                self.rounded_rect(x, y, w, h, c, False)

    def toggle_geom(self: _App, _: Optional[Event] = None) -> None:
        if self.master.state() == 'zoomed':
            self.master.state('normal')
            self.master.geometry(self._geom)
        else:
            self.master.state('zoomed')

    def toggle_fullscreen(self: _App, _: Optional[Event] = None) -> None:
        if self.master.attributes()[self.master.attributes().index('-fullscreen') + 1]:
            self.master.attributes('-fullscreen', False)
        else:
            self.master.attributes('-fullscreen', True)

    def toggle_mode(self: _App, button: _ToggleButton = None) -> None:
        if button is None and self.states[0] == 1:
            self.colour1 = "white"
            self.colour2 = "#121212"
            self.colour3 = "purple"
            self.colour4 = "#343434"
            self.colour5 = "magenta"
            self.colour6 = "#03DAC6"
            self.states[0] = 1
        elif button is None or not bool(button.get_state()):
            self.colour1 = "black"
            self.colour2 = "SystemButtonFace"
            self.colour3 = "lightblue"
            self.colour4 = "white"
            self.colour5 = "darkblue"
            self.colour6 = "#A34C00"  # "#653594"
            self.states[0] = 0
        else:
            self.colour1 = "white"
            self.colour2 = "#121212"
            self.colour3 = "purple"
            self.colour4 = "#343434"
            self.colour5 = "magenta"
            self.colour6 = "#03DAC6"
            self.states[0] = 1
        self.master.configure(bg=self.colour2)
        self.canvas.configure(background=self.colour2)
        self.input_frame.configure(background=self.colour2)
        self.slider_frame.configure(background=self.colour2)
        self.slider_label.configure(background=self.colour2, foreground=self.colour1)
        self.solve_button.configure(background=self.colour3, foreground=self.colour1)
        self.solve_from_map.configure(background=self.colour3, foreground=self.colour1)
        self.reset_map.configure(background=self.colour3, foreground=self.colour1)
        self.next_group.configure(background=self.colour3, foreground=self.colour1)
        for element in self.result_frame.winfo_children():
            element.configure(background=self.colour4, foreground=self.colour5)
        self.error_message.configure(background=self.colour2)
        self.expression_entry.configure(background=self.colour3, foreground=self.colour1, highlightcolor=self.colour1,
                                        highlightbackground=self.colour1)
        self.rescale()

    def toggle_state(self: _App, state: int, button: _ToggleButton = None) -> None:
        if button is None or not bool(button.get_state()):
            self.states[state] = 0
        else:
            self.states[state] = 1

    def solve(self: _App, _: Optional[Event] = None) -> None:
        if self._job is not None:
            self.master.after_cancel(self._job)
            self._job = None
        self.error_message.config(text="")
        self.error_message.pack_forget()
        self.kmap = KarnaughMap(raise_error=False, debug=False)
        if len(self.expression_entry.get()) != 0:
            self.reset_table = self.expression_entry.get()
            self.kmap.create_map(expression=self.expression_entry.get())
            try:
                self.solution = self.kmap.solve_map()
                for element in self.result_frame.winfo_children():
                    element.grid_forget()
                self.result_frame_widgets = []
                self.result_frame_widgets.append(
                    Label(self.result_frame, text=self.expression_entry.get() + "=", padx=0, borderwidth=0,
                          background=self.colour4, foreground=self.colour5))
                self.result_frame_widgets[-1].grid(row=0, column=0)
                for index, expression in enumerate(self.solution[1:-1].replace("v(", "").split(")")):
                    self.result_frame_widgets.append(Label(self.result_frame, background=self.colour4, borderwidth=0,
                                                           text="(" + expression + ")", foreground=self.colour5,
                                                           padx=0))
                    self.result_frame_widgets[-1].grid(row=0, column=1 + 2 * index)
                    Label(self.result_frame, text="v", padx=0, borderwidth=0, background=self.colour4,
                          foreground=self.colour5).grid(row=0, column=2 + 2 * index)
                self.result_frame.winfo_children()[-1].grid_forget()
                self.solve_from_map.pack_forget()
                self.reset_map.pack_forget()
                self.modified = False
                if self.states[1]:
                    self.slider_frame.pack()
                    self.next_group.pack_forget()
                else:
                    self.next_group.pack()
                    self.slider_frame.pack_forget()
                self.master.clipboard_clear()
                self.master.clipboard_append(self.solution)
                self.error_message.pack()
                self.error_message.config(text="Answer copied to clipboard")
                self.master.after(1500, lambda: (self.error_message.config(text=""), self.error_message.pack_forget()))
                self.rescale()
                self._job = self.master.after(200, lambda: self.flash_groups(0))
            except IndexError as e:
                self.error_message.pack()
                self.error_message.config(text="Invalid Statement!")
                print(e)

    def flash_groups(self: _App, index: int) -> None:
        if not self.modified:
            self.cur_group = index
            num_columns = len(self.kmap.table) + 1
            num_rows = len(self.kmap.table[0]) + 1
            width, height = self.canvas.winfo_width(), self.canvas.winfo_height()
            box_size = (height * 0.7) // num_columns if width * (num_rows / num_columns) > height \
                else (width * 0.7) // num_rows
            for column in range(1, num_columns):
                box_y = column * box_size + (height // 2 - (box_size * num_columns // 2))
                for row in range(1, num_rows):
                    box_x = row * box_size + (width // 2 - (box_size * num_rows // 2))
                    if len(self.kmap.groups) != 0:
                        if [row - 1, column - 1] in self.kmap.groups[index % len(self.kmap.groups)]:
                            colour = self.colour6
                        else:
                            colour = self.colour3
                    else:
                        colour = self.colour3
                    self.canvas.create_rectangle(box_x, box_y, box_x + box_size, box_y + box_size, fill=colour,
                                                 outline=self.colour1)
                    self.canvas.create_text(box_x + box_size // 2, box_y + box_size // 2,
                                            text=self.kmap.table[column - 1][row - 1],
                                            fill=self.colour1, font="Times {} bold".format(self.font_size))
            for position, expression_label in enumerate(self.result_frame_widgets):
                if len(self.kmap.groups) != 0:
                    if position == index % len(self.kmap.groups) + 1:
                        expression_label.configure(fg=self.colour6)
                    else:
                        expression_label.configure(fg=self.colour5)
                else:
                    expression_label.configure(fg=self.colour5)
            self.canvas.update()
            if self.states[1]:
                try:
                    speed = int(self.slider.get())
                except ValueError:
                    self.slider.delete(0, "end")
                    self.slider.insert(0, "5")
                    speed = 5
                speed = 10 if speed > 10 else speed
                speed = 1 if speed < 1 else speed
                speed = 11 - speed
                self._job = self.master.after(200 + 200 * speed, lambda: self.flash_groups(self.cur_group + 1))
        else:
            for element in self.result_frame.winfo_children():
                element.configure(background=self.colour4, foreground=self.colour5)
            self.rescale()
            self._job = None

    def change_map(self: _App, event: Event) -> None:
        if self.states[2]:
            if len(self.kmap.table) > 0:
                click_x, click_y = event.x, event.y
                num_columns = len(self.kmap.table) + 1
                num_rows = len(self.kmap.table[0]) + 1
                width, height = self.canvas.winfo_width(), self.canvas.winfo_height()
                box_size = (height * 0.7) // num_columns if width * (num_rows / num_columns) > height \
                    else (width * 0.7) // num_rows
                row = int((click_x - (width // 2 - (box_size * num_rows // 2))) // box_size)
                column = int((click_y - (height // 2 - (box_size * num_columns // 2))) // box_size)
                if 1 <= row <= num_rows - 1 and 1 <= column <= num_columns - 1:
                    if not self.modified:
                        self.solve_from_map.pack()
                        self.reset_map.pack()
                        self.modified = True
                    self.kmap.table[column - 1][row - 1] = int(not self.kmap.table[column - 1][row - 1])
                    for element in self.result_frame.winfo_children():
                        element.configure(background=self.colour4, foreground=self.colour5)
                    self.rescale()
                    self.next_group.pack_forget()
                    self.slider_frame.pack_forget()

    def solve_from_mod_map(self: _App) -> None:
        if self._job is not None:
            self.master.after_cancel(self._job)
            self._job = None
        self.error_message.config(text="")
        self.error_message.pack_forget()
        try:
            self.solution = self.kmap.solve_map()
            self.reset_table = self.solution
            for element in self.result_frame.winfo_children():
                element.grid_forget()
            self.result_frame_widgets = []
            self.result_frame_widgets.append(
                Label(self.result_frame, text="Solution: ", padx=0, borderwidth=0,
                      background=self.colour4, foreground=self.colour5))
            self.result_frame_widgets[-1].grid(row=0, column=0)
            for index, expression in enumerate(self.solution[1:-1].replace("v(", "").split(")")):
                self.result_frame_widgets.append(Label(self.result_frame, background=self.colour4, borderwidth=0,
                                                       text="(" + expression + ")", foreground=self.colour5,
                                                       padx=0))
                self.result_frame_widgets[-1].grid(row=0, column=1 + 2 * index)
                Label(self.result_frame, text="v", padx=0, borderwidth=0, background=self.colour4,
                      foreground=self.colour5).grid(row=0, column=2 + 2 * index)
            self.result_frame.winfo_children()[-1].grid_forget()
            self.solve_from_map.pack_forget()
            self.reset_map.pack_forget()
            self.modified = False
            if self.states[1]:
                self.slider_frame.pack()
                self.next_group.pack_forget()
            else:
                self.next_group.pack()
                self.slider_frame.pack_forget()
            self.master.clipboard_clear()
            self.master.clipboard_append(self.solution)
            self.error_message.pack()
            self.error_message.config(text="Answer copied to clipboard")
            self.master.after(1500, lambda: (self.error_message.config(text=""), self.error_message.pack_forget()))
            self.rescale()
            self._job = self.master.after(200, lambda: self.flash_groups(0))
        except IndexError as e:
            self.error_message.pack()
            self.error_message.config(text="Invalid Statement!")
            print(e)

    def reset_old_map(self: _App) -> None:
        self.expression_entry.delete(0, "end")
        self.expression_entry.insert(0, self.reset_table)
        self.solve()


if __name__ == "__main__":
    WindowManager.start_GUI()
