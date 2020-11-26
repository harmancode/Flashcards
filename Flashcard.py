#   Program FlashCards
#
#   Copyright 2020 Ertugrul Harman
#
#       E-mail  : harmancode@gmail.com
#       Twitter : https://twitter.com/harmancode
#       Web     : https://harman.page
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


class Flashcard:
    MAX_LENGTH_OF_QUESTION = 500
    MAX_LENGTH_OF_ANSWER = 500

    def __init__(self,
                 flashcard_id,
                 deck_id,
                 question,
                 answer,
                 last_study_date=None,
                 due_date_string="",
                 inter_repetition_interval=0,
                 easiness_factor=0.0,
                 repetition_number=0):
        """
        Flashcard class represents every flashcard item in a deck.
        :param int flashcard_id: Unique identifier. Provided by the database. Minimum value is 0.
        :param int deck_id: Unique identifier. Provided by the database. Minimum value is 0.
        :param str question: Front side of the flashcard. Usually contains the question.
        Length between 0 and MAX_LENGTH_OF_QUESTION
        :param str answer: The bask side of the flashcard. Usually contains the answer of the question.
        Length between 0 and MAX_LENGTH_OF_ANSWER.
        :param datetime.datetime last_study_date: When this flashcard last studied.
        :param str due_date_string: Due date of this flashcard as str.
        :param int inter_repetition_interval: How many days program should wait before setting this flahcard due again.
        Minimum value is 0.
        :param float easiness_factor: Calculated based on the answers of the user by using the spaced-repetition
        algorithm.
        :param int repetition_number: How many times user has studied this flashcard. Minimum value is 0.
        """

        self.flashcard_id = flashcard_id
        self.deck_id = deck_id
        self.question = question
        self.answer = answer
        self.last_study_date: datetime.datetime = last_study_date

        # Use due_date attribute to determine due flashcards that user should work on
        if due_date_string == "":
            # There is no due date passed. Set it as today. Otherwise this flashcard won't be included in study
            # sessions.
            today = datetime.datetime.today()
            self.due_date_string = today.strftime('%Y-%m-%d')
        else:
            # There is a due date passed. Assign it.
            self.due_date_string = due_date_string

        # For SM-2 Algorithm
        self.inter_repetition_interval = inter_repetition_interval      # in days
        self.easiness_factor = easiness_factor                          # from 0 (hardest) to 4 (easiest)
        self.repetition_number = repetition_number                      # how many times user solved this flashcard?

    def set_inter_repetition_interval(self, grade) -> None:
        """
        Parameter grade is a number between 0 (hardest) and 4 (easiest), indicating the difficulty
        level when solving the flashcard.
        Based on SM-2 Algorithm
        Explained here: https://en.wikipedia.org/wiki/SuperMemo#Description_of_SM-2_algorithm
        :param int grade: Between 0 and 4
        """

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
        # DEBUG
        # print("Flashcard's new internal values:")
        # print("repetition_number: ", self.repetition_number)
        # print("inter_repetition_interval: ", self.inter_repetition_interval)
        # print("easiness_factor: ", self.easiness_factor)

    def set_last_study_date(self, database_manager) -> None:
        """
        Set the self.last_study_datetime property and save to the database.
        :param database_manager:
        """
        self.last_study_datetime = datetime.datetime.now()
        database_manager.update_flashcard_in_db(flashcard_id=self.flashcard_id,
                                                question=self.question,
                                                answer=self.answer,
                                                last_study_date=self.last_study_date,
                                                due_date_string=self.due_date_string,
                                                inter_repetition_interval=self.inter_repetition_interval,
                                                easiness_factor=self.easiness_factor,
                                                repetition_number=self.repetition_number)

    def set_due_date(self) -> None:
        """
        Set self.due_date_string attribute by adding the interval calculated by spaced-repetition algorithm.
        """
        due_date = datetime.datetime.now() + datetime.timedelta(self.inter_repetition_interval)
        # today = datetime.datetime.today()
        self.due_date_string = due_date.strftime('%Y-%m-%d')
        # DEBUG
        # print("Flashcard's new due date: ", self.due_date_string)

    def process_answer(self, grade, database_manager) -> None:
        """
        Process user's answer to a flashcard, and set the due date as the final result.
        Update flashcard data in the database.
        :param int grade: Between 0 and 4
        :param DatabaseManager database_manager: DatabaseManager instance kept in the main controller (Program)
        """
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
