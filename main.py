# from pprint import pprint
import csv
import re


def reading_file(raw_csv_file):
    with open(raw_csv_file, encoding="utf-8") as f:
        rows = csv.reader(f, delimiter=",")
        contacts_list = list(rows)

        return contacts_list


def formatting_data(raw_csv_file):
    contacts_list = reading_file(raw_csv_file)

    pattern = (r"(\+7|8)?\s*\(*(495)\)*[\s|-]*(\d{3})[\s|-]*(\d{2})"
               r"[\s|-]*(\d+)(\s*)\(*(\w+\.)*\s*(\d*)\)*")
    sub_pattern = r"+7(\2)\3-\4-\5\6\7\8"

    new_contacts_list = list()

    for data in contacts_list:
        result = re.sub(pattern, sub_pattern, data[5])
        phone_list = [result]
        email = [data[6]]
        new_contact = ' '.join(data[:3]).split(' ')[
                      :3] + data[3:5] + phone_list + email
        new_contacts_list.append(new_contact)

    return new_contacts_list


def removing_duplicates(raw_csv_file):
    new_contacts_list = formatting_data(raw_csv_file)

    for data in new_contacts_list:
        for copy_data in new_contacts_list:
            if data[0] in copy_data and data[1] in copy_data:
                if data[2] == '':
                    data[2] = copy_data[2]
                if data[3] == '':
                    data[3] = copy_data[3]
                if data[4] == '':
                    data[4] = copy_data[4]
                if data[5] == '':
                    data[5] = copy_data[5]
                if data[6] == '':
                    data[6] = copy_data[6]

    result_list = []

    for contact in new_contacts_list:
        if contact not in result_list:
            result_list.append(contact)

    return result_list


def write_file(raw_csv_file, processed_csv_file):
    result_list = removing_duplicates(raw_csv_file)

    with open(processed_csv_file, "w", encoding="utf-8", newline='') as f:
        data_writer = csv.writer(f, delimiter=',')
        data_writer.writerows(result_list)
    return result_list


if __name__ == '__main__':
    phonebook_name = (
        f"{input('введите название телефонной книги для записи: ')}.csv"
    )
    phonebook_raw = 'phonebook_raw.csv'
    write_file(phonebook_raw, phonebook_name)
