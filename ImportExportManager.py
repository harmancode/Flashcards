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


import csv  # Documentation: https://docs.python.org/3/library/csv.html
from time import localtime, strftime

from Deck import Deck
from Flashcard import Flashcard
from DatabaseManager import DatabaseManager

try:
    import tkinter as tk  # python 3
except ImportError:
    import Tkinter as tk  # python 2


class ImportExportManager:

    def __init__(self, database_manager: DatabaseManager):
        """
        ImportExportManager class handles importing (and -not yet- exporting) data operations.
        :param database_manager: DatabaseManager
        """
        self.database_manager: DatabaseManager = database_manager

    def import_csv_file(self, filepath) -> bool:
        """
        Imports given csv file
        :param filepath: Path to the file, including filename
        :return: True if import is successful. Otherwise, False.
        """

        try:

            with open(filepath, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                reader.fieldnames = ("key", "value")
                dictionary = dict()
                decktitle = ""
                count = 0
                valid_file = False

                # Process every row in the imported data
                for row in reader:
                    # print(row['key'], row['value'])
                    try:
                        # Check if key is special
                        if row['key'] == 'decktitle':
                            decktitle = row['value']
                        elif row['key'] == 'fileversion':
                            # There is not any process defined yet for this data.
                            pass
                        elif row['key'] == 'program':
                            # There is not any process defined yet for this data.
                            pass
                        else:
                            # Key is not special, process it as an ordinary row
                            dictionary[row['key']] = row['value']
                            count += 1
                    except Exception as error:
                        print("Bad row in import_csv_file(): ", row)
                        print("Exception in import_csv_file(): ", error)
                # end for row in reader

                if count <= 0:
                    tk.messagebox.showwarning("No flashcards found",
                                              "There is not any recognizable flashcards found in this file.")
                    valid_file = False
                elif count > Deck.MAXIMUM_AMOUNT_OF_FLASHCARDS:
                    warning_message = "This file contains more flashcards that a deck may contain. " \
                                      "A deck may not contain more than {} " \
                                      "flashcards".format(Deck.MAXIMUM_AMOUNT_OF_FLASHCARDS)
                    tk.messagebox.showwarning("Too many flashcards",
                                              warning_message)
                    valid_file = False
                else:
                    valid_file = True
                # end if count <= ImportExportManager.MAXIMUM_FLASHCARDS_IN_IMPORTED_DECK

                if valid_file:
                    # Get current local time as formatted string
                    datetime_string = strftime("%Y-%m-%d %H:%M:%S", localtime())

                    decktitle = decktitle.strip()

                    # If there is not any decktitle key found in the imported data, set a title by adding current date
                    # and time to the title.
                    if decktitle == '':
                        decktitle = "Imported deck (" + datetime_string + ")"

                    # Create imported deck in memory and in database
                    new_deck_id = self.database_manager.add_new_deck_to_db(decktitle)
                    new_deck = Deck(new_deck_id, decktitle)
                    self.database_manager.decks.append(new_deck)

                    # print()
                    # print("dictionary is filled. its contents:", dictionary.items())
                    # print("now passing to listdict phase...")

                    # Add imported flashcards to the imported deck
                    listdict = list(dictionary.items())

                    for item in listdict:

                        # print("question: ", item[0])
                        # print("answer: ", item[1])

                        today_as_string = self.database_manager.today_as_string()

                        new_flashcard_id = self.database_manager.add_new_flashcard_to_db(deck_id=new_deck_id,
                                                                                         question=item[0],
                                                                                         answer=item[1],
                                                                                         last_study_date=None,
                                                                                         due_date_string=today_as_string)
                        new_flashcard = Flashcard(flashcard_id=new_flashcard_id,
                                                  deck_id=new_deck_id,
                                                  question=item[0],
                                                  answer=item[1])

                        new_deck.append_to_flashcards(new_flashcard)

                    # end for item in listdict

                    return True

                # end if valid_file

            return False

            # end with open

        # end try

        except Exception as error:
            print("Exception import_csv_file(): ", error)

        # end except

    # end import_csv_file()

    def export_csv_file(self, filepath, deck) -> bool:
        """
        Export a deck to a csv file.
        :param filepath: Path of the file with .csv extension added.
        :type filepath: str
        :param deck: Deck object to be exported
        :type deck: Deck
        :return: True if export is successful. Otherwise, false.
        :rtype: bool
        """

        try:

            with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:

                dictionary = dict()

                for flashcard in deck.flashcards:
                    question = flashcard.question
                    answer = flashcard.answer
                    dictionary[question] = answer

                fieldnames = ['key', 'value']

                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                # writer.writeheader() # Not necessary
                writer.writerow({'key': 'decktitle', 'value': deck.title})

                for key in dictionary:
                    # Uncomment to print the data as it is being written to the file.
                    # print("key: ", key)
                    # print("value: ", dictionary[key])
                    # print()
                    writer.writerow({'key': key, 'value': dictionary[key]})

                return True

        except Exception as error:

            print("Exception export_csv_file(): ", error)

            return False
