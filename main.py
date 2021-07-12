from pprint import pprint
import csv
import re


with open("phonebook_raw.csv", encoding='utf-8') as f:
  rows = csv.reader(f, delimiter=",")
  contacts_book = list(rows)

class Contacts_Filter:
    def filter_fio(self, contacts_list):
        for human in contacts_list:
            lastname = ''
            firstname = ''
            surname = ''

            for i, item in enumerate(human):
                if i > 2:
                    break

                tmp_list = item.split(' ')

                if i == 0:
                    if lastname == '':
                        lastname = item

                    if len(tmp_list) > 1:
                        lastname = tmp_list[0]

                        try:
                            firstname = tmp_list[1]
                        except IndexError:
                            continue

                        try:
                            surname = tmp_list[2]
                        except IndexError:
                            continue

                elif i == 1:
                    if firstname == '':
                        firstname = item

                    if len(tmp_list) > 1:
                        try:
                            firstname = tmp_list[0]
                        except IndexError:
                            continue

                        try:
                            surname = tmp_list[1]
                        except IndexError:
                            continue

                else:
                    if surname == '':
                        surname = item

            human[0] = lastname
            human[1] = firstname
            human[2] = surname
        return contacts_list

    def filter_phone(self, contacts_list):
        for human in contacts_list:
            for i, item in enumerate(human):
                if i == 5:
                    result = re.sub(
                        r'([\+7|8]+)\s*\(?(\d{3})\)?[\s|-]*(\d{3})[\s|-]*(\d{2})[\s|-]*(\d{2})\s*(\(?(\w+\.)\s*(\d+)\)?)*',
                        r'+7(\2)\3-\4-\5 \7 \8', item)
                    human[5] = result
        return contacts_list

    def search_duplicate_human(self, contacts_list):
        for human in contacts_list:
            quantity_duplicate = 0
            for human2 in contacts_list:
                if human[0] == human2[0] and human[1] == human2[1]:
                    quantity_duplicate += 1
                    if quantity_duplicate >= 2:
                        for i in range(len(human2)):
                            if human2[i] != '':
                                human[i] = human2[i]
                        contacts_list.remove(human2)

        return contacts_list


contact = Contacts_Filter()
contacts_book = contact.filter_fio(contacts_book)
contacts_book = contact.filter_phone(contacts_book)
contacts_book = contact.search_duplicate_human(contacts_book)


# TODO 2: сохраните получившиеся данные в другой файл
# код для записи файла в формате CSV
with open("phonebook.csv", "w", encoding='utf-8') as f:
  datawriter = csv.writer(f, delimiter=',')
  # Вместо contacts_list подставьте свой список
  datawriter.writerows(contacts_book)