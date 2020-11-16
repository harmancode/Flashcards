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

import datetime
# from DatabaseManager import DatabaseManager


class Flashcard:

    def __init__(self, flashcard_id, deck_id, question, answer, inter_repetition_interval=0, easiness_factor=0, repetition_number=0):
        self.flashcard_id = flashcard_id
        self.deck_id = deck_id
        self.question = question
        self.answer = answer
        self.last_study_date: datetime.datetime = None

        # Use due_date attribute to determine due flashcards that user should work on
        today = datetime.datetime.today()
        self.due_date_string: today.strftime('%Y-%m-%d')

        self.inter_repetition_interval = inter_repetition_interval
        self.easiness_factor = easiness_factor
        self.repetition_number = repetition_number

        # For SM-2 Algorithm
        self.inter_repetition_interval = 0  # in days
        self.easiness_factor = 0  # from 0 (hardest) to 4 (easiest)
        self.repetition_number = 0  # how many times user solved this flashcard?

    def set_inter_repetition_interval(self, grade):
        # Parameter grade is a number between 0 (hardest) and 4 (easiest), indicating the difficulty
        # level when solving the flashcard.
        # Based on SM-2 Algorithm
        # Explained here: https://en.wikipedia.org/wiki/SuperMemo#Description_of_SM-2_algorithm
        if self.repetition_number == 0:
            self.inter_repetition_interval = 1
        elif self.repetition_number == 1:
            self.inter_repetition_interval = 6
        elif self.repetition_number > 1:
            self.inter_repetition_interval = self.inter_repetition_interval * self.easiness_factor
        self.repetition_number += 1
        self.easiness_factor = self.easiness_factor + (0.1 - (4 - grade) * (0.08 + (4 - grade) * 0.02))
        if grade < 2:
            # This indicates incorrect answer
            self.repetition_number = 0
            self.inter_repetition_interval = 1
        if self.easiness_factor < 1.3:
            self.easiness_factor = 1.3

    def set_last_study_date(self, database_manager):
        self.last_study_datetime = datetime.datetime.now()
        database_manager.update_flashcard_in_db(self.flashcard_id, self.question, self.answer, self.last_study_date,
                                                self.due_date)
    def set_due_date(self):
        due_date = datetime.datetime.now() + datetime.timedelta(self.inter_repetition_interval)
        # today = datetime.datetime.today()
        self.due_date_string = due_date.strftime('%Y-%m-%d')

    # Process user's answer to a flashcard, and set the due date as the final result
    def process_answer(self, grade, database_manager):
        self.last_study_date = datetime.datetime.now()
        self.set_inter_repetition_interval(grade)
        self.set_due_date()
        database_manager.update_flashcard_in_db(self.flashcard_id,
                                                self.question,
                                                self.answer,
                                                self.last_study_date,
                                                self.due_date_string,
                                                self.inter_repetition_interval,
                                                self.easiness_factor,
                                                self.repetition_number)

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
