import csv
from time import localtime, strftime

from Deck import Deck
from Flashcard import Flashcard
from DatabaseManager import DatabaseManager


class ImportExportManager:

    def __init__(self, database_manager: DatabaseManager):
        # self.write_test()
        self.database_manager: DatabaseManager = database_manager
        # self.importfile("common_network_ports.csv")

    def write_test(self):
        with open('names.csv', 'w', newline='') as csvfile:
            fieldnames = ['first_name', 'last_name']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            writer.writerow({'first_name': 'Baked', 'last_name': 'Beans'})
            writer.writerow({'first_name': 'Lovely', 'last_name': 'Spam'})
            writer.writerow({'first_name': 'Wonderful', 'last_name': 'Spam'})

    # def read_test(self, filename):
    #     print("read_test")
    #     if filename == "":
    #         filename = "names.csv"
    #     with open(filename, newline='') as csvfile:
    #         try:
    #             reader = csv.DictReader(csvfile)
    #             dictionary = dict()
    #             for row in reader:
    #                     print(row['key'], row['value'])
    #                     dictionary[row['key']] = row['value']
    #             print("dictionary['program']: ", dictionary['program'])
    #             print("dictionary['decktitle']: ", dictionary['decktitle'])
    #             print("dictionary['fileversion']: ", dictionary['fileversion'])
    #             dictlist = list(dictionary.items())
    #             print(dictlist[0][0])
    #         except Exception as error:
    #             print("Exception: ", error)

    def importfile(self, filename):
        try:
            with open(filename, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                reader.fieldnames = ("key", "value")
                dictionary = dict()
                decktitle = ""
                index = 0
                for row in reader:
                    # print(row['key'], row['value'])
                    try:
                        if row['key'] != 'program' and row['key'] != 'fileversion' and row['key'] != 'decktitle':
                            dictionary[row['key']] = row['value']
                        elif row['key'] == 'decktitle':
                            decktitle = row['value']
                    except Exception as error:
                        print("Bad row: ", row)
                        print("Exception: ", error)

                datetime_string = strftime("%Y-%m-%d %H:%M:%S", localtime())

                decktitle = decktitle.strip()
                if decktitle == '':
                    decktitle = "Imported deck (" + datetime_string + ")"

                new_deck_id = self.database_manager.add_new_deck_to_db(decktitle)
                new_deck = Deck(new_deck_id, decktitle)
                self.database_manager.decks.append(new_deck)

                listdict = list(dictionary.items())
                for item in listdict:
                    print("item[0]: ", item[0])
                    print("item[1]: ", item[1])
                    today_as_string = self.database_manager.today_as_string()
                    new_flashcard_id = self.database_manager.add_new_flashcard_to_db(new_deck_id, item[0], item[1], last_study_date=None, due_date_string=today_as_string)
                    new_flashcard = Flashcard(new_flashcard_id, new_deck_id, item[0], item[1])
                    new_deck.flashcards.append(new_flashcard)

                return True
            return False
        except Exception as error:
            print("Exception: ", error)
