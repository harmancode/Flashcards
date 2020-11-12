from Flashcard import Flashcard
from Deck import Deck

import tkinter as tk


class ManageFlashcardsFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller

        # self.deck = self.controller.deck
        # self.flashcards = self.deck.flashcards
        self.current_flashcard: Flashcard = None

        # self.deck_title_frame = tk.LabelFrame(self, text="Deck")
        # self.deck_title_frame.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        #
        # self.deck_label = tk.Label(self)
        # self.deck_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.flashcards_frame = tk.LabelFrame(self, text="Flashcards")
        self.flashcards_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        # Setup Treeview
        self.treeview = tk.ttk.Treeview(self.flashcards_frame, columns=("Question", "Answer"))
        self.treeview.grid(row=0, column=0, sticky="nsew")

        # Format columns
        # We set width as 0 because we will not use parent-children rows
        self.treeview.column("#0", width=0, minwidth=0)
        self.treeview.column("#1", anchor="w", width="240")
        self.treeview.column("#2", anchor="e", width="70")

        # Create headings to the columns
        self.treeview.heading("#0", text="")
        self.treeview.heading("#1", text="Question", anchor="w", )
        self.treeview.heading("#2", text="Answer", anchor="e")

        # Add binding to the treeview
        # self.treeview.bind("<Double-1>", self.row_selected)
        self.treeview.bind("<ButtonRelease-1>", self.row_selected)

        self.treeview.grid(padx=10, pady=10, sticky="nsew")

        # # Add bottom frame
        # self.bottom_frame = tk.LabelFrame(self, text="Save")
        # self.bottom_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        # # self.bottom_frame.rowconfigure(2, weight=1)
        # # self.bottom_frame.columnconfigure(2, weight=1)
        #
        # self.save_button = tk.Button(self.bottom_frame, text="Save")
        # self.save_button.grid(row=0, column=0, padx=10)

        # Add right frame for buttons
        self.right_frame = tk.Frame(self)
        self.right_frame.grid(row=0, column=1, rowspan=2, padx=10, pady=10, sticky="nsew")

        # Add buttons to right frame
        self.add_flashcard_button = tk.Button(self.right_frame, text="Add new flashcard")
        self.add_flashcard_button.grid(row=0, column=0, pady=10, sticky="nsew")

        self.remove_flashcard_button = tk.Button(self.right_frame, text="Remove flashcard")
        self.remove_flashcard_button.grid(row=1, column=0, pady=10, sticky="nsew")

        self.move_up_button = tk.Button(self.right_frame, text="Move up")
        self.move_up_button.grid(row=2, column=0, pady=10, sticky="nsew")

        self.move_down_button = tk.Button(self.right_frame, text="Move down")
        self.move_down_button.grid(row=3, column=0, pady=10, sticky="nsew")

        # Add edit flashcard frame
        self.edit_flashcard_frame = tk.LabelFrame(self, text="Edit Flashcard")
        self.edit_flashcard_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        # Stretch the entry fields
        self.edit_flashcard_frame.grid_columnconfigure(1, weight=6)
        self.edit_flashcard_frame.grid_columnconfigure(2, weight=1)

        # This gives error: https://stackoverflow.com/questions/49317933/declare-stringvar-variable-as-class-variable-in-python
        # self.question_var = tk.StringVar(self)
        # self.answer_var = tk.StringVar(self)

        self.question_label = tk.Label(self.edit_flashcard_frame, text="Question:")
        self.question_label.grid(row=0, column=0, sticky="w")
        self.answer_label = tk.Label(self.edit_flashcard_frame, text="Answer:")
        self.answer_label.grid(row=1, column=0, sticky="w")

        self.question_entry = tk.Entry(self.edit_flashcard_frame)
        self.question_entry.grid(row=0, column=1, padx=10, pady=3, sticky="nsew")

        self.answer_entry = tk.Entry(self.edit_flashcard_frame)
        self.answer_entry.grid(row=1, column=1, padx=10, pady=3, sticky="nsew")

        # Save Flashcard
        self.save_flashcard = tk.Button(self.edit_flashcard_frame, text="Save flashcard")
        self.save_flashcard.grid(row=0, column=2, rowspan=2, padx=10, pady=10, sticky="e")

        # Setup bottom frame
        self.bottom_frame = tk.Frame(self)
        self.bottom_frame.grid(row=2, column=0, columnspan=2, sticky="nsew")

        # This is required to center the button
        self.bottom_frame.grid_columnconfigure(0, weight=1)

        self.go_back_button = tk.Button(self.bottom_frame, text="Close", command=self.go_back)
        self.go_back_button.grid(row=0, column=0, padx=10, pady=10)

        self.load_deck()

    def load_deck(self):
        deck = self.controller.database_manager.deck
        deck_title_string = "Deck: " + deck.title
        self.flashcards_frame.config(text=deck_title_string)
        self.refresh_treeview()

    def add_data_to_treeview(self):
        # Add data to the treeview
        flashcards = self.controller.database_manager.deck.flashcards
        flashcards_count = len(flashcards)
        for index in range(flashcards_count):
            question = flashcards[index].question
            answer = flashcards[index].answer
            self.treeview.insert(parent='', index='end', iid=index, text="", values=(question, answer))
            self.select_first_flashcard()

    def refresh_treeview(self):
        self.remove_all_data_from_treeview()
        self.add_data_to_treeview()

    def remove_all_data_from_treeview(self):
        # self.treeview.delete(*self.treeview.get_children())
        for i in self.treeview.get_children():
            self.treeview.delete(i)

    def selected_flashcard_index(self):
        selected_item = self.treeview.focus()
        # selected_item_dict = self.treeview.item(selected_item)
        index = self.treeview.index(selected_item)
        return index

    def select_first_flashcard(self):
        # Select first row if there is any
        if len(self.controller.database_manager.deck.flashcards) > 0:
            self.treeview.selection_set(0)
            self.treeview.focus(0)
            self.select_flashcard(0)

    def select_flashcard(self, index):
        if self.controller.database_manager.deck.flashcards[index] is not None:
            self.current_flashcard = self.controller.database_manager.deck.flashcards[index]
            self.question_entry.delete(0, tk.END)
            self.question_entry.insert(0, self.current_flashcard.question)
            self.answer_entry.delete(0, tk.END)
            self.answer_entry.insert(0, self.current_flashcard.answer)
        else:
            print("There is not any flashcard at index", index)

    # Binding function
    def row_selected(self, event):
        self.select_flashcard(self.selected_flashcard_index())

    def go_back(self):
        self.controller.show_frame("StudyFrame")