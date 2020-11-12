import sqlite3
import os
from Deck import Deck
from Flashcard import Flashcard


class DatabaseManager:
    DB_PATH = "Flashcards.db"

    def __init__(self):
        print("DatabaseManager inits")

        # # DEBUG
        # try:
        #     os.remove(DatabaseManager.DB_PATH)
        # except:
        #     print("Error in removing db file")

        self.db_connection: sqlite3.Connection = None
        self.cursor: sqlite3.Cursor = None
        self.provide_db()

        self.decks: [Deck] = []

        # Current deck will be held in this variable in a single place. This will be used in other classes too.
        self.deck: Deck = None

        # DEBUG
        # self.create_dummy_decks()
        # self.create_dummy_flashcards1(self.decks[0])
        # self.create_dummy_flashcards2(self.decks[1])
        self.load_all_decks()

    def open_db(self):
        try:
            self.db_connection = sqlite3.connect(DatabaseManager.DB_PATH)
            self.cursor = self.db_connection.cursor()
            # print("SQLite connection established.")
        except sqlite3.Error as error:
            print("Error while opening database: ", error)

    def close_db(self):
        try:
            self.db_connection.commit()
            self.cursor.close()
            self.db_connection.close()
        except sqlite3.Error as error:
            print("Error in closing database: ", error)
        # print("SQLite connection closed.")

    def provide_db(self):
        should_create_tables = False
        if not os.path.exists(DatabaseManager.DB_PATH):
            should_create_tables = True
        try:
            self.open_db()
            self.print_db_version()
            if should_create_tables:
                self.create_tables()
            self.close_db()
        except sqlite3.Error as error:
            print("Error while connecting to sqlite", error)
        finally:
            if self.db_connection:
                self.db_connection.close()
            print("SQLite connection closed.")

    def create_tables(self):
        try:
            cursor = self.db_connection.cursor()

            cursor.execute("""
            CREATE TABLE IF NOT EXISTS deck (
            deck_id INTEGER PRIMARY KEY, 
            title TEXT NOT NULL )
            """)

            cursor.execute("""
            CREATE TABLE IF NOT EXISTS flashcard (
            flashcard_id INTEGER PRIMARY KEY, 
            deck_id INTEGER NOT NULL, 
            question TEXT NOT NULL, 
            answer TEXT NOT NULL,
            FOREIGN KEY (deck_id) REFERENCES deck (deck_id) )
            """)

            print("SQLite tables have been created.")

        except sqlite3.Error as error:
            print("Error while creating tables", error)

    def print_db_version(self):
        sqlite_select_query = "select sqlite_version();"
        self.cursor.execute(sqlite_select_query)
        record = self.cursor.fetchall()
        print("SQLite Database Version is: ", record)

    def add_new_deck_to_db(self, deck_title):
        self.open_db()
        deck_row_tuple = (deck_title,)
        # deck_id will be added by SQLite automatically because it is defined as INTEGER PRIMARY KEY.
        # For more info: https://www.sqlite.org/autoinc.html
        sql = ''' INSERT INTO deck(title)
                      VALUES(?) '''
        self.cursor.execute(sql, deck_row_tuple)
        self.close_db()
        return self.cursor.lastrowid

    def add_new_flashcard_to_db(self, deck_id, question, answer):
        self.open_db()
        flashcard_row_tuple = (deck_id, question, answer)
        sql = ''' INSERT INTO flashcard(deck_id, question, answer)
                      VALUES(?,?,?) '''
        self.cursor.execute(sql, flashcard_row_tuple)
        self.close_db()
        return self.cursor.lastrowid

    def load_all_decks(self):
        print()
        print("load_all_decks:")
        self.open_db()
        self.cursor.execute("SELECT * FROM deck")
        temp_decks = self.cursor.fetchall()
        self.decks = []
        for deck in temp_decks:
            deck_id = deck[0]
            deck_title = deck[1]
            print("Loaded deck ID:", deck_id, "title:", deck_title)
            deck = Deck(deck_id, deck_title)
            self.decks.append(deck)
            self.load_flashcards(deck)
        self.close_db()
        if len(self.decks) > 0:
            self.load_deck(0)
        print()

    def load_deck(self, deck_index):
        self.deck = self.decks[deck_index]
        self.load_flashcards(self.deck)

    def load_flashcards(self, deck):
        self.open_db()
        deck.flashcards = []
        parameter = (deck.deck_id,)
        results = self.cursor.execute("SELECT * FROM flashcard WHERE deck_id == ?", parameter)
        print("Deck: ", deck.title, " Loaded flashcards: ", results)
        for result in results:
            print(result)
            flashcard_id = result[0]
            deck_id = result[1]
            question = result[2]
            answer = result[3]
            flashcard = Flashcard(flashcard_id, deck_id, question, answer)
            deck.flashcards.append(flashcard)
        # self.deck.flashcards =
        self.close_db()

    def create_dummy_decks(self):
        deck_title = "USA capital cities"
        deck_id = self.add_new_deck_to_db(deck_title)
        deck = Deck(deck_id, deck_title)
        self.decks.append(deck)

        deck_title = "Network Ports"
        deck_id = self.add_new_deck_to_db(deck_title)
        deck = Deck(deck_id, deck_title)
        self.decks.append(deck)

        # return decks

    def create_dummy_flashcards1(self, deck):
        print("deck.deck_id:", deck.deck_id)
        flashcard_id = self.add_new_flashcard_to_db(deck.deck_id, "Capital of Texas?", "Austin")
        flashcard1 = Flashcard(flashcard_id, deck.deck_id, "Capital of Texas?", "Austin")

        flashcard_id = self.add_new_flashcard_to_db(deck.deck_id, "Capital of California?", "Sacramento")
        flashcard2 = Flashcard(flashcard_id, deck.deck_id, "Capital of California?", "Sacramento")

        flashcard_id = self.add_new_flashcard_to_db(deck.deck_id, "Capital of Washington?", "Olympia")
        flashcard3 = Flashcard(flashcard_id, deck.deck_id, "Capital of Washington?", "Olympia")

        deck.flashcards = [flashcard1, flashcard2, flashcard3]

    def create_dummy_flashcards2(self, deck):
        question = "FTP"
        answer = "20, 21"
        flashcard_id = self.add_new_flashcard_to_db(deck.deck_id, question, answer)
        flashcard1 = Flashcard(flashcard_id, deck.deck_id, question, answer)
        question = "SSH"
        answer = "22"
        flashcard_id = self.add_new_flashcard_to_db(deck.deck_id, question, answer)
        flashcard2 = Flashcard(flashcard_id, deck.deck_id, question, answer)
        question = "Telnet"
        answer = "23"
        flashcard_id = self.add_new_flashcard_to_db(deck.deck_id, question, answer)
        flashcard3 = Flashcard(flashcard_id, deck.deck_id, question, answer)
        question = "SMTP"
        answer = "25"
        flashcard_id = self.add_new_flashcard_to_db(deck.deck_id, question, answer)
        flashcard4 = Flashcard(flashcard_id, deck.deck_id, question, answer)

        deck.flashcards = [flashcard1, flashcard2, flashcard3, flashcard4]

    def rename_deck_in_db(self, deck_id, title):
        self.open_db()
        self.db_connection.set_trace_callback(print)
        deck_row_tuple = (title, int(deck_id))
        sql = ''' UPDATE deck
                    SET title = ?
                    WHERE deck_id = ? '''
        self.cursor.execute(sql, deck_row_tuple)
        self.close_db()

    def update_flashcard_in_db(self, flashcard_id, question, answer):
        self.open_db()
        self.db_connection.set_trace_callback(print)
        flashcard_row_tuple = (question, answer, int(flashcard_id))
        sql = ''' UPDATE flashcard
                            SET question = ? ,
                                answer = ?
                            WHERE flashcard_id = ? '''
        self.cursor.execute(sql, flashcard_row_tuple)
        self.close_db()

    def delete_flashcard_from_db(self, flashcard_id):
        self.open_db()
        self.db_connection.set_trace_callback(print)
        flashcard_row_tuple = (int(flashcard_id),)
        sql = ''' DELETE FROM flashcard
                              WHERE flashcard_id = ? '''
        self.cursor.execute(sql, flashcard_row_tuple)
        self.close_db()
        print("\ndelete_flashcard_from_db just run\n")
        self.print_all_flashcards()

    def delete_deck_from_db(self, deck_id):
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
        print("\ndelete_deck_from_db just run\n")
        self.print_all_flashcards()

    def set_current_deck_if_possible(self):
        if len(self.decks) > 0:
            self.deck = self.decks[0]
        else:
            self.deck = None

    def print_all_flashcards(self):
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