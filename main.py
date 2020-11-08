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

from Program import Program
from Flashcard import Flashcard
from Deck import Deck

def main():
    decks = create_dummy_deck()

    # Initialize Program() object from Program module
    # Create window variable and set its value as the initialized Program object
    program = Program(decks)

def create_dummy_deck():
    deck = Deck("USA capital cities")
    flashcards = create_dummy_flashcards(deck)
    deck.flashcards = flashcards
    decks = [deck]
    return decks

def create_dummy_flashcards(deck):
    flashcard1 = Flashcard("Capital of Texas?", "Austin", deck)
    flashcard2 = Flashcard("Capital of California?", "Sacramento", deck)
    flashcard3 = Flashcard("Capital of Washington?", "Olympia", deck)
    flashcards = [flashcard1, flashcard2, flashcard3]
    return flashcards

# Call the main function
main()