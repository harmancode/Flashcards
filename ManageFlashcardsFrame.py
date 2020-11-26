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

import tkinter as tk
from typing import Optional

from Flashcard import Flashcard


class ManageFlashcardsFrame(tk.Frame):

    def __init__(self, parent, controller):
        """
        ManageFlashcardsFrame is the class that provides the view and controller for editing flashcards scene.
        :param tk.Frame parent: Container frame in Program class that acts as the parent view, holding all the main views
        (scenes) of the Program as child frames
        :param Program.Program controller: Program class that acts as the parent controller, provides access to model methods
        and properties.
        """
        tk.Frame.__init__(self, parent)

        # Provides direct access to the main controller (Program) and indirect access to the model (DatabaseManager).
        self.controller = controller

        # The parent frame of the treeview_frame. It will provide a label and a visual frame to the treeview.
        self.flashcards_frame = tk.LabelFrame(self, text="Flashcards")
        self.flashcards_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Set up Treeview

        # Create a new frame specific to Treeview and its scrollbar to easily use scrollbar in there
        self.treeview_frame = tk.Frame(self.flashcards_frame)
        self.treeview_frame.grid(row=0, column=0, pady=10, padx=10, sticky="nsew")

        self.treeview = tk.ttk.Treeview(self.treeview_frame, columns=("Question", "Answer"))
        self.treeview.grid(row=0, column=0, pady=2, ipady=2, sticky="nsew")

        self.yscrollbar = tk.ttk.Scrollbar(self.treeview_frame, orient='vertical', command=self.treeview.yview)
        self.treeview.configure(yscrollcommand=self.yscrollbar.set)

        self.yscrollbar.grid(row=0, column=1, sticky='nse')
        self.yscrollbar.configure(command=self.treeview.yview)

        # Format columns
        # We set width as 0 because we will not use parent-children rows
        self.treeview.column("#0", width=0, minwidth=0)
        self.treeview.column("#1", anchor="w", width="364")
        self.treeview.column("#2", anchor="e", width="80")

        # Create headings to the columns
        self.treeview.heading("#0", text="")
        self.treeview.heading("#1", text="Question", anchor="w", )
        self.treeview.heading("#2", text="Answer", anchor="e")

        # Add binding to the treeview
        self.treeview.bind("<ButtonRelease-1>", self.row_selected)

        # Add edit flashcard frame
        self.edit_flashcard_frame = tk.LabelFrame(self, text="Edit Flashcard...")
        self.edit_flashcard_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        self.question_label = tk.Label(self.edit_flashcard_frame, text="Question:")
        self.question_label.grid(row=0, rowspan=2, column=0, sticky="w")

        self.answer_label = tk.Label(self.edit_flashcard_frame, text="Answer:")
        self.answer_label.grid(row=2, rowspan=2, column=0, sticky="w")

        # self.question_entry = tk.Entry(self.edit_flashcard_frame)
        # self.question_entry.grid(row=0, column=1, padx=10, pady=5, sticky="nsew")

        self.question_textentry = tk.Text(self.edit_flashcard_frame, height=2, width=50, wrap="word")
        self.question_textentry.grid(row=0, column=1, ipadx=10, ipady=10, pady=4, sticky="nsew")
        self.question_textentry.configure(font=("Sans", 9))

        # self.answer_entry = tk.Entry(self.edit_flashcard_frame)
        # self.answer_entry.grid(row=1, column=1, padx=10, pady=5, sticky="nsew")

        self.answer_textentry = tk.Text(self.edit_flashcard_frame, height=2, wrap="word")
        self.answer_textentry.grid(row=2, column=1, ipadx=10, ipady=10, pady=4, sticky="nsew")
        self.answer_textentry.configure(font=("Sans", 9))

        # Save Flashcard
        self.save_flashcard_button = tk.Button(self.edit_flashcard_frame, text="Save flashcard",
                                               command=self.save_flashcard_button_pressed)
        self.save_flashcard_button.grid(row=0, column=2, rowspan=2, padx=10, pady=10, sticky="we")

        self.cancel_button = tk.Button(self.edit_flashcard_frame, text="Cancel",
                                       command=self.cancel_button_pressed)
        self.cancel_button.grid(row=1, column=2, rowspan=2, padx=10, pady=10, sticky="we")

        # Stretch the entry fields
        self.edit_flashcard_frame.grid_columnconfigure(0, weight=0)
        self.edit_flashcard_frame.grid_columnconfigure(1, weight=1)
        self.edit_flashcard_frame.grid_columnconfigure(2, weight=0)
        self.edit_flashcard_frame.grid_rowconfigure(0, weight=1)
        self.edit_flashcard_frame.grid_rowconfigure(1, weight=1)
        self.edit_flashcard_frame.grid_rowconfigure(2, weight=1)
        self.edit_flashcard_frame.grid_rowconfigure(3, weight=1)

        # Set up bottom frame
        self.bottom_frame = tk.Frame(self)
        self.bottom_frame.grid(row=2, column=0, sticky="nsew")

        # Add buttons to bottom frame
        self.add_flashcard_button = tk.Button(self.bottom_frame, text="Add flashcard", width=14,
                                              command=self.add_new_flashcard)
        self.add_flashcard_button.grid(row=0, column=1, padx=10, pady=10)

        self.remove_flashcard_button = tk.Button(self.bottom_frame, text="Remove flashcard", width=14,
                                                 command=self.remove_flashcard)
        self.remove_flashcard_button.grid(row=0, column=3, padx=10, pady=10)

        self.start_studying_button = tk.Button(self.bottom_frame, text="Start studying", width=14,
                                               command=self.start_studying)
        self.start_studying_button.grid(row=0, column=2, padx=10, pady=10)

        # Center group of buttons horizontally by creating empty columns on the left and right side,
        # and giving them a weight so that they consume all extra space
        # https://stackoverflow.com/a/48934682/3780985
        self.bottom_frame.grid_columnconfigure(0, weight=1)
        self.bottom_frame.grid_columnconfigure(4, weight=1)

        self.flashcards_frame.grid_rowconfigure(0, weight=1)
        self.flashcards_frame.grid_columnconfigure(0, weight=1)

        self.treeview_frame.grid_rowconfigure(0, weight=1)
        self.treeview_frame.grid_columnconfigure(0, weight=1)

        self.grid_columnconfigure(0, weight=1)

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=0)

        # All GUI setup is complete. Now prepare the view contents.
        self.prepare_manage_flashcards_view()

    def load_deck(self) -> None:
        """
        Make the view ready for user interaction by loading the deck, flashcards, and configuring GUI elements.
        """
        deck = self.controller.database_manager.deck
        # Safety check
        if deck is not None:
            deck_title_string = "Deck: " + deck.get_truncated_title()
            self.flashcards_frame.config(text=deck_title_string)
            # self.refresh_treeview()
        else:
            print("Deck is None in load_deck()")

    def add_data_to_treeview(self) -> None:
        """
        Fill the treeview with data.
        """
        try:
            deck = self.controller.database_manager.deck
            if hasattr(deck, "flashcards"):
                flashcards = self.controller.database_manager.deck.flashcards
                flashcards_count = len(flashcards)
                for index in range(flashcards_count):
                    question = flashcards[index].question
                    answer = flashcards[index].answer
                    self.treeview.insert(parent='', index='end', iid=index, text="", values=(question, answer))
        except AttributeError:
            tk.messagebox.showwarning("Info", "You should create a deck first.")
        except Exception as error:
            print("Error in add_data_to_treeview(): ", error)

    def refresh_treeview(self) -> None:
        """
        Remove all contents from treeview, fill it with data and give it focus.
        """
        self.remove_all_data_from_treeview()
        self.clear_entry_boxes()
        self.add_data_to_treeview()
        self.treeview.focus_set()

        # flashcards = self.controller.database_manager.deck.flashcards

        # if len(flashcards) > 0:
        #     # self.question_entry.config(state="normal")
        #     # self.answer_entry.config(state="normal")
        #     self.question_textentry.config(state="normal")
        #     self.answer_textentry.config(state="normal")
        #     self.save_flashcard_button.config(state="normal")
        # else:
        #     # self.question_entry.config(state="disabled")
        #     # self.answer_entry.config(state="disabled")
        #     self.question_textentry.config(state="disabled")
        #     self.answer_textentry.config(state="disabled")
        #     self.save_flashcard_button.config(state="disabled")

    def remove_all_data_from_treeview(self) -> None:
        """
        Remove all contents from treeview
        """
        for i in self.treeview.get_children():
            self.treeview.delete(i)

    def index_of_last_selection_in_treeview(self) -> int:
        """
        Returns the index of the item that is last selected in treeview.
        :return: Index of the item in the treeview. -1 if there is no item.
        """
        # Details: https://stackoverflow.com/a/30615520/3780985
        result = -1
        if self.treeview.focus() != '':
            row_index = int(self.treeview.focus())
            # print("item: ", self.treeview.item(row_index))
            result = row_index
        return result

    def get_flashcards_when_multiple_selection_in_treeview(self) -> [Flashcard]:
        """
        Returns selected flashcards in treeview as a list.
        :return: [Flashcard]
        """
        row_indexes = self.treeview.selection()
        selected_flashcards = []
        for row_index in row_indexes:
            selected_flashcard = self.controller.database_manager.deck.flashcards[int(row_index)]
            selected_flashcards.append(selected_flashcard)
        return selected_flashcards

    def select_first_flashcard(self) -> None:
        """
        Calls select_flashcard_at_index(self, index) for the first row in treeview.
        """
        # Select first row if there is any
        if self.controller.database_manager.deck is not None:
            if len(self.controller.database_manager.deck.flashcards) > 0:
                self.select_flashcard_at_index(0)
            else:
                pass
                # print("Error: No flashcard for select_first_flashcard()")

    def select_last_flashcard_in_treeview(self) -> None:
        """
        Calls select_flashcard_at_index(self, index) for the last row in treeview.
        """
        # Select last flashcard item in treeview, i.e. give it focus
        flashcards = self.controller.database_manager.deck.flashcards
        count = len(flashcards)
        if count > 0:
            self.select_flashcard_at_index(count - 1)
        else:
            print("Error: No flashcard for select_last_flashcard_in_treeview()")

    def select_flashcard_at_index(self, index) -> None:
        """
        Give selection to the given index in the treeview. Assign it to the self.current.flashcard. Fill edit boxes.
        :param index:
        """
        flashcards = self.controller.database_manager.deck.flashcards
        count = len(flashcards)
        # Safety check
        if 0 <= index <= count - 1:
            self.treeview.selection_set(index)
            self.treeview.focus(index)
            self.fill_entry_boxes_based_on_selected_row_index(index)
        else:
            print("Error: No flashcard for select_flashcard_at_index(), index: ", index)

    def selected_flashcard(self) -> Optional[Flashcard]:
        """
        Returns if there is a flashcard selected in the treeview.
        :return: Checks the treeview if there is an item selected. If yes, returns selected Flashcard. If no,
        returns None.
        :rtype: Flashcard or None
        """
        result = None
        index = self.index_of_last_selection_in_treeview()
        if (len(self.controller.database_manager.deck.flashcards) > 0) and (index >= 0):
            if self.controller.database_manager.deck.flashcards[index] is not None:
                selected_flashcard = self.controller.database_manager.deck.flashcards[index]
                result = selected_flashcard
        return result

    def fill_entry_boxes_based_on_selected_row_index(self, index) -> None:
        """
        Fill text entry boxes based on the selected row index in the treeview.
        :param int index: Index of selected row in treeview.
        """
        if (len(self.controller.database_manager.deck.flashcards) > 0) and (index >= 0):
            if self.controller.database_manager.deck.flashcards[index] is not None:
                current_flashcard = self.controller.database_manager.deck.flashcards[index]
                self.clear_entry_boxes()
                # self.question_entry.insert(0, current_flashcard.question)
                # self.answer_entry.insert(0, current_flashcard.answer)
                self.question_textentry.insert(1.0, current_flashcard.question)
                self.answer_textentry.insert(1.0, current_flashcard.answer)
            else:
                print("There is not any flashcard at index", index)

    # Binding function for treeview selection event
    def row_selected(self, event):
        """
        Event handler for row selection in treeview.
        :param event: Treeview button release
        """
        # Check if there are any flashcards in the deck
        if len(self.controller.database_manager.deck.flashcards) > 0:
            # Set add_mode_switch to False. This will automatically enable entry boxes for the selected flashcard
            # if any.
            self.add_mode_switch(status=False)

    def start_studying(self) -> None:
        """
        Event handler for start_studying button click. It finds the deck index and calls self.controller.open_deck(
        index=index) with that index.
        """
        index = self.controller.database_manager.decks.index(self.controller.database_manager.deck)
        self.controller.open_deck(index=index)

    def remove_selection_from_treeview(self) -> None:
        """
        Removes any selection from the treeview.
        """
        # See: https://stackoverflow.com/a/48593195
        if len(self.treeview.selection()) > 0:
            self.treeview.selection_remove(self.treeview.selection()[0])

    def add_mode_switch(self, status) -> None:
        """
        There are two modes: self.adding_new_flashcard = True or False
        When it is True, user is adding a new flashcard by using the entry boxes.
        When it is False, user is editing an existing flashcard by using the entry boxes.
        This functions makes this switch, configures the view, and variables accordingly.
        :param status: True when user is adding a new Flashcard. Otherwise, by default, False.
        :type status: bool
        """
        if status:
            self.adding_new_flashcard = True
            self.edit_flashcard_frame.config(text="Add new flashcard... ")
            self.clear_entry_boxes()
            self.question_textentry.focus_set()
            self.remove_selection_from_treeview()
        else:
            self.adding_new_flashcard = False
            index = self.index_of_last_selection_in_treeview()
            # Safety check
            if index >= 0:
                self.fill_entry_boxes_based_on_selected_row_index(index)
                self.edit_flashcard_frame.config(text="Edit flashcard... ")

        # Set the status of the buttons depending on the add/edit mode/status
        self.configure_buttons()

    def cancel_button_pressed(self) -> None:
        """
        Event handler for cancel button click.
        """
        self.add_mode_switch(status=False)
        self.treeview.focus_set()
        index = self.index_of_last_selection_in_treeview()
        if index >= 0:
            self.treeview.selection_set(index)

    def add_new_flashcard(self) -> None:
        """
        Just calls self.add_mode_switch by passing True as status parameter. This function is called when user clicks
        on the "Add new flashcard..." button.
        """
        self.add_mode_switch(status=True)

    # def add_new_flashcard(self):
    #     """
    #     Event handler for self.add_flashcard_button click. It adds a new flashcard by requesting a question and an
    #     answer from the user by performing necessary checks. It adds it to the database, to the decks list in memory,
    #     and to the treeview.
    #     """
    #
    #     # done: remove this function and merge it with create_new_flashcard()
    #
    #     # done: Add new flashcards by using the text entry boxes. That would be more user friendly, especially
    #     #  when user enters a question or answer longer than allowed.
    #
    #     add_flashcard = True
    #     while add_flashcard:
    #
    #         add_flashcard = False
    #
    #         question = tk.simpledialog.askstring(title="New flashcard", prompt="Please enter the question:",
    #                                              initialvalue="")
    #         if question is not None:
    #             question = question.strip()
    #
    #             if len(question) > 0:
    #                 if len(question) > Flashcard.MAX_LENGTH_OF_QUESTION:
    #                     warning_message = "Question cannot be longer than {} characters.".format(
    #                         Flashcard.MAX_LENGTH_OF_QUESTION)
    #                     tk.messagebox.showwarning("Too long question", warning_message)
    #                 else:
    #                     answer = tk.simpledialog.askstring(title="New flashcard", prompt="Please enter the answer:",
    #                                                        initialvalue="")
    #                     if answer is not None:
    #                         answer = answer.strip()
    #                         if len(answer) > 0:
    #                             if len(answer) > Flashcard.MAX_LENGTH_OF_ANSWER:
    #                                 warning_message = "Answer cannot be longer than {} characters.".format(
    #                                     Flashcard.MAX_LENGTH_OF_ANSWER)
    #                                 tk.messagebox.showwarning("Too long answer", warning_message)
    #                             else:
    #                                 deck_id = self.controller.database_manager.deck.deck_id
    #
    #                                 due_date_string = self.controller.database_manager.today_as_string()
    #
    #                                 # Add flashcard to the database and obtain a unique flashcard_id
    #                                 new_flashcard_id = self.controller.database_manager.add_new_flashcard_to_db(
    #                                     deck_id=deck_id,
    #                                     question=question,
    #                                     answer=answer,
    #                                     last_study_date=None,
    #                                     due_date_string=due_date_string)
    #
    #                                 # Initialize new Flashcard object with the just-obtained flashcard_id
    #                                 new_flashcard = Flashcard(new_flashcard_id=new_flashcard_id,
    #                                                           deck_id=deck_id,
    #                                                           question=question,
    #                                                           answer=answer,
    #                                                           last_study_date=None,
    #                                                           due_date_string=due_date_string,
    #                                                           inter_repetition_interval=0,
    #                                                           easiness_factor=0,
    #                                                           repetition_number=0)
    #
    #                                 # Add initialized Flashcard object to the deck.flashcard list
    #                                 self.controller.database_manager.deck.flashcards.append(new_flashcard)
    #
    #                                 self.refresh_treeview()
    #
    #                                 add_another = tk.messagebox.askquestion("Add again?",
    #                                                                         "Flashcard has been added successfully. Would you like to add another flashcard?")
    #                                 if add_another == "yes":
    #                                     add_flashcard = True
    #                                 else:
    #                                     self.select_last_flashcard_in_treeview()
    #                         else:
    #                             tk.messagebox.showwarning("Info", "Answer cannot be empty.")
    #             else:
    #                 tk.messagebox.showwarning("Info", "Question cannot be empty.")

    def remove_flashcard(self) -> None:
        """
        Deletes a flashcard from database, from model, and from the view. And then refreshes the view and selects
        first flashcard in the treeview, if there is any.
        """
        flashcards = self.get_flashcards_when_multiple_selection_in_treeview()
        for flashcard in flashcards:
            self.controller.database_manager.delete_flashcard_from_db(flashcard.flashcard_id)
            self.controller.database_manager.deck.flashcards.remove(flashcard)
        self.clear_entry_boxes()
        self.refresh_treeview()
        self.select_first_flashcard()
        self.activate_adding_flashcard_mode_if_no_flashcard()

    def activate_adding_flashcard_mode_if_no_flashcard(self):
        """
        Activate adding flashcard mode if there is no flashcard in the deck. This will make the program more
        easy-to-use, because user will not have to click on "Add flashcard" button to add a new flashcard.
        """
        if self.controller.database_manager.deck is not None:
            if len(self.controller.database_manager.deck.flashcards) == 0:
                self.add_mode_switch(True)
            else:
                self.add_mode_switch(False)

    def clear_entry_boxes(self) -> None:
        """
        Clear text the text entry boxes in the frame.
        """
        # self.question_entry.delete(0, tk.END)
        # self.answer_entry.delete(0, tk.END)
        self.question_textentry.delete(1.0, tk.END)
        self.answer_textentry.delete(1.0, tk.END)

    def update_existing_flashcard(self) -> None:
        """
                Updates flashcard by using texts in entry boxes.
                """
        selected_treeview_index = self.index_of_last_selection_in_treeview()
        # Safety check
        if selected_treeview_index >= 0:
            flashcard = self.controller.database_manager.deck.flashcards[selected_treeview_index]
            # question = str(self.question_entry.get())
            # answer = str(self.answer_entry.get())
            question = str(self.question_textentry.get("1.0", tk.END))
            answer = str(self.answer_textentry.get("1.0", tk.END))
            question = question.strip()
            answer = answer.strip()
            if len(question) == 0 or len(answer) == 0:
                tk.messagebox.showwarning("Info", "Question or answer cannot be empty.")
            elif len(question) > Flashcard.MAX_LENGTH_OF_QUESTION:
                warning_message = "Question cannot be longer than {} characters.".format(
                    Flashcard.MAX_LENGTH_OF_QUESTION)
                tk.messagebox.showwarning("Too long question", warning_message)
            elif len(answer) > Flashcard.MAX_LENGTH_OF_ANSWER:
                warning_message = "Answer cannot be longer than {} characters.".format(
                    Flashcard.MAX_LENGTH_OF_ANSWER)
                tk.messagebox.showwarning("Too long answer", warning_message)
            else:
                flashcard.question = question
                flashcard.answer = answer
                self.controller.database_manager.update_flashcard_in_db(flashcard_id=flashcard.flashcard_id,
                                                                        question=question,
                                                                        answer=answer,
                                                                        last_study_date=flashcard.last_study_date,
                                                                        due_date_string=flashcard.due_date_string,
                                                                        inter_repetition_interval=flashcard.inter_repetition_interval,
                                                                        easiness_factor=flashcard.easiness_factor,
                                                                        repetition_number=flashcard.repetition_number
                                                                        )
                self.refresh_treeview()
                self.select_flashcard_at_index(selected_treeview_index)

    def are_entry_box_entries_valid_to_save(self, show_warnings:bool=False) -> bool:
        """
        Checks if entry boxes have valid entries to be saved as Flashcard properties.
        :param show_warnings: If True, user will be warned about the issue.
        :type show_warnings: bool
        :return: True if entries are valid. False if not.
        :rtype: bool
        """
        result = False
        question_is_valid = True
        answer_is_valid = True
        question = self.question_textentry.get("1.0", tk.END).strip()
        answer = self.answer_textentry.get("1.0", tk.END).strip()

        if len(question) <= 0 or len(answer) <= 0:
            if show_warnings:
                tk.messagebox.showwarning("Info", "Question or answer cannot be empty.")
            question_is_valid = False
        elif len(question) > Flashcard.MAX_LENGTH_OF_QUESTION:
            if show_warnings:
                warning_message = "Question cannot be longer than {} characters.".format(
                    Flashcard.MAX_LENGTH_OF_QUESTION)
                tk.messagebox.showwarning("Too long question", warning_message)
            question_is_valid = False
        elif len(answer) > Flashcard.MAX_LENGTH_OF_ANSWER:
            if show_warnings:
                warning_message = "Answer cannot be longer than {} characters.".format(
                    Flashcard.MAX_LENGTH_OF_ANSWER)
                tk.messagebox.showwarning("Too long answer", warning_message)
            answer_is_valid = False

        if question_is_valid and answer_is_valid:
            result = True
        else:
            result = False

        return result

    def create_new_flashcard(self) -> None:
        """
        Creates and adds a new flashcard to the current deck. It saves it to the database by calling necessary
        functions.
        """
        if self.are_entry_box_entries_valid_to_save(show_warnings=True):
            deck_id = self.controller.database_manager.deck.deck_id

            due_date_string = self.controller.database_manager.today_as_string()

            # It is safe to take data from textentry boxes because their validity has just been checked in
            # self.are_entry_box_entries_valid_to_save()
            question = self.question_textentry.get("1.0", tk.END).strip()
            answer = self.answer_textentry.get("1.0", tk.END).strip()

            # Add flashcard to the database and obtain a unique flashcard_id
            new_flashcard_id = self.controller.database_manager.add_new_flashcard_to_db(
                deck_id=deck_id,
                question=question,
                answer=answer,
                last_study_date=None,
                due_date_string=due_date_string)

            # Initialize new Flashcard object with the just-obtained flashcard_id
            new_flashcard = Flashcard(flashcard_id=new_flashcard_id,
                                      deck_id=deck_id,
                                      question=question,
                                      answer=answer,
                                      last_study_date=None,
                                      due_date_string=due_date_string,
                                      inter_repetition_interval=0,
                                      easiness_factor=0,
                                      repetition_number=0)

            # Add initialized Flashcard object to the deck.flashcard list
            self.controller.database_manager.deck.flashcards.append(new_flashcard)

            self.refresh_treeview()

            self.select_last_flashcard_in_treeview()

            self.scroll_to_the_bottom_of_treeview()

            self.add_mode_switch(False)

    def scroll_to_the_bottom_of_treeview(self) -> None:
        """
        Scroll to the bottom of the treeview.
        "You can use tree.yview_moveto(1) to display the bottom of the table. The yview_moveto method takes as
        argument the fraction of the total (scrollable) widget height that you want to be off-screen to the top.
        So, yview_moveto(0) will display the top part of the table, yview_moveto(1) the bottom part and
        yview_moveto(0.5) will adjust the display so that the top half of the widget is hidden."
        Source: https://stackoverflow.com/a/42161808
        """
        self.treeview.yview_moveto(1)

    def save_flashcard_button_pressed(self) -> None:
        """
        Called when "Save flashcard" buttons pressed. It calls relevant functions based on the status of the
        self.adding_new_flashcard flag.
        """

        # Set self.adding_new_flashcard = True when there is no flashcard in the deck. Because when there is no
        # flashcard, user will probably trying to add a new flashcard by using the entry boxes, instead of trying to
        # edit something.
        if len(self.controller.database_manager.deck.flashcards) == 0:
            self.adding_new_flashcard = True

        if self.adding_new_flashcard:
            self.create_new_flashcard()
        else:
            self.update_existing_flashcard()

    def configure_buttons(self) -> None:
        """
        Set the status of the buttons depending on the adding/editing flashcard status, and on the amount of flashcards.
        """
        if self.adding_new_flashcard:
            self.add_flashcard_button.config(state="disabled")
            self.remove_flashcard_button.config(state="disabled")
            self.start_studying_button.config(state="disabled")
        else:
            self.add_flashcard_button.config(state="normal")
            self.remove_flashcard_button.config(state="normal")
            self.start_studying_button.config(state="normal")

        if len(self.controller.database_manager.deck.flashcards) == 0:
            self.start_studying_button.config(state="disabled")
            self.remove_flashcard_button.config(state="disabled")
        else:
            self.start_studying_button.config(state="normal")
            self.remove_flashcard_button.config(state="normal")

    def is_there_unsaved_changes_in_flashcard(self) -> bool:
        """
        Check if there is any changes made in the flashcard's question or answer.
        :return: True if there is any change. False if there is not.
        :rtype: bool
        """
        result = False
        question_in_entrybox = self.question_textentry.get("1.0", tk.END).strip()
        answer_in_entrybox = self.answer_textentry.get("1.0", tk.END).strip()
        selected_flashcard = self.selected_flashcard()
        if selected_flashcard != None:
            if (question_in_entrybox != selected_flashcard.question or
                answer_in_entrybox != selected_flashcard.answer):
                result = True
        return result

    def ask_save_question_if_necessary(self):
        asking_is_necessary = False
        adding_new_flashcard = self.adding_new_flashcard
        unsaved_changes = self.is_there_unsaved_changes_in_flashcard()
        valid_entries = self.are_entry_box_entries_valid_to_save()
        if (adding_new_flashcard or unsaved_changes) and valid_entries:
            response = tk.messagebox.askquestion('Save changes?', 'Would you like to save this flashcard?')
            if response == 'yes':
                self.save_flashcard_button_pressed()

    def prepare_manage_flashcards_view(self) -> None:
        """
        Prepare the view before bringing it to the front (displaying it to the user), by refreshing the treeview and
        selecting the first flashcard in the treeview.
        """
        # done: refresh_treeview() is called here and in load_deck(). Eliminate duplicate calls.
        self.load_deck()
        self.refresh_treeview()
        self.select_first_flashcard()
        self.activate_adding_flashcard_mode_if_no_flashcard()
