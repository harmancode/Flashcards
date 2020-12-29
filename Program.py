#   Program FlashCards
#
#   Copyright 2020 Ertugrul Harman
#
#       E-mail  : harmancode@gmail.com
#       Twitter : https://twitter.com/harmancode
#       Web     : https://harman.page
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

# To open PDF file with default application of the operating system
import platform
import subprocess

import sys
import os

import tkinter as tk
import tkinter.ttk
import tkinter.filedialog
from PIL import ImageTk

from ManageFlashcardsFrame import ManageFlashcardsFrame
from StudyFrame import StudyFrame
from ManageDecksFrame import ManageDecksFrame
from DatabaseManager import DatabaseManager
from ImportExportManager import ImportExportManager

class Program(tk.Tk):

    WINDOW_WIDTH = 510
    WINDOW_HEIGHT = 442
    STUDYFRAME = "StudyFrame"
    DECKSFRAME = "ManageDecksFrame"
    FLASHCARDSFRAME = "ManageFlashcardsFrame"

    def __init__(self):
        # Initialize super class
        tk.Tk.__init__(self)

        # It will be used for all database and data operations by this class and by child frames.
        self.database_manager = DatabaseManager()

        # It will be used for all import and export operations.
        self.import_export_manager = ImportExportManager(self.database_manager)

        # Set the app favicon
        # The r prefix specifies it as a raw string. See: https://stackoverflow.com/q/55890931/3780985
        if platform.system() == 'Darwin':  # macOS
            icon_path = self.resource_path(r"icon/favicon.gif")
            img = tk.PhotoImage(file=icon_path)                      
            self.tk.call('wm', 'iconphoto', self._w, img)
        elif platform.system() == 'Windows':  # Windows
            icon_path = self.resource_path(r"icon\favicon.ico")
            self.iconbitmap(self, icon_path)
        else:  # linux variants
            icon_path = self.resource_path(r"icon/favicon.gif")
            img = tk.PhotoImage(file=icon_path)                      
            self.tk.call('wm', 'iconphoto', self._w, img)
        # end set the app favicon

        # Set title of the main window
        self.title("Flashcards")

        # Disable resize on main window
        self.resizable(False, False)
        # self.maxsize(Program.WINDOW_HEIGHT, Program.WINDOW_WIDTH)
        # self.minsize(Program.WINDOW_HEIGHT, Program.WINDOW_WIDTH)

        # Create menu bar
        self.menu_bar = tk.Menu(self)
        self.config(menu=self.menu_bar)

        # Create Menu
        self.decks_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Menu", menu=self.decks_menu)
        self.decks_menu.add_command(label="Decks...", command=self.show_manage_decks_frame)
        self.decks_menu.add_command(label="Flashcards...", command=self.show_manage_flashcards_frame)
        self.decks_menu.add_separator()
        self.decks_menu.add_command(label="Import...", command=self.import_deck_from_csv_file)
        self.decks_menu.add_command(label="Export...", command=self.export_deck_as_csv_file_menu_command)
        self.decks_menu.add_separator()
        self.decks_menu.add_command(label="Quit", command=self.quit)

        # Create About menu
        self.help_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Help", menu=self.help_menu)
        self.help_menu.add_command(label="Open manual", command=self.open_manual_file)
        self.help_menu.add_separator()
        self.help_menu.add_command(label="About", command=self.show_about_box)

        # All other views (frames, i.e. StudyFrame, DecksFrame, etc.) will be children of the container frame
        # that is set up here. We can raise any child frame to bring it to the front (to the top of the stack).
        # For details: https://stackoverflow.com/a/7557028
        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        # Frames dictionary will hold all the Frames (other views) that the GUI of the program consists of.
        self.frames = dict()

        # Current frame
        self.current_frame = None

        # Initialize child frames by iterating through the "Frame classes", classes that inherits from tk.Frame
        # Add initialized frames to the self.frames dictionary. It will provide access and persistence (in memory).
        for frame in (StudyFrame, ManageDecksFrame, ManageFlashcardsFrame):
            frame_name = frame.__name__
            # print("A new frame is being initialized; frame_name is", frame_name)

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

        # Center the main window on screen
        self.center_window()

        # Welcome user by showing the decks frame.
        self.show_manage_decks_frame()

    # Necessary to use data files with pyinstaller in onefile mode.
    # https://stackoverflow.com/a/44352931/3780985
    # https://stackoverflow.com/a/44438174/3780985
    def resource_path(self, relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base_path, relative_path)

    def open_deck(self, index: int) -> None:
        """
        Opens a deck and starts a study session if all preconditions are met.
        :param int index: Index of the deck in self.database_manager.decks[] list
        """
        deck = None
        if len(self.database_manager.decks) > 0:
            deck = self.database_manager.decks[index]
        if deck is not None:
            deck.set_due_flashcards(self.database_manager)
            count = len(deck.flashcards)
            due_count = len(deck.due_flashcards)
            if count > 0:
                if due_count > 0:
                    # There are some due flashcards. Study session will only use those.
                    self.database_manager.load_deck(index)
                    self.show_study_frame(show_only_due_flashcards=True)
                    self.frames[Program.STUDYFRAME].start_study_session()
                else:
                    # There are not any due flashcards. Study session will use all flashcards in the deck if user
                    # confirms.
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

    def show_study_frame(self, show_only_due_flashcards=True) -> None:
        """
        Brings Study frame to the top.
        :param bool show_only_due_flashcards: True when only due flashcards are used in study session.
        """
        deck = self.database_manager.deck
        frame = self.frames[Program.STUDYFRAME]

        # Ask to save if there is any unsaved changes in the entry boxes
        if isinstance(self.current_frame, ManageFlashcardsFrame):
            manage_flashcards_frame = self.frames[Program.FLASHCARDSFRAME]
            manage_flashcards_frame.ask_save_question_if_necessary()

        # Safety check
        if isinstance(frame, StudyFrame):
            try:
                if hasattr(deck, "flashcards"):
                    if len(deck.flashcards) > 0:
                        frame.prepare_view(show_only_due_flashcards=show_only_due_flashcards)
                        frame.tkraise()
                        self.current_frame = frame
                    else:
                        tk.messagebox.showwarning("Info", "You should add some flashcards first.", icon="info")
            except AttributeError:
                tk.messagebox.showwarning("Info", "You should create a deck first.")
        else:
            print("Error in show_study_frame()")

    def show_manage_decks_frame(self) -> None:
        """
        Brings Manage Decks frame to the top.
        """
        deck = self.database_manager.deck
        frame = self.frames[Program.DECKSFRAME]

        # Ask to save if there is any unsaved changes in the entry boxes
        if isinstance(self.current_frame, ManageFlashcardsFrame):
            manage_flashcards_frame = self.frames[Program.FLASHCARDSFRAME]
            manage_flashcards_frame.ask_save_question_if_necessary()

        # Safety check
        if isinstance(frame, ManageDecksFrame):
            frame.prepare_manage_decks_view()
            frame.tkraise()
            self.current_frame = frame
            if deck is None:
                tk.messagebox.showwarning("Info", """
                Welcome to Flashcards!

                You can create decks of flashcards, and study them later to improve your knowledge and long-time memory.

                Click on the "New deck" button below to start.
                """, icon='info')
                frame.new_deck_button.focus_force()
        else:
            print("Error in show_manage_decks_frame()")

    def show_manage_flashcards_frame(self) -> None:
        """
        Brings Manage Flashcards frame to the top.
        """
        deck = self.database_manager.deck
        frame = self.frames[Program.FLASHCARDSFRAME]
        # Safety check
        if isinstance(frame, ManageFlashcardsFrame):
            try:
                if hasattr(deck, "flashcards"):
                    # frame.load_deck()
                    frame.prepare_manage_flashcards_view()
                    frame.tkraise()
                    self.current_frame = frame
                else:
                    tk.messagebox.showwarning("Info", "You should add some flashcards first.", icon="info")
            except Exception as error:
                print("Exception in show_manage_flashcards_frame(): ", error)
        else:
            print("Error in show_manage_flashcards_frame()")

    def center_window(self):
        """
        Center the window on the screen.
        """

        if platform.system() == 'Darwin':  # macOS
            window_width = Program.WINDOW_WIDTH
            window_height = Program.WINDOW_HEIGHT
        elif platform.system() == 'Windows':  # Windows
            window_width = Program.WINDOW_WIDTH
            window_height = Program.WINDOW_HEIGHT
        else:  # linux variants
            window_width = Program.WINDOW_WIDTH + 130
            window_height = Program.WINDOW_HEIGHT
        # end if
        
        # print(self.winfo_width())
        # print(self.winfo_height())

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # print(screen_width)
        # print(screen_height)

        x_cordinate = int((screen_width / 2) - (window_width / 2))
        y_cordinate = int((screen_height / 2) - (window_height / 2))

        self.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))

    def show_about_box(self) -> None:
        """
        Displays about box.
        """
        message_text = """
        Flashcards v1.0 RC1
        
        Copyright 2020 Ertugrul Harman
        E-mail: harmancode@gmail.com
        Twitter: https://twitter.com/harmancode
        Web: https://harman.page
        
        Flashcards is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
        
        See the GNU General Public License for more details. You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>.
        """
        tk.messagebox.showinfo(title="About Flashcards", message=message_text)

    def import_deck_from_csv_file(self) -> None:
        """
        Import a new deck from a csv file.
        """
        filename = tkinter.filedialog.askopenfilename(filetypes=(("CSV files", "*.csv"),
                                                                 ("All files", "*.*")))
        if filename:
            try:
                # print("filepath: ", filename)
                result = self.import_export_manager.import_csv_file(filename)
                if result:
                    self.frames["ManageDecksFrame"].prepare_manage_decks_view()
                    tk.messagebox.showwarning("Info", "Import is successful.", icon="info")
                else:
                    tk.messagebox.showwarning("Info", "Import has failed.")
            except:  # <- naked except is a bad idea
                tk.messagebox.showerror("Open Source File", "Failed to read file\n'%s'" % filename)
        else:
            pass
            # print("Filename error in import_deck_from_csv_file()")

    def export_deck_as_csv_file_menu_command(self):
        """
        Export deck as a csv file menu command click handler
        """

        deck_to_be_exported = None

        # Check if Decks view is open
        if isinstance(self.current_frame, ManageDecksFrame):
            deck_to_be_exported = self.current_frame.get_selected_deck()
        elif isinstance(self.current_frame, ManageFlashcardsFrame):
            deck_to_be_exported = self.database_manager.deck
        elif isinstance(self.current_frame, StudyFrame):
            deck_to_be_exported = self.database_manager.deck
        else:
            print("Error in export_deck_as_csv_file_menu_command()")

        if deck_to_be_exported is not None:
            filename = tkinter.filedialog.asksaveasfilename(filetypes=(("CSV files", "*.csv"),
                                                               ("All files", "*.*")))
            if filename != "":

                # filepath = filename.name
                filepath = filename

                # Add .csv extension only if there is not one already.
                if filepath[-4:].lower() != ".csv":
                    filepath += ".csv"

                result = self.import_export_manager.export_csv_file(filepath=filepath, deck=deck_to_be_exported)

                if result:

                    export_message = """
                    Export is successful.
                    
                    Please note that export functionality is for using this data in other applications. Therefore only deck's title, and all flashcards in the deck have been exported. Other data about the deck, such as last study date, due date, your previous responses to the flashcards, etc., have not been exported.
                    
                    If you intend to back up your data to use it later with this program you should not use export functionality for this purpose. You can back up \"Flashcards.db\" file that is located in the program directory (by copying it to another location, for example), and restore it later.
                    """

                    tk.messagebox.showinfo("Info", export_message)

            else:
                # Cancel pressed
                pass

        else:
            if len(self.database_manager.decks) == 0:
                tk.messagebox.showwarning("Info", "There is not any deck to export. Click on \"New deck\" button to "
                                                  "create one.")
            else:
                tk.messagebox.showwarning("Info", "Please select a deck first.")

    def open_manual_file(self):
        """
        Opens the manual file by using the default PDF reader of the operating system
        """
        # Source: https://stackoverflow.com/a/435669
        if platform.system() == 'Darwin':  # macOS
            filepath = self.resource_path(r"manual/Flashcards.pdf")
            subprocess.call(('open', filepath))
        elif platform.system() == 'Windows':  # Windows
            filepath = self.resource_path(r"manual\Flashcards.pdf")
            os.startfile(filepath)
        else:  # linux variants
            filepath = self.resource_path(r"manual/Flashcards.pdf")
            subprocess.call(('xdg-open', filepath))
