try:
    import tkinter as tk  # python 3
    from tkinter import font as tkfont  # python 3
except ImportError:
    import Tkinter as tk  # python 2
    import tkFont as tkfont  # python 2

from Deck import Deck
from Flashcard import Flashcard


# Inherit from tk.Frame
class StudyFrame(tk.Frame):
    def __init__(self, parent, controller):
        # Initialize super class
        tk.Frame.__init__(self, parent)

        # Assign passed controller attribute to the class attribute
        self.controller = controller

        # label = tk.Label(self, text="This is page 1", font=controller.title_font)
        # label.pack(side="top", fill="x", pady=10)
        # button = tk.Button(self, text="Go to the start page",
        #                    command=lambda: controller.show_frame("StartPage"))
        # button.pack()

        # Holds the current deck's index in the decks list
        self.deck_index = int()

        # Holds the current flashcard's index in the flashcards list
        self.flashcard_index = int()

        # Holds if card is flipped
        self.flipped = False

        # When object is initialized there is not any deck selected. Therefore deck index and flashcard index will be
        # -1.
        self.deck_index = -1
        self.flashcard_index = -1

        # self.decks holds the Deck list
        self.decks = controller.decks

        # self.deck holds the current deck. As the main window is now being initialized, there is no selected deck.
        self.deck: Deck = None

        # self.flashcards will be a list holding the flashcards of the current deck.
        self.flashcards = [Flashcard]

        # As there is not any selected Deck, current flashcard will be None.
        self.flashcard: Flashcard = None

        # Create two frames, top and bottom
        self.top_frame = tk.Frame(self)
        self.bottom_frame = tk.Frame(self)
        self.status_frame = tk.Frame(self)

        self.top_frame.grid()
        self.bottom_frame.grid()
        self.status_frame.grid(sticky="we")

        self.index_card_image = tk.PhotoImage(master=self.top_frame, file='image/index_card.gif')
        self.flashcard_label = tk.Label(self.top_frame, text="Load a flashcard", wraplength=350,
                                        font=("Arial", 14, "bold"),
                                        image=self.index_card_image, compound=tk.CENTER)
        self.flashcard_label.grid(row=0, column=0, rowspan=6)

        # Create three buttons for the bottom frame
        self.previous_button = tk.ttk.Button(self.bottom_frame, text='Previous',
                                             command=self.show_previous_flashcard)
        self.show_hide_button = tk.ttk.Button(self.bottom_frame, text='Flip', command=self.flip)
        self.next_button = tk.ttk.Button(self.bottom_frame, text='Next', command=self.show_next_flashcard)

        # self.show_hide_button.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

        # self.previous_button.pack(side='left')
        self.previous_button.grid(row=0, column=0, padx=10, pady=5)
        self.show_hide_button.grid(row=0, column=1, padx=10, pady=5)
        self.next_button.grid(row=0, column=2, padx=10, pady=5)

        # Create "Deck Table" as a TreeView
        # This object will be used to edit flashcards in the deck
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
        status_bar_text = self.status_bar_text()
        print("status_bar_text: ", status_bar_text)
        self.status_bar = tk.ttk.Label(self.status_frame, text=status_bar_text, border=1, relief=tk.SUNKEN)
        self.status_bar.pack(fill=tk.X)
        # self.status_bar = tkinter.ttk.Label(self.status_frame, text=status_bar_text, border=1, relief=tkinter.SUNKEN)
        # self.status_bar.grid(row=1, column=0, columnspan=3)

        # DEBUG: Load deck
        self.load_deck(0)

    def load_deck(self, index):
        self.deck_index = index
        self.deck = self.decks[self.deck_index]
        self.controller.deck = self.deck
        self.flashcard_index = 0
        self.flashcards = self.deck.flashcards
        self.flashcard = self.flashcards[self.flashcard_index]
        self.load_flashcard()
        self.set_button_status()
        print("deck is loaded. deck index: ", self.deck_index, " deck title: ", self.deck.title)
        print("first flashcard loaded. index: ", self.flashcard_index, " question: ", self.flashcard.question)

    def load_flashcard(self):
        print("load_flashcard")
        print("self.flashcard_index: ", self.flashcard_index)
        self.flashcard = self.flashcards[self.flashcard_index]
        if self.flipped:
            self.flashcard_label.config(fg="green")
            self.flashcard_label.config(text=self.flashcard.answer)
        else:
            self.flashcard_label.config(fg="red")
            self.flashcard_label.config(text=self.flashcard.question)
        self.set_status_bar_text()

    def show_next_flashcard(self):
        self.flipped = False
        self.flashcard_index += 1
        self.load_flashcard()
        print("self.flashcard_index: ", self.flashcard_index, "; len(self.flashcards): ", len(self.flashcards))
        self.set_button_status()

    def show_previous_flashcard(self):
        if self.flashcard_index != 0:
            self.flipped = False
            self.flashcard_index -= 1
            self.load_flashcard()
            print("self.flashcard_index: ", self.flashcard_index, "; len(self.flashcards): ", len(self.flashcards))
            self.set_button_status()

    def set_button_status(self):
        if self.flashcard_index == 0:
            self.previous_button.config(state='disabled')
        else:
            self.previous_button.config(state='enabled')
        if self.flashcard_index == len(self.flashcards) - 1:
            self.next_button.config(state='disabled')
        else:
            self.next_button.config(state='enabled')

    def flip(self):
        self.flipped = not self.flipped
        self.load_flashcard()

    def set_status_bar_text(self):
        self.status_bar.config(text=self.status_bar_text())

    def status_bar_text(self):
        if self.deck is None:
            return "Please load a deck."
        else:
            text = "Deck: " + self.deck.title + " | Flashcard " + str(self.flashcard_index + 1) + " out of " + str(
                len(self.flashcards))
            return text
