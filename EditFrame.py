try:
    import tkinter as tk  # python 3
    from tkinter import font as tkfont  # python 3
except ImportError:
    import Tkinter as tk  # python 2
    import tkFont as tkfont  # python 2


class EditFrame(tk.Frame):

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
        self.treeview = tk.ttk.Treeview(self.select_deck_frame, columns=("Question", "Answer"))

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

        # Add data to the treeview
        decks = self.controller.decks
        deck_count = len(decks)
        for index in range(deck_count):
            title = decks[index].title
            count = len(decks[index].flashcards)
            self.treeview.insert(parent='', index='end', iid=index, text="", values=(title, count))

        self.treeview.grid(padx=10, pady=10, sticky="nsew")

        # Select first row if there is any
        if deck_count > 0:
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
        pass

    def rename_deck(self):
        pass

    def delete_deck(self):
        pass

    def edit_flashcards(self):
        pass

    def open_deck(self):
        pass

    def go_back(self):
        self.controller.show_frame("StudyFrame")
