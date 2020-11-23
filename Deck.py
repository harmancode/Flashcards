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

from datetime import datetime
from typing import Optional

from Flashcard import Flashcard


class Deck:
    MAXIMUM_LENGTH_OF_DECK_TITLE = 250
    MAXIMUM_LENGTH_OF_DECK_SHORT_TITLE = 20

    def __init__(self, deck_id, title, last_study_datetime: Optional[datetime] = None):
        """
        Deck class represents every deck in the Program, that holds flashcards. Decks are simply sets of flashcards.
        :param int deck_id: Unique identifer for the Deck. Provided by the database.
        :param str title: Title of the deck. Max length is kept in a class constant: MAXIMUM_LENGTH_OF_DECK_TITLE
        :param Optional[datetime] last_study_datetime: When this deck was studied for the last time. It can be None.
        """
        self.deck_id = deck_id
        self.title = title
        self.flashcards: [Flashcard] = []
        self.due_flashcards: [Flashcard] = []
        # last_study_datetime will hold the last study date and time. For compatibility with SQlite3,
        # ISO8601 string format will be used as follows:
        # YYYY-MM-DD HH:MM:SS.SSS
        self.last_study_datetime = last_study_datetime

    def get_truncated_title(self) -> str:
        """
        Truncates title according to the Deck.MAXIMUM_LENGTH_OF_DECK_SHORT_TITLE value. It is used where limited space is
        available on the view.
        :return: Title of the deck truncated according to the Deck.MAXIMUM_LENGTH_OF_DECK_SHORT_TITLE value
        :rtype: str
        """
        truncated_deck_title = self.title[:Deck.MAXIMUM_LENGTH_OF_DECK_SHORT_TITLE]
        if len(self.title) > Deck.MAXIMUM_LENGTH_OF_DECK_SHORT_TITLE:
            truncated_deck_title += "..."
        return truncated_deck_title

    def record_last_study_datetime(self, database_manager) -> None:
        """
        Update deck's last.study_datetime record in the database.
        :param database_manager: DatabaseManager object kept in the main controller (Program)
        :type database_manager: DatabaseManager
        """
        database_manager.update_deck_in_db(self.deck_id, self.title, self.last_study_datetime)

    def set_last_study_datetime(self, database_manager) -> None:
        """
        Updates deck's last_study_datetime attribute in memory and in database.
        :param database_manager: DatabaseManager object kept in the main controller (Program)
        :type database_manager: DatabaseManager
        """
        self.last_study_datetime = datetime.now()
        self.record_last_study_datetime(database_manager)

    def get_last_study_datetime_as_formatted_string(self) -> str:
        """
        See return statement.
        :return: last_study_datetime attribute as string in "%m/%d/%Y" date string format
        :rtype: str
        """
        # last_study_datetime_string = self.last_study_datetime.strftime("%m/%d/%Y, %H:%M")
        last_study_datetime_string = ""
        if self.last_study_datetime is not None:
            last_study_datetime_string = self.last_study_datetime.strftime("%m/%d/%Y")
        return last_study_datetime_string

    def set_due_flashcards(self, database_manager) -> None:
        """
        Loads due flashcards from the database and puts them in self.due_flashcards list attribute.
        :param database_manager: DatabaseManager object kept in the main controller (Program)
        :type database_manager: DatabaseManager
        """
        database_manager.load_due_flashcards(self)
