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

import random

try:
    import tkinter as tk  # python 3
    from tkinter import font as tkfont  # python 3
except ImportError:
    import Tkinter as tk  # python 2
    import tkFont as tkfont  # python 2

from Flashcard import Flashcard


class StudyFrame(tk.Frame):
    NO_FLASHCARD_FOUND_TEXT = "Welcome to Flashcards!\n\nTo add some flashcards, click Flashcards in the Menu on the top of this window. Then click Add new flaschard button."
    NO_DECK_FOUND_FLASHCARD_TEXT = "Welcome to Flashcards!\n\nTo create a deck, click Decks in the Menu on the top of this window. Then click New Deck button."
    NO_DECK_FOUND_STATUS_TEXT = "Welcome to Flashcards!"

    def __init__(self, parent, controller):
        """
        StudyFrame is the class that provides the view and controller for study sessions.
        :param tk.Frame parent: Container frame in Program class that acts as the parent view, holding all the main views (
        scenes) of the Program as child frames
        :param Program.Program controller: Program class that acts as the parent controller, provides access to model methods
        and properties.
        """
        # Initialize super class
        tk.Frame.__init__(self, parent)

        # *** Model attributes ***

        # Provides direct access to the main controller (Program) and indirect access to the model (DatabaseManager).
        self.controller = controller

        # Holds the current deck's index in the list of decks
        self.deck_index = int()

        # Holds the current flashcard's index in the list of flashcards
        self.flashcard_index = int()

        # Holds displayed flashcard object
        self.flashcard = None

        # True when loaded flashcard is flipped, i.e. showing the answer.
        # False when loaded flashcard is not flipped, i.e. showing the question.
        self.flipped = False

        # False when user wants to go over all the flashcards, due or not due.
        self.show_only_due_flashcards = True

        # Flashcards will be loaded from this list. It will be re-filled by self.randomize_deck() at the beginning of
        # each study session, based on the preferences of the user.
        self.randomized_flashcards: [Flashcard] = None

        # *** View attributes ***

        # Create three frames
        # top_frame is for displaying flashcards
        self.top_frame = tk.Frame(self)
        # bottom_frame is for buttons
        self.bottom_frame = tk.Frame(self)
        # status_frame is for status bar
        self.status_frame = tk.Frame(self)

        self.top_frame.grid(row=0, column=0, pady=10, padx=10, sticky="nsew")
        self.bottom_frame.grid(row=1, column=0, pady=10, padx=10, sticky="new")
        self.status_frame.grid(row=2, column=0, pady=0, padx=10, sticky="new")

        image_path = self.controller.resource_path("image\index_card.gif")
        # print("image_path: ", image_path)
        self.index_card_image = tk.PhotoImage(master=self.top_frame, file=image_path)

        # Configure flashcard text
        self.flashcard_label = tk.Label(self.top_frame, text="", wraplength=350,
                                        font=("Arial", 14, "bold"),
                                        image=self.index_card_image, compound=tk.CENTER)
        self.flashcard_label.grid(row=0, column=0)

        # Create three buttons for the bottom frame
        self.very_hard_button = tk.ttk.Button(self.bottom_frame, text='Very Hard',
                                              command=self.very_hard_button_clicked)
        self.hard_button = tk.ttk.Button(self.bottom_frame, text='Hard',
                                         command=self.hard_button_clicked)
        self.normal_button = tk.ttk.Button(self.bottom_frame, text='Show Answer',
                                           command=self.flip)
        self.easy_button = tk.ttk.Button(self.bottom_frame, text='Easy',
                                         command=self.easy_button_clicked)
        self.super_easy_button = tk.ttk.Button(self.bottom_frame, text='Super Easy',
                                               command=self.super_easy_button_clicked)

        # Set up the buttons. They will be hidden when self.flipped = False, except self.normal_button, which will
        # always be visible.
        self.very_hard_button.grid(row=0, column=1, padx=10, pady=5)
        self.hard_button.grid(row=0, column=2, padx=10, pady=5)
        self.normal_button.grid(row=0, column=3, padx=10, pady=5)
        self.easy_button.grid(row=0, column=4, padx=10, pady=5)
        self.super_easy_button.grid(row=0, column=5, padx=10, pady=5)

        # Center group of buttons horizontally by creating empty columns on the left and right side,
        # and giving them a weight so that they consume all extra space
        # https://stackoverflow.com/a/48934682/3780985
        self.bottom_frame.grid_columnconfigure(0, weight=1)
        self.bottom_frame.grid_columnconfigure(6, weight=1)

        # Create "Deck Table" as a TreeView
        self.table = tk.ttk.Treeview(self, columns=["Question", "Answer"])

        # Define table columns
        self.deck_table_columns = ["Question", "Answer"]
        self.table.column("#0", width=120, minwidth=25)
        self.table.column("Question", anchor="w", width=120)
        self.table.column("Answer", anchor="e", width=120)

        # Define table column headings (headers?)
        self.table.heading("#0", text="Label", anchor="w")
        self.table.heading("Question", text="Question", anchor="w")
        self.table.heading("Answer", text="Answer", anchor="e")

        # Add a status bar
        status_bar_text = self.produce_status_bar_text()
        # print("status_bar_text: ", status_bar_text)
        self.status_bar = tk.ttk.Label(self.status_frame, text=status_bar_text, border=1, relief=tk.SUNKEN)
        self.status_bar.pack(fill=tk.X)

        self.prepare_view(show_only_due_flashcards=True)

    def load_flashcard(self) -> None:
        """
        Displays the question or answer of the flashcard depending on the status of self.flipped flag.
        """
        deck = self.controller.database_manager.deck
        # print("load_flashcard")
        # print("self.flashcard_index: ", self.flashcard_index)

        if deck is not None:
            # Safety check
            if self.flashcard_index < len(self.randomized_flashcards):
                flashcard = self.randomized_flashcards[self.flashcard_index]
                self.flashcard = flashcard
                if self.flipped:
                    # Display the answer
                    self.flashcard_label.config(fg="green")
                    self.flashcard_label.config(text=flashcard.answer)
                else:
                    # Display the question
                    self.flashcard_label.config(fg="red")
                    self.flashcard_label.config(text=flashcard.question)
                self.set_status_bar_text()
                # Give focus to the middle button in all cases
                self.normal_button.focus_set()
            else:
                print("Error: Index not in range in load_flashcard()")
        else:
            print("Error: Deck is None in load_flashcard()")

    def show_next_flashcard(self) -> None:
        """
        Displays next flashcard if there is one. Otherwise notifies user that study session is over.
        """
        deck = self.controller.database_manager.deck
        if deck is not None:
            if self.flashcard_index < len(self.randomized_flashcards) - 1:
                self.flipped = False
                self.flashcard_index += 1
                self.load_flashcard()
                self.configure_buttons()
            else:
                tk.messagebox.showinfo("All done!", "All done! Congrats!")
                self.controller.show_manage_decks_frame()
        else:
            print("Error: Deck is None in show_next_flashcard()")

    # Not used anymore.
    # def show_previous_flashcard(self):
    #     """
    #     Displays previous flashcard, if there is one.
    #     """
    #     if self.flashcard_index != 0:
    #         self.flipped = False
    #         self.flashcard_index -= 1
    #         self.load_flashcard()

    def flip(self) -> None:
        """
        Flips the flashcard, i.e. it shows the answer.
        """
        # Originally the program was designed to let user flip the flashcard as much as she wants. But now it can
        # only be flipped once. Maybe in the future this feature can be used again, to show the question after
        # displaying the answer for example.
        if self.flipped:
            # Answer has already been shown, therefore it is certain that user clicked on the "Normal" button.
            self.normal_button_clicked()
        else:
            # Answer has not been shown before. User tapped on a grade button. Show the answer and toggle the flag.
            self.flipped = True
            self.load_flashcard()
            self.configure_buttons()

    def very_hard_button_clicked(self) -> None:
        """
        Processes the answer of the user, and calls self.show_next_flashcard()
        """
        self.process_answer(grade=0)
        self.show_next_flashcard()

    def hard_button_clicked(self) -> None:
        """
        Processes the answer of the user, and calls self.show_next_flashcard()
        """
        self.process_answer(grade=1)
        self.show_next_flashcard()

    def normal_button_clicked(self) -> None:
        """
        Processes the answer of the user, and calls self.show_next_flashcard()
        """
        self.process_answer(grade=2)
        self.show_next_flashcard()

    def easy_button_clicked(self) -> None:
        """
        Processes the answer of the user, and calls self.show_next_flashcard()
        """
        self.process_answer(grade=3)
        self.show_next_flashcard()

    def super_easy_button_clicked(self) -> None:
        """
        Processes the answer of the user, and calls self.show_next_flashcard()
        """
        self.process_answer(grade=4)
        self.show_next_flashcard()

    def configure_buttons(self) -> None:
        """
        Hides or shows the buttons based on the current situation.
        """
        if self.flipped:
            self.super_easy_button.grid()
            self.easy_button.grid()
            self.hard_button.grid()
            self.very_hard_button.grid()
            self.normal_button.config(text="Normal")
        else:
            self.super_easy_button.grid_remove()
            self.easy_button.grid_remove()
            self.hard_button.grid_remove()
            self.very_hard_button.grid_remove()
            self.normal_button.config(text="Show Answer")

    def set_status_bar_text(self) -> None:
        """
        Sets the text in the status bar.
        """
        self.status_bar.config(text=self.produce_status_bar_text())

    def produce_status_bar_text(self) -> str:
        """
        Creates a string and returns it to be displayed in the status bar based on the current situation.
        :return: str
        """
        deck = self.controller.database_manager.deck
        if deck is None:
            return StudyFrame.NO_DECK_FOUND_STATUS_TEXT
        elif len(deck.flashcards) == 0:
            return StudyFrame.NO_DECK_FOUND_STATUS_TEXT
        else:
            # Check if randomized_flashcards list is present, for safety. This list is required to create a status
            # bar string.
            if self.randomized_flashcards is not None:
                flashcard_count = len(self.randomized_flashcards)
                text = "Deck: " + deck.get_truncated_title() + \
                       " | Flashcard " + str(self.flashcard_index + 1) + " out of " + str(flashcard_count)
            else:
                # String will be empty if there is self.randomized_flashcards not set.
                text = ""
            return text

    def randomize_deck(self) -> None:
        """
        Sets the self.randomized_flashcards list based on the status of the flag of self.show_only_due_flashcards.
        """
        deck = self.controller.database_manager.deck
        # Include all frashcards as default
        flashcards = deck.flashcards
        if self.show_only_due_flashcards:
            # Only include due flashcards
            flashcards = deck.due_flashcards
        if deck is not None:
            try:
                # Set the current deck here
                self.randomized_flashcards = flashcards
                random.shuffle(self.randomized_flashcards)
                # self.randomized_flashcards.shuffle()
            except Exception as error:
                print("Exception randomize_deck: ", error)
        else:
            print("Error: Deck is None in randomize_deck()")

    def prepare_view(self, show_only_due_flashcards: bool) -> None:
        """
        Resets the flags, prepares the data and the view before a study session starts.
        :param bool show_only_due_flashcards: True when self.randomized_flashcard set will include only due flashcards.
        False when all flashcards of the deck will be included to the self.randomized_deck.
        """
        self.show_only_due_flashcards = show_only_due_flashcards
        deck = self.controller.database_manager.deck
        self.flashcard_index = 0
        self.flipped = False
        if deck is None:
            self.normal_button.config(state="disabled")
            # Normally flashcard should not be displayed when there is no deck. This is set here for safety.
            self.flashcard_label.config(text=StudyFrame.NO_DECK_FOUND_FLASHCARD_TEXT)
        else:
            # Set up due flashcards of the current deck
            deck.set_due_flashcards(self.controller.database_manager)
            # Set up self.randomized_flashcards attribute based on the self.show_only_due_flashcards flag.
            self.randomize_deck()
            # Check if there is a flashcard to be displayed for safety.
            if len(self.randomized_flashcards) < 1:
                self.normal_button.config(state="disabled")
                print("Flashcard cannot be loaded because there is no flashcard.")
                self.flashcard_label.config(text=StudyFrame.NO_FLASHCARD_FOUND_TEXT)
            else:
                # Load the first flashcard and set the "Show Answer" button enabled.
                self.load_flashcard()
                self.normal_button.config(state="enabled")
        self.set_status_bar_text()
        self.configure_buttons()

    def start_study_session(self) -> None:
        """
        Update deck's last study attribute. Reset self.flipped and self_flashcard_index.
        """
        deck = self.controller.database_manager.deck
        if deck is not None:
            deck.set_last_study_datetime(self.controller.database_manager)
            self.flipped = False
            self.flashcard_index = 0

    def process_answer(self, grade: int) -> None:
        """
        Process the answer of the user by calling current flashcard's process_answer() method.
        :param grade: int   Between 0 and 4. Indicates the difficulty of the current flashcard.
        """
        self.flashcard.process_answer(grade=grade, database_manager=self.controller.database_manager)
