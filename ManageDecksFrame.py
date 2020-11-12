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
        tk.Frame.__init__(self, parent)

        self.controller = controller

        # print("controller.winfo_height(): ", controller.winfo_height())
        # print("controller.winfo_width()", controller.winfo_width())
        # print("self.winfo_width(): ", self.winfo_width())

        # Setup select deck frame
        self.select_deck_frame = tk.LabelFrame(self, text="Select deck")
        self.select_deck_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Setup Treeview
        self.treeview = tk.ttk.Treeview(self.select_deck_frame, columns=("Title", "Flashcards"))

        # Define columns
        # self.treeview['columns'] = ("Question", "Answer")

        # Format columns
        # We set width as 0 because we will not use parent-children rows
        self.treeview.column("#0", width=0, minwidth=0)
        self.treeview.column("#1", anchor="w", width="240")
        self.treeview.column("#2", anchor="e", width="70")

        # Create headings to the columns
        self.treeview.heading("#0", text="")
        self.treeview.heading("#1", text="Title", anchor="w",)
        self.treeview.heading("#2", text="Flashcards", anchor="e")

        self.add_data_to_treeview()

        self.treeview.grid(padx=10, pady=10, sticky="nsew")

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
        self.buttons_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        self.open_deck_button = tk.Button(self.buttons_frame, text="Open deck", command=self.open_deck)
        self.rename_button = tk.Button(self.buttons_frame, text="Rename deck", command=self.rename_deck)
        self.delete_button = tk.Button(self.buttons_frame, text="Delete deck", command=self.delete_deck)
        self.new_deck_button = tk.Button(self.buttons_frame, text="New deck", command=self.new_deck)
        self.edit_deck_button = tk.Button(self.buttons_frame, text="Edit Flashcards", command=self.edit_flashcards)

        # Place buttons
        self.open_deck_button.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.edit_deck_button.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self.rename_button.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        self.delete_button.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")
        self.new_deck_button.grid(row=4, column=0, padx=10, pady=10, sticky="nsew")

        self.grid_rowconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)

        # Setup bottom frame
        self.bottom_frame = tk.Frame(self)
        self.bottom_frame.grid(row=1, column=0, columnspan=2, sticky="nsew")

        # This is required to center the button
        self.bottom_frame.grid_columnconfigure(0, weight=1)

        self.go_back_button = tk.Button(self.bottom_frame, text="Go back", command=self.go_back)
        self.go_back_button.grid(row=0, column=0, padx=10, pady=10)

    def new_deck(self):
        new_title = tkinter.simpledialog.askstring(title = "New deck", prompt = "Please enter the title of the new deck:", initialvalue="")
        new_title = new_title.strip()
        if len(new_title) > 0:
            new_deck_id = self.controller.database_manager.add_new_deck_to_db(new_title)
            new_deck = Deck(title=new_title, deck_id=new_deck_id)
            self.controller.database_manager.decks.append(new_deck)
            self.refresh_treeview()
        else:
            tk.messagebox.showwarning("Info", "Title cannot be empty.")

    def rename_deck(self):
        new_title = tkinter.simpledialog.askstring(title = "Rename deck", prompt = "Please enter new title of the deck:", initialvalue=self.selected_deck_title())
        if new_title is not None:
            print(new_title)
            selected_index = self.selected_deck_index()
            self.selected_deck().title = new_title
            self.refresh_treeview()
            self.treeview.selection_set(selected_index)
            self.treeview.focus(selected_index)

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
        pass

    def edit_flashcards(self):
        self.controller.database_manager.deck = self.selected_deck()
        self.controller.manage_flashcards()

    def open_deck(self):
        selected_deck = self.selected_deck()
        count = len(selected_deck.flashcards)
        if count > 0:
            self.controller.open_deck(self.selected_deck_index())
        else:
            tk.messagebox.showwarning("Info","This deck is empty. Please add some flashcards to it first by clicking 'Edit Flashcards' button.")

    def go_back(self):
        self.controller.show_frame("StudyFrame")

    def selected_deck_index(self):
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
        selected_deck = self.controller.database_manager.decks[self.selected_deck_index()]
        print("selected_deck: ", selected_deck.title)
        print("selected_desk's flashcards:")
        for flashcard in selected_deck.flashcards:
            print(flashcard.flashcard_id, flashcard.deck_id, flashcard.question, flashcard.answer)
        return selected_deck

    def selected_deck_flashcard_count(self):
        index = self.selected_deck_index()
        count = len(self.controller.database_manager.decks[index].flashcards)
        return count

    def add_data_to_treeview(self):
        # Add data to the treeview
        decks = self.controller.database_manager.decks
        deck_count = len(decks)
        for index in range(deck_count):
            title = decks[index].title
            count = len(decks[index].flashcards)
            self.treeview.insert(parent='', index='end', iid=index, text="", values=(title, count))
