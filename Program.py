#   Program FlashCards
#
#   Copyright 2020 Ertugrul Harman
#
#   Website     : harman.page
#   Email (1)   : dev@harman.page
#   Email (2)   : ertugrulharman@gmail.com
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

import tkinter
import tkinter.ttk
from Flashcard import Flashcard
from Deck import Deck


class Program:
    # Holds the current deck's index in the decks list
    deck_index = int()

    # Holds the current flashcard's index in the flashcards list
    flashcard_index = int()

    # Holds if card is flipped
    flipped = False

    def __init__(self, decks):

        print("MainWindow initialization begins")

        # When object is initialized there is not any deck selected. Therefore deck index and flashcard index will be -1.
        self.deck_index = -1
        self.flashcard_index = -1

        # self.decks holds the Deck list
        self.decks = decks

        # self.deck holds the current deck. As the main window is now being initialized, there is no selected deck.
        self.deck: Deck = None

        # self.flashcards will be a list holding the flashcards of the current deck.
        self.flashcards = [Flashcard]

        # As there is not any selected Deck, current flashcard will be None.
        self.flashcard: Flashcard = None

        print("MainWindow initialized")

        # Create the main window widget
        self.window = tkinter.Tk()

        self.center_window()

        # Set the app icon
        # Used https://www.favicon-generator.org/
        self.window.iconbitmap("ico/favicon.ico")

        # Set title of the main window
        self.window.title("Flashcards")

        # Disable resize on main window
        self.window.resizable(False, False)

        # Create two frames, top and bottom
        self.top_frame = tkinter.Frame(self.window)
        self.bottom_frame = tkinter.Frame(self.window)
        self.status_frame = tkinter.Frame(self.window)

        index_card_image = tkinter.PhotoImage(file='image/index_card.gif')
        self.card_front = tkinter.Label(self.top_frame, text="Load a flashcard", wraplength=350,
                                        font=("Arial", 14, "bold"),
                                        image=index_card_image, compound=tkinter.CENTER)
        self.card_front.grid(row=0, column=0, rowspan=6)

        # Create three buttons for the bottom frame
        self.previous_button = tkinter.ttk.Button(self.bottom_frame, text='Previous',
                                                  command=self.show_previous_flashcard)
        self.show_hide_button = tkinter.ttk.Button(self.bottom_frame, text='Flip', command=self.flip)
        self.next_button = tkinter.ttk.Button(self.bottom_frame, text='Next', command=self.show_next_flashcard)

        # self.show_hide_button.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

        # self.previous_button.pack(side='left')
        self.previous_button.grid(row=0, column=0, padx=10, pady=5)
        self.show_hide_button.grid(row=0, column=1, padx=10, pady=5)
        self.next_button.grid(row=0, column=2, padx=10, pady=5)

        # Create "Deck Table" as a TreeView
        # This object will be used to edit flashcards in the deck
        self.table = tkinter.ttk.Treeview(self.window, columns=["Question", "Answer"])

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
        self.status_bar = tkinter.ttk.Label(self.status_frame, text=status_bar_text, border=1, relief=tkinter.SUNKEN)
        self.status_bar.pack(fill=tkinter.X)
        # self.status_bar = tkinter.ttk.Label(self.status_frame, text=status_bar_text, border=1, relief=tkinter.SUNKEN)
        # self.status_bar.grid(row=1, column=0, columnspan=3)

        self.top_frame.grid()
        self.bottom_frame.grid()
        self.status_frame.grid(sticky="we")

        # Create menu bar
        menubar = tkinter.Menu(self.window)
        self.window.config(menu=menubar)

        # Create Decks menu
        decks_menu = tkinter.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Deck", menu=decks_menu)

        decks_menu.add_command(label="New deck...", command=self.new_deck)
        decks_menu.add_command(label="Open a deck...", command=self.open_deck)
        decks_menu.add_separator()
        decks_menu.add_command(label="Quit", command=self.open_deck)

        # Create Flashcard menu
        flashcard_menu = tkinter.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Flashcard", menu=flashcard_menu)
        flashcard_menu.add_command(label="Add new flashcard...", command=self.open_deck)
        flashcard_menu.add_command(label="Change this question...", command=self.new_deck)
        flashcard_menu.add_command(label="Change this answer...", command=self.new_deck)
        flashcard_menu.add_command(label="Remove from deck...", command=self.new_deck)

        # Create About menu
        help_menu = tkinter.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.new_deck)

        # DEBUG: Load deck
        self.load_deck(0)

        # Enter the tkinter main loop
        tkinter.mainloop()

    def load_deck(self, index):
        self.deck_index = index
        self.deck = self.decks[self.deck_index]
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
            self.card_front.config(fg="green")
            self.card_front.config(text=self.flashcard.answer)
        else:
            self.card_front.config(fg="red")
            self.card_front.config(text=self.flashcard.question)
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

    def center_window(self):
        # self.window.update()

        # print(self.window.winfo_width())
        # print(self.window.winfo_height())
        #
        # print(self.window.winfo_reqwidth())
        # print(self.window.winfo_reqheight())

        # window_width = 483
        # window_height = 370

        window_width = 483
        window_height = 420

        # print(self.window.winfo_width())
        # print(self.window.winfo_height())

        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()

        # print(screen_width)
        # print(screen_height)

        x_cordinate = int((screen_width / 2) - (window_width / 2))
        y_cordinate = int((screen_height / 2) - (window_height / 2))

        self.window.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))

    def new_deck(self):
        pass

    def open_deck(self):
        pass

    def hide_all_frames(self):
        # Loop through all the children and delete them
        for widget in self.top_frame.winfo_children():
            widget.destroy()
        for widget in self.bottom_frame.winfo_children():
            widget.destroy()
        for widget in self.status_bar.winfo_children():
            widget.destroy()

