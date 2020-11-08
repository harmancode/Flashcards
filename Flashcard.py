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

class Flashcard:

    def __init__(self, question, answer, parent_deck):
        self.question = question
        self.answer = answer
        self.parent_deck = parent_deck

    # def get_question(self):
    #     return self._Flashcard__question
    #
    # def get_answer(self):
    #     return self.__answer
    #
    # def get_parent_deck(self):
    #     return self.__parent_deck
    #
    # def set_question(self, question):
    #     self.__question = question
    #
    # def set_answer(self, answer):
    #     self.__answer = answer
    #
    # def set_parent_deck(self, parent_deck):
    #     self.__parent_deck = parent_deck
