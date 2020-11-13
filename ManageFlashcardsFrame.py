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
        self.flashcards_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Setup Treeview

        # Create a new frame specific to Treeview and its scrollbar to easily use scrollbar in there
        self.treeview_frame = tk.Frame(self.flashcards_frame)
        self.treeview_frame.grid(row=0, column=0, pady=10, padx=10, sticky="nsew")

        self.treeview = tk.ttk.Treeview(self.treeview_frame, columns=("Question", "Answer"))
        self.treeview.grid(row=0, column=0, sticky="nsew")

        self.yscrollbar = tk.ttk.Scrollbar(self.treeview_frame, orient='vertical', command=self.treeview.yview)
        self.treeview.configure(yscrollcommand=self.yscrollbar.set)

        # self.treeview.grid(row=0, column=0, sticky="nsew")
        self.yscrollbar.grid(row=0, column=1, sticky='nse')
        self.yscrollbar.configure(command=self.treeview.yview)

        self.treeview_frame.grid_rowconfigure(0, weight=1)
        self.treeview_frame.grid_columnconfigure(0, weight=1)

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
        self.add_flashcard_button = tk.Button(self.right_frame, text="Add new flashcard", command=self.add_new_flashcard)
        self.add_flashcard_button.grid(row=0, column=0, pady=10, sticky="nsew")

        self.remove_flashcard_button = tk.Button(self.right_frame, text="Remove flashcard", command=self.remove_flashcard)
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
        self.save_flashcard_button = tk.Button(self.edit_flashcard_frame, text="Save flashcard", command=self.edit_flashcard)
        self.save_flashcard_button.grid(row=0, column=2, rowspan=2, padx=10, pady=10, sticky="e")

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
        if deck is not None:
            deck_title_string = "Deck: " + deck.truncated_title()
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

    def refresh_treeview(self):
        self.remove_all_data_from_treeview()
        self.clean_entry_boxes()
        self.add_data_to_treeview()
        self.treeview.focus_set()

        flashcards = self.controller.database_manager.deck.flashcards
        if len(flashcards) > 0:
            self.question_entry.config(state="normal")
            self.answer_entry.config(state="normal")
            self.save_flashcard_button.config(state="normal")
        else:
            self.question_entry.config(state="disabled")
            self.answer_entry.config(state="disabled")
            self.save_flashcard_button.config(state="disabled")

    def remove_all_data_from_treeview(self):
        # self.treeview.delete(*self.treeview.get_children())
        for i in self.treeview.get_children():
            self.treeview.delete(i)

    def index_of_last_selection_in_treeview(self):
        # https://stackoverflow.com/a/30615520/3780985
        row_index = int(self.treeview.focus())
        print("item: ", self.treeview.item(row_index))
        return row_index


    def get_flashcards_when_multiple_selection_in_treeview(self):
        row_indexes = self.treeview.selection()
        print(row_indexes)
        selected_flashcards = []
        for row_index in row_indexes:
            selected_flashcard = self.controller.database_manager.deck.flashcards[int(row_index)]
            selected_flashcards.append(selected_flashcard)
            print("selected_flashcard: ", selected_flashcard.question)
        return selected_flashcards

    def select_first_flashcard(self):
        # Select first row if there is any
        if len(self.controller.database_manager.deck.flashcards) > 0:
            self.treeview.selection_set(0)
            self.treeview.focus(0)
            self.fill_entry_boxes_based_on_selected_row_index(0)

    def select_last_flashcard_in_treeview(self):
        # Select last flashcard item in treeview, i.e. give it focus
        flashcards = self.controller.database_manager.deck.flashcards
        count = len(flashcards)
        if count > 0:
            self.treeview.selection_set(count-1)
            self.treeview.focus(count-1)
            self.fill_entry_boxes_based_on_selected_row_index(count-1)

    def select_flashcard_at_index(self, index):
        flashcards = self.controller.database_manager.deck.flashcards
        count = len(flashcards)
        if index <= count - 1:
            self.treeview.selection_set(index)
            self.treeview.focus(index)
            self.fill_entry_boxes_based_on_selected_row_index(index)

    def fill_entry_boxes_based_on_selected_row_index(self, index):
        if self.controller.database_manager.deck.flashcards[index] is not None:
            self.current_flashcard = self.controller.database_manager.deck.flashcards[index]
            self.clean_entry_boxes()
            self.question_entry.insert(0, self.current_flashcard.question)
            self.answer_entry.insert(0, self.current_flashcard.answer)
        else:
            print("There is not any flashcard at index", index)

    # Binding function
    def row_selected(self, event):
        self.fill_entry_boxes_based_on_selected_row_index(self.index_of_last_selection_in_treeview())

    def go_back(self):
        self.controller.show_frame("StudyFrame")

    def add_new_flashcard(self):
        add_flashcard = True
        while add_flashcard:
            add_flashcard = False

            question = tk.simpledialog.askstring(title="New flashcard", prompt="Please enter the question:",
                                                       initialvalue="")
            if question is not None:
                question = question.strip()
                if len(question) > 0:
                    answer = tk.simpledialog.askstring(title="New flashcard", prompt="Please enter the answer:",
                                                              initialvalue="")
                    if answer is not None:
                        answer = answer.strip()
                        if len(answer) > 0:
                            deck_id = self.controller.database_manager.deck.deck_id

                            new_flashcard_id = self.controller.database_manager.add_new_flashcard_to_db(deck_id=deck_id,
                                                                                                        question=question, answer=answer)
                            new_flashcard = Flashcard(new_flashcard_id, deck_id, question, answer)
                            self.controller.database_manager.deck.flashcards.append(new_flashcard)
                            self.refresh_treeview()

                            add_another = tk.messagebox.askquestion("Add again?", "Flashcard has been added successfully. Would you like to add another flashcard?")
                            if add_another == "yes":
                                add_flashcard = True
                            else:
                                self.select_last_flashcard_in_treeview()

                        else:
                            tk.messagebox.showwarning("Info", "Answer cannot be empty.")
                else:
                    tk.messagebox.showwarning("Info", "Question cannot be empty.")

    def remove_flashcard(self):
        flashcards = self.get_flashcards_when_multiple_selection_in_treeview()
        for flashcard in flashcards:
            self.controller.database_manager.delete_flashcard_from_db(flashcard.flashcard_id)
            self.controller.database_manager.deck.flashcards.remove(flashcard)
        self.clean_entry_boxes()
        self.refresh_treeview()
        self.select_first_flashcard()

    def clean_entry_boxes(self):
        self.question_entry.delete(0, tk.END)
        self.answer_entry.delete(0, tk.END)

    def edit_flashcard(self):
        selected_treeview_index = self.index_of_last_selection_in_treeview()
        flashcard = self.controller.database_manager.deck.flashcards[selected_treeview_index]
        question = str(self.question_entry.get())
        answer = str(self.answer_entry.get())
        question = question.strip()
        answer = answer.strip()
        if len(question) == 0 or len(answer) == 0:
            tk.messagebox.showwarning("Info", "Question or answer cannot be empty.")
        else:
            flashcard.question = question
            flashcard.answer = answer
            self.controller.database_manager.update_flashcard_in_db(flashcard_id=flashcard.flashcard_id,
                                                                    question=question,
                                                                    answer=answer)
            self.refresh_treeview()
            self.select_flashcard_at_index(selected_treeview_index)

    def prepare_view(self):
        self.refresh_treeview()
        self.select_first_flashcard()