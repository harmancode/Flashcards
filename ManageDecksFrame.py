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

from typing import Optional

from Deck import Deck

try:
    import tkinter as tk  # python 3
    from tkinter import font as tkfont  # python 3
    import tkinter.simpledialog
except ImportError:
    import Tkinter as tk  # python 2
    import tkFont as tkfont  # python 2


class ManageDecksFrame(tk.Frame):

    def __init__(self, parent, controller):
        """
        ManageDecksFrame is the class that provides the view and controller for editing decks scene.
        :param tk.Frame parent: Container frame in Program class that acts as the parent view, holding all the main views
        (scenes) of the Program as child frames
        :param Program.Program controller: Program class that acts as the parent controller, provides access to model methods
        and properties.
        """
        tk.Frame.__init__(self, parent)

        # Provides direct access to the main controller (Program) and indirect access to the model (DatabaseManager).
        self.controller = controller

        # Setup select deck frame
        self.select_deck_frame = tk.LabelFrame(self, text="Select deck")
        self.select_deck_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Set up Treeview

        # Create a new frame specific to Treeview and its scrollbar to easily use scrollbar in there
        self.treeview_frame = tk.Frame(self.select_deck_frame)
        self.treeview_frame.grid(row=0, column=0, pady=10, padx=10, sticky="nsew")

        self.treeview = tk.ttk.Treeview(self.treeview_frame, columns=("Title", "Last Study", "Due", "Total"))
        self.treeview.grid(row=0, column=0, sticky="nsew")

        self.yscrollbar = tk.ttk.Scrollbar(self.treeview_frame, orient='vertical', command=self.treeview.yview)
        self.treeview.configure(yscrollcommand=self.yscrollbar.set)

        self.yscrollbar.grid(row=0, column=1, sticky='nse')
        self.yscrollbar.configure(command=self.treeview.yview)

        # Format columns
        # We set width as 0 because we will not use parent-children rows
        self.treeview.column("#0", width=0, minwidth=0)
        self.treeview.column("#1", anchor="w", width="235")
        self.treeview.column("#2", anchor="e", width="70")
        self.treeview.column("#3", anchor="e", width="70")
        self.treeview.column("#4", anchor="e", width="70")

        # Create headings to the columns
        self.treeview.heading("#0", text="")
        self.treeview.heading("#1", text="Title", anchor="w", )
        self.treeview.heading("#2", text="Last Study", anchor="e")
        self.treeview.heading("#3", text="Due", anchor="e")
        self.treeview.heading("#4", text="Total", anchor="e")

        # Fill treeview with data
        self.add_data_to_treeview()

        # Select first row if there is any
        decks = self.controller.database_manager.decks
        if len(decks) > 0:
            self.treeview.selection_set(0)
            self.treeview.focus(0)

        # Set up buttons frame
        self.buttons_frame = tk.Frame(self)
        self.buttons_frame.grid(row=1, column=0, padx=10, pady=10, sticky="sew")

        self.study_button = tk.Button(self.buttons_frame, text="Study", command=self.switch_to_study_mode, width=9)
        self.rename_button = tk.Button(self.buttons_frame, text="Rename", command=self.rename_deck, width=9)
        self.delete_button = tk.Button(self.buttons_frame, text="Delete", command=self.delete_deck, width=9)
        self.new_deck_button = tk.Button(self.buttons_frame, text="New deck", command=self.new_deck, width=9)
        self.edit_deck_button = tk.Button(self.buttons_frame, text="Flashcards",
                                          command=self.show_manage_flashcards_frame, width=9)

        # Place buttons
        self.study_button.grid(row=0, column=1, padx=6, pady=10, sticky="nsew")
        self.edit_deck_button.grid(row=0, column=2, padx=6, pady=10, sticky="nsew")
        self.rename_button.grid(row=0, column=3, padx=6, pady=10, sticky="nsew")
        self.delete_button.grid(row=0, column=4, padx=6, pady=10, sticky="nsew")
        self.new_deck_button.grid(row=0, column=5, padx=6, pady=10, sticky="nsew")

        # Give weights to the widgets
        self.set_weights()

    def set_weights(self) -> None:
        """
        Set weights of the visual elements to align them on the frame as intended.
        """
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=0)

        self.select_deck_frame.grid_rowconfigure(0, weight=1)
        self.select_deck_frame.grid_columnconfigure(0, weight=0)

        self.treeview_frame.grid_rowconfigure(0, weight=1)
        self.treeview_frame.grid_columnconfigure(0, weight=0)

        # Center group of buttons horizontally by creating empty columns on the left and right side,
        # and giving them a weight so that they consume all extra space
        # https://stackoverflow.com/a/48934682/3780985
        self.buttons_frame.grid_columnconfigure(0, weight=1)
        self.buttons_frame.grid_columnconfigure(6, weight=1)

    def new_deck(self) -> None:
        """
        Handles click event of New deck button. Strips it if given title length is too long. It initializes a new
        Deck object, and adds it to the decks list. Also it saves it to the database permanently.
        """

        new_title = tkinter.simpledialog.askstring(title="New deck", prompt="Please enter a title for the new deck:",
                                                   initialvalue="")

        # Safety check
        if new_title is not None:

            # Strip the given text first
            new_title = new_title.strip()

            # Safety checks for given text
            if len(new_title) > 0:
                if len(new_title) > Deck.MAXIMUM_LENGTH_OF_DECK_TITLE:
                    tk.messagebox.showwarning("Too long title", "The title you typed was too long. It was shortened.")
                new_title = new_title[:Deck.MAXIMUM_LENGTH_OF_DECK_TITLE]

                # Add the new deck to the database and get a new deck id meanwhile
                new_deck_id = self.controller.database_manager.add_new_deck_to_db(new_title, None)

                # Initialize the new deck with the obtained id
                new_deck = Deck(title=new_title, deck_id=new_deck_id, last_study_datetime=None)

                # Add initialized object to the decks list
                self.controller.database_manager.decks.append(new_deck)

                # Set newly added deck as the current deck, if it is the only deck.
                if len(self.controller.database_manager.decks) == 1:
                    self.controller.database_manager.set_first_deck_as_the_current_deck_if_possible()

                # GUI tasks
                self.refresh_treeview()
                self.select_last_deck_in_treeview()

                # For user's convenience
                self.offer_to_create_flashcards()
            else:
                tk.messagebox.showwarning("Info", "Title cannot be empty.")

    def offer_to_create_flashcards(self) -> None:
        """
        Ask users if they want to create flashcards upon creating first (or only) deck, for their convenience.
        """
        deck = self.get_selected_deck()
        count_of_decks = len(self.controller.database_manager.decks)
        if (deck is not None) and (count_of_decks == 1):
            tk.messagebox.showwarning("Info",
                                      "Now you have a deck. Good job! To create some flashcards for this deck, you can click Flashcards button below.",
                                      icon="info")

    def rename_deck(self) -> None:
        """
        Handles the click event of self.rename_button. Renames the deck selected in the treeview. Updates the data in
        memory and in database.
        """
        deck = self.get_selected_deck()
        if deck is not None:
            new_title = tkinter.simpledialog.askstring(title="Rename deck",
                                                       prompt="Please enter new title of the deck:",
                                                       initialvalue=self.get_selected_deck_title())
            if new_title is not None:
                # print(new_title)
                selected_index = self.get_selected_treeview_index()

                deck.title = new_title
                self.controller.database_manager.update_deck_in_db(deck.deck_id, deck.title, deck.last_study_datetime)

                self.refresh_treeview()
                self.treeview.selection_set(selected_index)
                self.treeview.focus(selected_index)
        else:
            tk.messagebox.showwarning("Info", "You should create a deck first.")

    def refresh_treeview(self) -> None:
        """
        Removes all contents from the treeview and fills it again with the current data.
        """
        self.remove_all_data_from_treeview()
        self.add_data_to_treeview()

    def remove_all_data_from_treeview(self) -> None:
        """
        Removes all the contents from the treeview.
        """
        for i in self.treeview.get_children():
            self.treeview.delete(i)

    def delete_deck(self) -> None:
        """
        Permanently deletes a deck from the memory and from the database.
        """
        decks = self.controller.database_manager.decks
        if len(decks) > 0:
            deck = decks[self.get_selected_treeview_index()]
            flashcard_count = len(deck.flashcards)
            confirmation_message = "This deck will be deleted: " + deck.title + "\n\n"
            if flashcard_count == 0:
                confirmation_message += "It does not contain any flashcards."
            elif flashcard_count == 1:
                confirmation_message += "It contains one flashcard. It will be deleted with the deck."
            else:
                confirmation_message += "It contains " + str(
                    flashcard_count) + " flashcards. They will be deleted with the deck."
            # Icons in messagebox: https://stackoverflow.com/a/59344478/3780985
            confirmation = tk.messagebox.askokcancel("Please confirm",
                                                     confirmation_message, icon="warning")
            if confirmation:
                # Delete the deck from the database
                self.controller.database_manager.delete_deck_from_db(deck.deck_id)
                # Remove the deck from the decks list, so that it can be removed from the memory
                self.controller.database_manager.decks.remove(deck)
                # Update view
                self.refresh_treeview()
                # Assign a new deck as current deck, if current deck has just been deleted.
                if self.controller.database_manager.deck.deck_id == deck.deck_id:
                    self.controller.database_manager.set_first_deck_as_the_current_deck_if_possible()
        else:
            tk.messagebox.showwarning("Info", "You should create a deck first.")

    def show_manage_flashcards_frame(self) -> None:
        """
        Updates current deck based on the selection in treeview, and displays ManageFlashcardsFrame.
        """
        deck = self.get_selected_deck()
        if deck is not None:
            self.controller.database_manager.deck = deck
            self.controller.show_manage_flashcards_frame()
        else:
            tk.messagebox.showwarning("Info", "You should create a deck first.")

    def switch_to_study_mode(self) -> None:
        """
        Brings StudyFrame to the front by calling controller's open_deck method with the index parameter which is
        derived from the selected row in the treeview.
        """
        self.controller.open_deck(self.get_selected_treeview_index())

    def get_selected_treeview_index(self) -> int:
        """
        Gets the index of the selected row in the treeview
        :return: int
        """
        selected_item = self.treeview.focus()
        # selected_item_dict = self.treeview.item(selected_item)
        index = self.treeview.index(selected_item)
        # print("selected_deck_index: ", index)
        result = index
        if (index < 0) or (index > (len(self.controller.database_manager.decks) - 1)):
            print("Error: Invalid index in get_selected_treeview_index")
            result = 0
        return result

    def get_selected_deck_title(self) -> str:
        """
        Returns the title of the deck that is delected in the treeview
        :return: str
        """
        selected_item = self.treeview.focus()
        selected_item_dict = self.treeview.item(selected_item)
        item_list = selected_item_dict["values"]
        if len(item_list) > 0:
            title = item_list[0]
        else:
            print("Error in get_selected_deck_title()")
            title = ""
        # print("title: ", title)
        return title

    def get_selected_deck(self) -> Optional[Deck]:
        """
        Finds selected deck by using self.get_selected_treeview_index() and returns it.
        :return: Deck | None
        """
        result = None
        decks = self.controller.database_manager.decks
        if len(decks) > 0:
            selected_deck = self.controller.database_manager.decks[self.get_selected_treeview_index()]
            # print("selected_deck: ", selected_deck.title)
            # print("selected_desk's flashcards:")
            # for flashcard in selected_deck.flashcards:
            #     print(flashcard.flashcard_id, flashcard.deck_id, flashcard.question, flashcard.answer)
            result = selected_deck
        return result

    def add_data_to_treeview(self) -> None:
        """
        Fills treeview with data derived from decks
        """
        # Add data to the treeview
        decks = self.controller.database_manager.decks
        deck_count = len(decks)
        for index in range(deck_count):
            deck = decks[index]
            title = deck.title
            deck.set_due_flashcards(self.controller.database_manager)
            due_count = len(deck.due_flashcards)
            total_count = len(deck.flashcards)
            last_study = deck.get_last_study_datetime_as_formatted_string()
            self.treeview.insert(parent='', index='end', iid=index, text="",
                                 values=(title, last_study, due_count, total_count))

    def select_first_row_in_treeview(self) -> None:
        """
        Selects first row in the treeview if there is any row.
        """
        if len(self.controller.database_manager.decks) > 0:
            self.treeview.selection_set(0)
            self.treeview.focus(0)

    def select_last_deck_in_treeview(self) -> None:
        """
        Selects last row in the treeview if there is any row.
        """
        # Select last flashcard item in treeview, i.e. give it focus
        decks = self.controller.database_manager.decks
        count = len(decks)
        if count > 0:
            self.treeview.selection_set(count - 1)
            self.treeview.focus(count - 1)

    def prepare_manage_decks_view(self) -> None:
        """
        Prepare the view before bringing it to the front (displaying it to the user), by refreshing the treeview and
        selecting the first row in the treeview.
        """
        self.refresh_treeview()
        self.select_first_row_in_treeview()
