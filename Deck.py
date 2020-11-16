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

from datetime import datetime

from Flashcard import Flashcard

class Deck:
    def __init__(self, deck_id, title, last_study_datetime=None):
        self.deck_id = deck_id
        self.title = title
        self.flashcards: [Flashcard] = []
        self.due_flashcards: [Flashcard] = []
        # last_study_datetime will hold the last study date and time. For compatibility with SQlite3,
        # ISO8601 string format will be used as follows:
        # YYYY-MM-DD HH:MM:SS.SSS
        self.last_study_datetime = last_study_datetime

    def truncated_title(self):
        truncated_deck_title = self.title[:20]
        if len(self.title) > 20:
            truncated_deck_title += "..."
        return truncated_deck_title

    def record_last_study_datetime(self, database_manager):
        database_manager.update_deck_in_db(self.deck_id, self.title, self.last_study_datetime)

    def set_last_study(self, database_manager):
        self.last_study_datetime = datetime.now()
        self.record_last_study_datetime(database_manager)

    def get_last_study(self):
        # last_study_datetime_string = self.last_study_datetime.strftime("%m/%d/%Y, %H:%M")
        last_study_datetime_string = ""
        if self.last_study_datetime is not None:
            last_study_datetime_string = self.last_study_datetime.strftime("%m/%d/%Y")
        return last_study_datetime_string

    def set_due_flashcards(self, database_manager):
        database_manager.load_due_flashcards(self)