#   Program FlashCards
#
#   Copyright 2020 Ertugrul Harman
#
#   Website     : harman.page
#   Email (1)   : dev@harman.page
#   Email (2)   : ertugrulharman@gmail.com
#
#   This file is part of Flashcards.
#
#   Flashcards is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <https://www.gnu.org/licenses/>.

import tkinter as tk
from tkinter import font as tkfont
import tkinter.ttk
from Flashcard import Flashcard
from Deck import Deck
from StudyFrame import StudyFrame
from EditFrame import EditFrame


# Inherit from top level widget class (Tk) of tkinter module (tk)
# For additional information:
#   https://stackoverflow.com/questions/34301300/tkinter-understanding-how-to-switch-frames
#   https://stackoverflow.com/questions/7546050/switch-between-two-frames-in-tkinter/7557028#7557028
#   https://stackoverflow.com/questions/48122796/tkinter-creating-multiple-frames-inside-a-frame-class
class Program(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # self.WINDOW_HEIGHT = 483
        # self.WINDOW_WIDTH = 420

        # self.geometry(str(self.WINDOW_HEIGHT) + "x" + str(self.WINDOW_WIDTH))

        # self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        self.decks = self.create_dummy_deck()

        # self.deck : Deck = self.decks[0]

        # # Create the main window widget
        # self.window_name = self.winfo_parent()
        # print("self.window_name: ", self.window_name)
        # self.window = tk.Widget._nametowidget(self, name=self.window_name)

        # Set the app icon
        # Used https://www.favicon-generator.org/
        self.iconbitmap("ico/favicon.ico")

        # Set title of the main window
        self.title("Flashcards")

        # Disable resize on main window
        self.resizable(False, False)

        # Create menu bar
        self.menu_bar = tk.Menu(self)
        self.config(menu=self.menu_bar)

        # Create Decks menu
        self.decks_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Deck", menu=self.decks_menu)
        self.decks_menu.add_command(label="Manage decks...", command=self.edit_deck)
        self.decks_menu.add_separator()
        self.decks_menu.add_command(label="Quit", command=self.quit)

        # # Create Flashcard menu
        # flashcard_menu = tk.Menu(self.menu_bar, tearoff=0)
        # self.menu_bar.add_cascade(label="Flashcard", menu=flashcard_menu)
        # flashcard_menu.add_command(label="Add new flashcard...", command=self.open_deck)
        # flashcard_menu.add_command(label="Change this question...", command=self.new_deck)
        # flashcard_menu.add_command(label="Change this answer...", command=self.new_deck)
        # flashcard_menu.add_command(label="Remove from deck...", command=self.new_deck)

        # Create About menu
        help_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about_box)

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        # frames dictionary will hold all the Frames that the Program consists of.
        self.frames = dict()

        # Iterate through the "Frame classes", classes that inherits from tk.Frame
        for frame in (StudyFrame, EditFrame):
            frame_name = frame.__name__
            print("frame_name is", frame_name)

            # Initialize child frame with two parameters, parent and controller Parent is the container, an attribute
            # of the Program class, that will contain all frames Controller is the Program class itself. By passing
            # these parameters, child frame will have references to access attributes and methods of the Program class.
            frame = frame(parent=self.container, controller=self)

            # Add the frame that has just been initialized to the dictionary: self.frames
            # So that Program class instance can access those frames later by calling their names
            self.frames[frame_name] = frame

            # Put all the frames to the same location (row and column) so that they will be stacked
            # on top of each other. Only the top Frame will be shown to the user. This is a default behavior in many
            # GUIs. We will only change the top Frame to change the view in the main window.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StudyFrame")

        self.center_window()

        # Enter the tkinter main loop
        # self.mainloop()

    def show_frame(self, frame_name):
        # Show a frame for the given page name
        frame = self.frames[frame_name]
        frame_name = frame.__class__.__name__
        print("show_frame will load the frame: ", frame_name)
        frame.tkraise()

    def create_dummy_deck(self):
        deck = Deck("USA capital cities")
        deck.flashcards = self.create_dummy_flashcards1(deck)
        decks = [deck]
        deck = Deck("Network Ports")
        deck.flashcards = self.create_dummy_flashcards2(deck)
        decks.append(deck)
        return decks

    def create_dummy_flashcards1(self, deck):
        flashcard1 = Flashcard("Capital of Texas?", "Austin", deck)
        flashcard2 = Flashcard("Capital of California?", "Sacramento", deck)
        flashcard3 = Flashcard("Capital of Washington?", "Olympia", deck)
        flashcards = [flashcard1, flashcard2, flashcard3]
        return flashcards

    def create_dummy_flashcards2(self, deck):
        flashcard1 = Flashcard("FTP", "20, 21", deck)
        flashcard2 = Flashcard("SSH", "22", deck)
        flashcard3 = Flashcard("Telnet", "23", deck)
        flashcard4 = Flashcard("SMTP", "25", deck)
        flashcards = [flashcard1, flashcard2, flashcard3, flashcard4]
        return flashcards

    def center_window(self):
        # self.window.update()

        # print(self.window.winfo_width())
        # print(self.window.winfo_height())
        #
        # print(self.window.winfo_reqwidth())
        # print(self.window.winfo_reqheight())

        # window_width = 483
        # window_height = 370

        window_width = 483
        window_height = 420

        print(self.winfo_width())
        print(self.winfo_height())

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        print(screen_width)
        print(screen_height)

        x_cordinate = int((screen_width / 2) - (window_width / 2))
        y_cordinate = int((screen_height / 2) - (window_height / 2))

        # self.window.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))
        self.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))


    def edit_deck(self):
        self.show_frame("EditFrame")

    def show_about_box(self):
        pass

    # def select_deck(self, index):
    #     self.deck = self.decks[index]

    def open_deck(self, index):
        self.frames["StudyFrame"].load_deck(index)
        self.show_frame("StudyFrame")