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


import sqlite3
import os
from datetime import datetime

from Deck import Deck
from Flashcard import Flashcard


class DatabaseManager:
    DB_PATH = "Flashcards.db"

    def __init__(self):

        # Initialize a single sqlite3 connection. One and only one initialization.
        self.db_connection: sqlite3.Connection = None

        # Initialize a single sqlite3 connection cursor. One and only one initialization.
        self.cursor: sqlite3.Cursor = None

        # Check if database exists. If it does not, create.
        self.provide_db()

        # List of decks. It will be used everywhere in the Program for consistency.
        self.decks: [Deck.Deck] = []

        # Current deck. It will be used everywhere in the Program for consistency.
        self.deck: Deck.Deck = None

        # Flag to check if db is open or not
        self.is_database_open = False

        # Load all decks when Program starts
        self.load_all_decks()

    def open_db(self) -> None:
        """
        Set connection and cursor attributes for database access.
        """
        try:
            self.db_connection = sqlite3.connect(DatabaseManager.DB_PATH,
                                                 detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
            self.cursor = self.db_connection.cursor()
            self.is_database_open = True
            # print("SQLite connection established.")
        except sqlite3.Error as error:
            print("Error while opening database: ", error)

    def close_db(self) -> None:
        """
        Commit changes to the database, close the cursor, and the connection.
        """
        if self.is_database_open:
            try:
                self.db_connection.commit()
                self.cursor.close()
                self.db_connection.close()
                self.is_database_open = False
            except sqlite3.ProgrammingError as programming_error:
                print("Database is probably already closed: ", programming_error)
            except sqlite3.error as error:
                print("Error in closing database: ", error)
            # print("SQLite connection closed.")

    def provide_db(self) -> None:
        """
        Check if database exists. If it does not, create.
        """
        should_create_tables = False
        if not os.path.exists(DatabaseManager.DB_PATH):
            # TODO: Find a better way to check if this is a valid database.
            should_create_tables = True
        try:
            self.open_db()
            # self.print_db_version()
            if should_create_tables:
                self.create_tables()
            self.close_db()
        except sqlite3.Error as error:
            print("Error while connecting to sqlite", error)
        finally:
            if self.db_connection:
                self.db_connection.close()
            # print("SQLite connection closed.")

    def create_tables(self) -> None:
        """
        Create SQLite tables in database
        """
        try:
            cursor = self.db_connection.cursor()

            cursor.execute("""
            CREATE TABLE IF NOT EXISTS deck (
            deck_id INTEGER PRIMARY KEY, 
            title TEXT NOT NULL, 
            last_study_datetime timestamp ) 
            """)

            cursor.execute("""
            CREATE TABLE IF NOT EXISTS flashcard (
            flashcard_id INTEGER PRIMARY KEY, 
            deck_id INTEGER NOT NULL, 
            question TEXT NOT NULL, 
            answer TEXT NOT NULL,
            last_study_date timestamp, 
            due_date_string TEXT,
            inter_repetition_interval INTEGER,
            easiness_factor REAL,
            repetition_number INTEGER, 
            FOREIGN KEY (deck_id) REFERENCES deck (deck_id) )
            """)

            # print("SQLite tables have been created.")

        except sqlite3.Error as error:
            print("Error while creating tables", error)

    def print_db_version(self) -> None:
        """
        Print database version for debugging.
        """
        if self.cursor is not None:
            sqlite_select_query = "select sqlite_version();"
            self.cursor.execute(sqlite_select_query)
            record = self.cursor.fetchall()
            print("SQLite Database Version is: ", record)
        else:
            print("DEBUG: print_db_version failed because self.cursor is None.")

    def add_new_deck_to_db(self, deck_title, last_study_datetime=None) -> int:
        """
        Adds a new deck data to the database.
        :param deck_title: Will be used as deck.title
        :type deck_title: str
        :param last_study_datetime: Will be used as  deck.last_study_datetime. Shows when deck was studied last time.
        :type last_study_datetime: datetime
        :return: Will be used as deck.deck_id
        :rtype: int
        """
        self.open_db()
        deck_row_tuple = (deck_title, last_study_datetime)
        # deck_id will be added by SQLite automatically because it is defined as INTEGER PRIMARY KEY.
        # For more info: https://www.sqlite.org/autoinc.html
        sql = ''' INSERT INTO deck(title, last_study_datetime)
                      VALUES(?, ?) '''
        self.cursor.execute(sql, deck_row_tuple)
        self.close_db()
        return self.cursor.lastrowid

    def add_new_flashcard_to_db(self, deck_id, question, answer, last_study_date, due_date_string) -> int:
        """
        Adds a new flashcard data to the database.
        :param deck_id: Flashcard's parent deck's deck.id
        :type deck_id: int
        :param question: Flashcard's question, i.e. front side text
        :type question: str
        :param answer: Flashcard's answer, i.e. back side text
        :type answer: str
        :param last_study_date: Will be used as flashcard's last_study_date property
        :type last_study_date: datetime
        :param due_date_string: When this flashcard will be due. As strftime('%Y-%m-%d').
        :type due_date_string: str
        :return: flashcard's flashcard_id
        :rtype: int
        """
        self.open_db()
        inter_repetition_interval = 0
        easiness_factor = 0
        repetition_number = 0
        flashcard_row_tuple = (deck_id, question, answer, last_study_date, due_date_string, inter_repetition_interval,
                               easiness_factor, repetition_number)
        sql = ''' INSERT INTO flashcard(deck_id, question, answer, last_study_date, due_date_string, 
                                inter_repetition_interval, easiness_factor, repetition_number)
                      VALUES(?,?,?,?,?,?,?,?) '''
        self.cursor.execute(sql, flashcard_row_tuple)
        self.close_db()

        # self.print_all_flashcards()

        return self.cursor.lastrowid

    def load_all_decks(self) -> None:
        """
        Load all decks from database during initialization, so that Program can use this data.
        """
        # print()
        # print("load_all_decks:")
        self.open_db()
        self.cursor.execute("SELECT * FROM deck")
        temp_decks = self.cursor.fetchall()
        self.decks = []
        for deck in temp_decks:
            deck_id = deck[0]
            deck_title = deck[1]
            last_study_datetime = deck[2]
            # print("Loaded deck ID:", deck_id, "title:", deck_title, "Last study:", deck[2])
            deck = Deck(deck_id, deck_title, last_study_datetime)
            self.decks.append(deck)
            self.load_flashcards(deck)
        self.close_db()
        if len(self.decks) > 0:
            self.load_deck(0)
        # print()

    def load_deck(self, deck_index: int) -> None:
        """
        Load all flashcards of the deck.
        :param deck_index: deck's index in self.decks list
        :type deck_index: int
        """
        self.deck = self.decks[deck_index]
        self.load_flashcards(self.deck)

    def load_flashcards(self, deck: Deck) -> None:
        """
        Load flashcards of the given deck from the database, and add them to the self.flashcards list of each deck
        that is a member of self.decks list.
        :param deck: Parent of the flashcards to be loaded
        :type deck: Deck object
        """
        # self.print_all_flashcards()
        self.open_db()
        deck.flashcards = []
        parameter = (deck.deck_id,)
        results = self.cursor.execute("SELECT * FROM flashcard WHERE deck_id == ?", parameter)
        # print("Deck title: ", deck.title, "Last study: ", deck.last_study_datetime)
        # print("Loaded flashcards: \n", results)
        for result in results:
            # print(result)
            flashcard_id = result[0]
            deck_id = result[1]
            question = result[2]
            answer = result[3]
            last_study_date = result[4]
            due_date_string = result[5]
            inter_repetition_interval = result[6]
            easiness_factor = result[7]
            repetition_number = result[8]
            # print("load_flashcards Flashcard id:", flashcard_id, " deck id:", deck_id, " question:", question, " answer:", answer,
            #       " laststudy:", last_study_date, " due_date_string:", due_date_string, " inter_repetition_interval:",
            #       inter_repetition_interval, " easiness_factor:", easiness_factor, " repetition_number:",
            #       repetition_number)
            flashcard = Flashcard(flashcard_id=flashcard_id,
                                  deck_id=deck_id,
                                  question=question,
                                  answer=answer,
                                  last_study_date=last_study_date,
                                  due_date_string=due_date_string,
                                  inter_repetition_interval=inter_repetition_interval,
                                  easiness_factor=easiness_factor,
                                  repetition_number=repetition_number)
            # print()
            deck.append_to_flashcards(flashcard)
        self.close_db()

    def today_as_string(self):
        """
        Creates a string from today's date.
        :return: Today's date as str in the format of YYYY-MM-DD.
        :rtype: str
        """
        today = datetime.today()
        return today.strftime('%Y-%m-%d')

    def load_due_flashcards(self, deck: Deck) -> None:
        """
        Fetch all due flashcards and only due flashcards of the given Deck object from the database
        by comparing due_date_string column in the database with the due_date_string attribute of
        Flashcard objects. A string comparison will be performed.
        :param deck: Deck object
        :type deck: Deck
        """
        self.open_db()
        deck.due_flashcards = []
        today_string = self.today_as_string()
        parameter = (deck.deck_id, today_string)
        # Due date is stored as str in the db. We make a string comparison to find due flashcards.
        results = self.cursor.execute("""
                                    SELECT * 
                                    FROM flashcard 
                                    WHERE deck_id == ? AND
                                    due_date_string <= ?
                                        """, parameter)
        # print("Deck title: ", deck.title, "Last study: ", deck.last_study_datetime)
        # print("Loaded flashcards: \n", results)
        for result in results:
            # print(result)
            flashcard_id = result[0]
            deck_id = result[1]
            question = result[2]
            answer = result[3]
            last_study_date = result[4]
            due_date_string = result[5]
            inter_repetition_interval = result[6]
            easiness_factor = result[7]
            repetition_number = result[8]
            # print("Due Flashcard id:", flashcard_id, " deck id:", deck_id, " question:", question, " answer:", answer,
            #       " laststudy:", last_study_date, " last_study_date type:", type(last_study_date), " duedate:",
            #       due_date_string, " due_date_string type:", type(due_date_string), " inter_repetition_interval:",
            #       inter_repetition_interval, " easiness_factor:", easiness_factor, " repetition_number:",
            #       repetition_number)
            flashcard = Flashcard(flashcard_id=flashcard_id,
                                  deck_id=deck_id,
                                  question=question,
                                  answer=answer,
                                  last_study_date=last_study_date,
                                  due_date_string=due_date_string,
                                  inter_repetition_interval=inter_repetition_interval,
                                  easiness_factor=easiness_factor,
                                  repetition_number=repetition_number)
            deck.due_flashcards.append(flashcard)
        self.close_db()

    def update_deck_in_db(self, deck_id, title, last_study_datetime) -> None:
        """
        This function updates the Deck's title and last_study_time values in the database. Update them always at the
        same time in this function. Deck's flashcard records are updated by update_flashcard_in_db().
        :param int deck_id: Deck's deck_id attribute. Unique identifier.
        :type deck_id: int
        :param str title: Deck's title attribute.
        :type title: str
        :param datetime last_study_datetime: Deck's last_study_daytime attribute.
        :type last_study_datetime: datetime
        """
        self.open_db()
        # self.db_connection.set_trace_callback(print)
        deck_row_tuple = (title, last_study_datetime, int(deck_id))
        sql = ''' UPDATE deck
                    SET title = ? , 
                    last_study_datetime = ?
                    WHERE deck_id = ? '''
        self.cursor.execute(sql, deck_row_tuple)
        self.close_db()

    def update_flashcard_in_db(self, flashcard_id, question, answer, last_study_date, due_date_string,
                               inter_repetition_interval, easiness_factor, repetition_number) -> None:
        """
        Update values in Flashcard table in the db.
        :param flashcard_id: Flashcard's unique identifier
        :type flashcard_id: int
        :param question: Value for question column
        :type question: str
        :param answer: Value for answer column
        :type answer: str
        :param last_study_date: Value for last_study_date column
        :type last_study_date: datetime
        :param due_date_string: Value for due_date_string column
        :type due_date_string: str
        :param inter_repetition_interval: Value for inter_repetition_interval column
        :type inter_repetition_interval: int
        :param easiness_factor: Value for easiness_factor column
        :type easiness_factor: float
        :param repetition_number: Value for repetition_number column
        :type repetition_number: int
        """
        self.open_db()
        # self.db_connection.set_trace_callback(print)
        flashcard_row_tuple = (question, answer, last_study_date, due_date_string,
                               inter_repetition_interval, easiness_factor, repetition_number,
                               int(flashcard_id))
        sql = ''' UPDATE flashcard
                            SET question = ? ,
                                answer = ?,
                                last_study_date = ?, 
                                due_date_string = ?,
                                inter_repetition_interval = ?, 
                                easiness_factor = ?, 
                                repetition_number = ?
                            WHERE flashcard_id = ? '''
        self.cursor.execute(sql, flashcard_row_tuple)
        self.close_db()

    def delete_flashcard_from_db(self, flashcard_id):
        """
        Delete a row from Flashcard table in the database.
        :param flashcard_id: Primary key in Flashcard table, mapping to the Flashcard's flashcard_id
        :type flashcard_id: int
        """
        self.open_db()
        # self.db_connection.set_trace_callback(print)
        flashcard_row_tuple = (int(flashcard_id),)
        sql = ''' DELETE FROM flashcard
                              WHERE flashcard_id = ? '''
        self.cursor.execute(sql, flashcard_row_tuple)
        self.close_db()
        # print("\ndelete_flashcard_from_db just run\n")
        # self.print_all_flashcards()

    def delete_deck_from_db(self, deck_id):
        """
        First delete all rows in Flashcard table where deck_id is the foreign key
        Finally, delete the row from Deck table where deck_id is the primary key
        As a result, delete from the database everything related to the Deck object
        of which deck_id is the passed deck_id
        :param deck_id: Primary key in Deck table, mapping to the Deck's deck_id
        :type deck_id: int
        """
        self.open_db()
        # First delete all flashcards of this deck
        flashcard_row_tuple = (int(deck_id),)
        sql = ''' DELETE FROM flashcard
                                      WHERE deck_id = ? '''
        self.cursor.execute(sql, flashcard_row_tuple)
        # Now delete the deck
        deck_row_tuple = (int(deck_id),)
        sql = ''' DELETE FROM deck
                              WHERE deck_id = ? '''
        self.cursor.execute(sql, deck_row_tuple)
        self.close_db()
        # print("\ndelete_deck_from_db just run\n")
        # self.print_all_flashcards()

    def set_first_deck_as_the_current_deck_if_possible(self) -> None:
        """
        To not leave current deck (self.deck) None, assign the Deck object at self.decks[0] to the self.deck attribute.
        If there is not any Deck object in the decks.list, assign None. // "What are you gonna do?" - T.S.
        """
        if len(self.decks) > 0:
            self.deck = self.decks[0]
        else:
            self.deck = None

    def print_all_flashcards(self) -> None:
        """
        Print all values from Flashcards table for debug purposes.
        """
        print()
        print("All Flashcards in the DB:")
        self.open_db()
        sql = ''' SELECT * FROM flashcard '''
        results = self.cursor.execute(sql)
        for result in results:
            flashcard_string = ''
            for index in range(4):
                flashcard_string += str(result[index]) + " "
            print(flashcard_string)
        self.close_db()
        print()

    # TODO [New Feature] Code a function to find duplicate values in the database. It can be useful when user is
    #  attempting to add a duplicate flashcard.

    # TODO [New Feature] Code a function to search data in the database.
