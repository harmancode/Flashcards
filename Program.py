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

import sys
import os

import tkinter as tk
import tkinter.ttk
import tkinter.filedialog

from ManageFlashcardsFrame import ManageFlashcardsFrame
# from Flashcard import Flashcard
# from Deck import Deck
from StudyFrame import StudyFrame
from ManageDecksFrame import ManageDecksFrame
from DatabaseManager import DatabaseManager
from ImportExportManager import ImportExportManager

# from tkinter.filedialog import askopenfilename
# from tkinter.messagebox import showerror


# Inherit from top level widget class (Tk) of tkinter module (tk)
# For additional information:
#   https://stackoverflow.com/questions/34301300/tkinter-understanding-how-to-switch-frames
#   https://stackoverflow.com/questions/7546050/switch-between-two-frames-in-tkinter/7557028#7557028
#   https://stackoverflow.com/questions/48122796/tkinter-creating-multiple-frames-inside-a-frame-class


class Program(tk.Tk):
    WINDOW_WIDTH = 510
    WINDOW_HEIGHT = 442
    STUDYFRAME = "StudyFrame"
    DECKSFRAME = "ManageDecksFrame"
    FLASHCARDSFRAME = "ManageFlashcardsFrame"

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # self.geometry(str(self.WINDOW_HEIGHT) + "x" + str(self.WINDOW_WIDTH))

        # self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        # This will be used all db operations.
        self.database_manager = DatabaseManager()

        self.import_export_manager = ImportExportManager(self.database_manager)

        # # Create the main window widget
        # self.window_name = self.winfo_parent()
        # print("self.window_name: ", self.window_name)
        # self.window = tk.Widget._nametowidget(self, name=self.window_name)

        # Set the app icon
        # Used https://www.favicon-generator.org/
        # To solve a bug, add r to this string. See: https://stackoverflow.com/q/55890931/3780985
        # The r prefix specifies it as a raw string.
        icon_path = self.resource_path(r"icon\favicon.ico")
        # print("icon_path: ", icon_path)
        self.iconbitmap(self, icon_path)

        # Set title of the main window
        self.title("Flashcards")

        # Disable resize on main window
        self.resizable(False, False)
        # self.maxsize(Program.WINDOW_HEIGHT, Program.WINDOW_WIDTH)
        # self.minsize(Program.WINDOW_HEIGHT, Program.WINDOW_WIDTH)

        # Create menu bar
        self.menu_bar = tk.Menu(self)
        self.config(menu=self.menu_bar)

        # Create Decks menu
        self.decks_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Menu", menu=self.decks_menu)
        self.decks_menu.add_command(label="Decks...", command=self.show_manage_decks_frame)
        self.decks_menu.add_command(label="Flashcards...", command=self.show_manage_flashcards_frame)
        self.decks_menu.add_separator()
        self.decks_menu.add_command(label="Import deck as CSV file...", command=self.import_deck_as_csv)
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
        for frame in (StudyFrame, ManageDecksFrame, ManageFlashcardsFrame):
            frame_name = frame.__name__
            print("A new frame is being created; frame_name is", frame_name)

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

        self.center_window()

        self.show_manage_decks_frame()

        # Enter the tkinter main loop
        # self.mainloop()

    # Necessary to use data files with pyinstaller in onefile mode.
    # https://stackoverflow.com/a/44352931/3780985
    # https://stackoverflow.com/a/44438174/3780985
    def resource_path(self, relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base_path, relative_path)

        return os.path.join(base_path, relative_path)

    def open_deck(self, index):
        try:
            deck = self.database_manager.decks[index]
            if deck is not None:
                deck.set_due_flashcards(self.database_manager)
                count = len(deck.flashcards)
                due_count = len(deck.due_flashcards)
                if count > 0:
                    if due_count > 0:
                        self.database_manager.load_deck(index)
                        self.show_study_frame(show_only_due_flashcards=True)
                        self.frames[Program.STUDYFRAME].start_study_session()
                    else:
                        confirmation = tk.messagebox.askokcancel("No due flashcard",
                                                                 "There is no due flashcard. Would you like to go over all of them?",
                                                                 icon="question")
                        if confirmation:
                            self.database_manager.load_deck(index)
                            self.show_study_frame(show_only_due_flashcards=False)
                            self.frames[Program.STUDYFRAME].start_study_session()
                else:
                    tk.messagebox.showwarning("Info",
                                              "This deck is empty. Please add some flashcards to it first by clicking Flashcards button below.")
            else:
                tk.messagebox.showwarning("Info", "You should create a deck first.")
        except Exception as error:
            print("Exception in open deck: ", error)

    def show_study_frame(self, show_only_due_flashcards=True):
        deck = self.database_manager.deck
        frame = self.frames[Program.STUDYFRAME]
        if isinstance(frame, StudyFrame):
            try:
                if hasattr(deck, "flashcards"):
                    if len(deck.flashcards) > 0:
                        frame.prepare_view(show_only_due_flashcards=show_only_due_flashcards)
                        frame.tkraise()
                    else:
                        tk.messagebox.showwarning("Info", "You should add some flashcards first.", icon="info")
            except AttributeError:
                tk.messagebox.showwarning("Info", "You should create a deck first.")

    def show_manage_decks_frame(self):
        deck = self.database_manager.deck
        frame = self.frames[Program.DECKSFRAME]
        if isinstance(frame, ManageDecksFrame):
            frame.prepare_view()
            frame.tkraise()
            if deck is None:
                tk.messagebox.showwarning("Info", """
                Welcome to Flashcards!

                You can create decks of flashcards, and study them later to improve your knowledge and long-time memory.

                Click on the "New deck" button below to start.
                """, icon='info')

    def show_manage_flashcards_frame(self):
        deck = self.database_manager.deck
        frame = self.frames[Program.FLASHCARDSFRAME]
        if isinstance(frame, ManageFlashcardsFrame):
            try:
                if hasattr(deck, "flashcards"):
                    frame.load_deck()
                    frame.prepare_view()
                    frame.tkraise()
                else:
                    tk.messagebox.showwarning("Info", "You should add some flashcards first.", icon="info")
            except Exception as error:
                print("Exception: ", error)

    # def show_frame(self, frame_name):
    #     # Show a frame for the given page name
    #     deck = self.database_manager.deck
    #     frame = self.frames[frame_name]
    #     # frame_name = frame.__class__.__name__
    #     # print("show_frame will load the frame: ", frame_name)
    #
    #     if isinstance(frame, StudyFrame):
    #         try:
    #             if hasattr(deck, "flashcards"):
    #                 if len(deck.flashcards) > 0:
    #                     self.prepare_and_raise_frame(frame)
    #                 else:
    #                     tk.messagebox.showwarning("Info", "You should add some flashcards first.", icon="info")
    #         except AttributeError:
    #             tk.messagebox.showwarning("Info", "You should create a deck first.")
    #
    #     elif isinstance(frame, ManageFlashcardsFrame):
    #         try:
    #             if hasattr(deck, "flashcards"):
    #                 self.prepare_and_raise_frame(frame)
    #             else:
    #                 tk.messagebox.showwarning("Info", "You should add some flashcards first.", icon="info")
    #         except Exception as error:
    #             print("Exception: ", error)
    #
    #     elif isinstance(frame, ManageDecksFrame):
    #         self.prepare_and_raise_frame(frame)
    #         if deck is None:
    #             tk.messagebox.showwarning("Info", """
    #                 Welcome to Flashcards!
    #
    #                 You can create decks of flashcards, and study them later to improve your knowledge and long-time memory.
    #
    #                 Click on the "New deck" button below to start.
    #                 """, icon='info')

    def center_window(self):
        # self.window.update()

        # print(self.window.winfo_width())
        # print(self.window.winfo_height())
        #
        # print(self.window.winfo_reqwidth())
        # print(self.window.winfo_reqheight())

        # window_width = 483
        # window_height = 370

        window_width = Program.WINDOW_WIDTH
        window_height = Program.WINDOW_HEIGHT

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

    def show_about_box(self):
        message_text = """
        Flashcards v0.1
        
        Copyright 2020 Ertugrul Harman
        E-mail: dev@harman.page
        Twitter: twitter.com/harmancode
        
        Flashcards is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
        
        This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. 
        
        See the GNU General Public License for more details. You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>.
        """
        tk.messagebox.showinfo(title="About Flashcards", message=message_text)

    def import_deck_as_csv(self):
        filename = tkinter.filedialog.askopenfilename(filetypes=(("CSV files", "*.csv"),
                                                                 ("All files", "*.*")))
        if filename:
            try:
                print("filename: ", filename)
                result = self.import_export_manager.importfile(filename)
                if result:
                    self.frames["ManageDecksFrame"].prepare_view()
                    tk.messagebox.showwarning("Info", "Import successful.", icon="info")
                else:
                    tk.messagebox.showwarning("Info", "Import failed.")
            except:  # <- naked except is a bad idea
                tk.messagebox.showerror("Open Source File", "Failed to read file\n'%s'" % filename)
            return
