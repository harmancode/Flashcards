from Deck import Deck

try:
    import tkinter as tk  # python 3
    from tkinter import font as tkfont  # python 3
    import tkinter.simpledialog
except ImportError:
    import Tkinter as tk  # python 2
    import tkFont as tkfont  # python 2


class ManageDecksFrame(tk.Frame):

    MAXIMUM_LENGTH_OF_DECK_TITLE = 250

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller

        # print("controller.winfo_height(): ", controller.winfo_height())
        # print("controller.winfo_width()", controller.winfo_width())
        # print("self.winfo_width(): ", self.winfo_width())

        # Setup select deck frame
        self.select_deck_frame = tk.LabelFrame(self, text="Select deck")
        self.select_deck_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Setup Treeview

        # Create a new frame specific to Treeview and its scrollbar to easily use scrollbar in there
        self.treeview_frame = tk.Frame(self.select_deck_frame)
        self.treeview_frame.grid(row=0, column=0, pady=10, padx=10, sticky="nsew")

        self.treeview = tk.ttk.Treeview(self.treeview_frame, columns=("Title", "Last Study", "Due", "Total"))
        self.treeview.grid(row=0, column=0, sticky="nsew")

        self.yscrollbar = tk.ttk.Scrollbar(self.treeview_frame, orient='vertical', command=self.treeview.yview)
        self.treeview.configure(yscrollcommand=self.yscrollbar.set)

        # self.treeview.grid(row=0, column=0, sticky="nsew")
        self.yscrollbar.grid(row=0, column=1, sticky='nse')
        self.yscrollbar.configure(command=self.treeview.yview)

        # Format columns
        # We set width as 0 because we will not use parent-children rows
        self.treeview.column("#0", width=0, minwidth=0)
        # self.treeview.column("#1", anchor="w")
        # self.treeview.column("#2", anchor="e")
        self.treeview.column("#1", anchor="w", width="235")
        self.treeview.column("#2", anchor="e", width="70")
        self.treeview.column("#3", anchor="e", width="70")
        self.treeview.column("#4", anchor="e", width="70")

        # Create headings to the columns
        self.treeview.heading("#0", text="")
        self.treeview.heading("#1", text="Title", anchor="w",)
        self.treeview.heading("#2", text="Last Study", anchor="e")
        self.treeview.heading("#3", text="Due", anchor="e")
        self.treeview.heading("#4", text="Total", anchor="e")

        self.add_data_to_treeview()

        # Select first row if there is any
        decks = self.controller.database_manager.decks
        if len(decks) > 0:
            self.treeview.selection_set(0)
            self.treeview.focus(0)

        # # Setup rename deck frame
        # self.rename_deck_frame = tk.LabelFrame(self, text="Rename selected deck")
        # self.deck_label = tk.Label(self.rename_deck_frame, text="Deck title: ")
        # self.deck_label.grid(row=0, column=0, sticky="w")
        # self.deck_title_textedit = tk.Entry(self.rename_deck_frame)
        # self.deck_title_textedit.insert(0, self.controller.deck.title)
        # self.deck_title_textedit.grid(row=0, column=1, sticky="nsew")
        # self.rename_deck_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        # self.rename_deck_frame.grid_columnconfigure(1, weight=1)
        # # self.rename_deck_frame.pack(side="top", fill="both", expand=True)

        # Setup buttons frame
        self.buttons_frame = tk.Frame(self)
        self.buttons_frame.grid(row=1, column=0, padx=10, pady=10, sticky="sew")

        self.open_deck_button = tk.Button(self.buttons_frame, text="Study", command=self.open_deck, width=9)
        self.rename_button = tk.Button(self.buttons_frame, text="Rename", command=self.rename_deck, width=9)
        self.delete_button = tk.Button(self.buttons_frame, text="Delete", command=self.delete_deck, width=9)
        self.new_deck_button = tk.Button(self.buttons_frame, text="New deck", command=self.new_deck, width=9)
        self.edit_deck_button = tk.Button(self.buttons_frame, text="Flashcards", command=self.edit_flashcards, width=9)

        # Place buttons
        self.open_deck_button.grid(row=0, column=1, padx=6, pady=10, sticky="nsew")
        self.edit_deck_button.grid(row=0, column=2, padx=6, pady=10, sticky="nsew")
        self.rename_button.grid(row=0, column=3, padx=6, pady=10, sticky="nsew")
        self.delete_button.grid(row=0, column=4, padx=6, pady=10, sticky="nsew")
        self.new_deck_button.grid(row=0, column=5, padx=6, pady=10, sticky="nsew")

        self.set_weights()

        # # Setup bottom frame
        # self.bottom_frame = tk.Frame(self)
        # self.bottom_frame.grid(row=1, column=0, columnspan=2, sticky="nsew")
        #
        # # This is required to center the button
        # self.bottom_frame.grid_columnconfigure(0, weight=1)
        #
        # self.go_back_button = tk.Button(self.bottom_frame, text="Go back", command=self.go_back)
        # self.go_back_button.grid(row=0, column=0, padx=10, pady=10)

    def set_weights(self):
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

    def new_deck(self):
        new_title = tkinter.simpledialog.askstring(title = "New deck", prompt = "Please enter a title for the new deck:", initialvalue="")
        if new_title is not None:
            new_title = new_title.strip()
            if len(new_title) > 0:
                new_title = new_title[:ManageDecksFrame.MAXIMUM_LENGTH_OF_DECK_TITLE]
                new_deck_id = self.controller.database_manager.add_new_deck_to_db(new_title, None)
                new_deck = Deck(title=new_title, deck_id=new_deck_id, last_study_datetime=None)
                self.controller.database_manager.decks.append(new_deck)
                # Set current deck when a new deck is added and count of decks was 0.
                if len(self.controller.database_manager.decks) == 1:
                    self.controller.database_manager.set_current_deck_if_possible()
                self.refresh_treeview()
                self.select_last_deck_in_treeview()
                self.offer_to_create_flashcards()
            else:
                tk.messagebox.showwarning("Info", "Title cannot be empty.")

    def offer_to_create_flashcards(self):
        deck = self.selected_deck()
        count_of_decks = len(self.controller.database_manager.decks)
        if (deck is not None) and (count_of_decks == 1):
            tk.messagebox.showwarning("Info", "Now you have a deck. Good job! To create some flashcards for this deck, you can click Flashcards button below.", icon="info")

    def rename_deck(self):
        deck = self.selected_deck()
        if deck is not None:
            new_title = tkinter.simpledialog.askstring(title = "Rename deck", prompt = "Please enter new title of the deck:", initialvalue=self.selected_deck_title())
            if new_title is not None:
                print(new_title)
                selected_index = self.selected_treeview_index()

                deck.title = new_title
                self.controller.database_manager.update_deck_in_db(deck.deck_id, deck.title, deck.last_study_datetime)

                self.refresh_treeview()
                self.treeview.selection_set(selected_index)
                self.treeview.focus(selected_index)
        else:
            tk.messagebox.showwarning("Info", "You should create a deck first.")

        # # Change value in treeview
        # count = self.selected_deck_flashcard_count
        # focused_index_string = str(self.selected_deck_index())
        # self.treeview.delete(self.selected_deck_index())
        # self.treeview.insert(parent='', index='end', iid=focused_index_string, text="", values=(new_title, count))
        # # self.treeview.insert("", str(focused)[1:], values=("", new_title))
        # # print("self.decks: ", self.decks)
        # # print("self.controller.decks: ", self.controller.decks)

    def refresh_treeview(self):
        self.remove_all_data_from_treeview()
        self.add_data_to_treeview()

    def remove_all_data_from_treeview(self):
        # self.treeview.delete(*self.treeview.get_children())
        for i in self.treeview.get_children():
            self.treeview.delete(i)

    def delete_deck(self):
        decks = self.controller.database_manager.decks
        if len(decks) > 0:
            deck = decks[self.selected_treeview_index()]
            flashcard_count = len(deck.flashcards)
            confirmation_message = "This deck will be deleted: " + deck.title + "\n\n"
            if flashcard_count == 0:
                confirmation_message += "It does not contain any flashcards."
            elif flashcard_count == 1:
                confirmation_message += "It contains one flashcard. It will be deleted with the deck."
            else:
                confirmation_message += "It contains " + str(flashcard_count) + " flashcards. They will be deleted with the deck."
            # Icons in messagebox: https://stackoverflow.com/a/59344478/3780985
            confirmation = tk.messagebox.askokcancel("Please confirm",
                                                    confirmation_message, icon="warning")
            if confirmation:
                self.controller.database_manager.delete_deck_from_db(deck.deck_id)
                self.controller.database_manager.decks.remove(deck)
                self.refresh_treeview()
                # Assign a new deck as current deck, if current deck has just been deleted.
                if self.controller.database_manager.deck.deck_id == deck.deck_id:
                    self.controller.database_manager.set_current_deck_if_possible()
        else:
            tk.messagebox.showwarning("Info", "You should create a deck first.")

    def edit_flashcards(self):
        deck = self.selected_deck()
        if deck is not None:
            self.controller.database_manager.deck = deck
            self.controller.show_manage_flashcards_frame()
        else:
            tk.messagebox.showwarning("Info", "You should create a deck first.")

    def open_deck(self):
        self.controller.open_deck(self.selected_treeview_index())
        # selected_deck = self.selected_deck()
        # if selected_deck is not None:
        #     count = len(selected_deck.flashcards)
        #     due_count = len(selected_deck.due_flashcards)
        #     if count > 0:
        #         if due_count > 0:
        #             self.controller.open_deck(self.selected_treeview_index(), show_only_due_flashcards=True)
        #         else:
        #             confirmation = tk.messagebox.askokcancel("No due flashcard",
        #                                                      "There is no due flashcard. Would you like to go over all of them?",
        #                                                      icon="question")
        #             if confirmation:
        #                 self.controller.open_deck(self.selected_treeview_index(), show_only_due_flashcards=False)
        #     else:
        #         tk.messagebox.showwarning("Info","This deck is empty. Please add some flashcards to it first by clicking Flashcards button below.")
        # else:
        #     tk.messagebox.showwarning("Info", "You should create a deck first.")

    def selected_treeview_index(self):
        selected_item = self.treeview.focus()
        # selected_item_dict = self.treeview.item(selected_item)
        index = self.treeview.index(selected_item)
        print("selected_deck_index: ", index)
        return index

    def selected_deck_title(self):
        selected_item = self.treeview.focus()
        selected_item_dict = self.treeview.item(selected_item)
        item_list = selected_item_dict["values"]
        title = item_list[0]
        print("title: ", title)
        return title

    def selected_deck(self):
        result = None
        decks = self.controller.database_manager.decks
        if len(decks) > 0:
            selected_deck = self.controller.database_manager.decks[self.selected_treeview_index()]
            print("selected_deck: ", selected_deck.title)
            print("selected_desk's flashcards:")
            for flashcard in selected_deck.flashcards:
                print(flashcard.flashcard_id, flashcard.deck_id, flashcard.question, flashcard.answer)
            result = selected_deck
        return result

    def selected_deck_flashcard_count(self):
        index = self.selected_treeview_index()
        count = len(self.controller.database_manager.decks[index].flashcards)
        return count

    def add_data_to_treeview(self):
        # Add data to the treeview
        decks = self.controller.database_manager.decks
        deck_count = len(decks)
        for index in range(deck_count):
            deck = decks[index]
            title = deck.title
            deck.set_due_flashcards(self.controller.database_manager)
            due_count = len(deck.due_flashcards)
            total_count = len(deck.flashcards)
            last_study = deck.get_last_study()
            self.treeview.insert(parent='', index='end', iid=index, text="", values=(title, last_study, due_count, total_count))

    def select_first_deck(self):
        if len(self.controller.database_manager.decks) > 0:
            self.treeview.selection_set(0)
            self.treeview.focus(0)

    def select_last_deck_in_treeview(self):
        # Select last flashcard item in treeview, i.e. give it focus
        decks = self.controller.database_manager.decks
        count = len(decks)
        if count > 0:
            self.treeview.selection_set(count - 1)
            self.treeview.focus(count - 1)

    def prepare_view(self):
        self.refresh_treeview()
        self.select_first_deck()
