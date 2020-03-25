import pandas as pd
from transliterate import translit
import string
import random
import argparse
import os


def create_parser():
    parser = argparse.ArgumentParser(
        prog="Create User to CSV for Moodle",
        description="This profgram creates new csv file with useranme, password, lastname, firstname, middlename, "
                    "email (if not exists it will be created fake one) and cohort. "
                    "For that action you should provide csv file with at least lastname, firstname, middlename",
        epilog='(c) A.V. Liubimov.'
    )
    parser.add_argument('-f', '--file', type=argparse.FileType(mode='r', encoding="UTF8"), required=True,
                        help='Path to original cvs file')
    parser.add_argument('-e', '--email', action='store_true', default=False,
                        help='Should it create "fake" e-mail. Default - No. But you shold provide e-mail in csv.')
    parser.add_argument('-c', '--cohort', help='Name of cohort')
    return parser


def random_password():
    chars = string.ascii_uppercase + string.ascii_lowercase + string.digits
    size = random.randint(8, 12)
    return ''.join(random.choice(chars) for x in range(size))


def create_username(last_name, first_name, middle_name):
    return translit_text(last_name + first_name[0] + middle_name[0])


def email(username):
    return username + "@example.com"


def translit_text(text):
    return translit(text, "ru", reversed=True).lower()
    # username = translit(row[0], "ru", reversed=True).lower()
    # email = username.replace("'", "") + "@example.com"
    # return pd.Series([username.replace("'", ""), random_password(), row[2].replace(" ", ""),
    #                   row[3].replace(" ", ""), row[4].replace(" ", ""), email, row[6].replace(" ", "")], headers)


if __name__ == '__main__':
    parser = create_parser()
    namespace = parser.parse_args()
    path = os.path.dirname(namespace.file.name)
    file = os.path.basename(namespace.file.name)
    newFile = path + "\\new_" + file
    print(newFile)
    headers = ['username', 'password', 'lastname', 'firstname', 'middlename', 'email', 'cohort1']
    myCSV = pd.read_csv(file, sep=';')
    df = pd.DataFrame(index=range(0, len(myCSV)), columns=headers)
    header_list = myCSV.columns.to_list()

    for i, row in enumerate(myCSV.values):
        for j in range(len(row) - 1):
            row[j] = row[j].strip()
        username = create_username(myCSV.lastname[i].strip(), myCSV.firstname[i].strip(), myCSV.middlename[i].strip())
        if namespace.email:
            if namespace.cohort:
                df.loc[i] = pd.Series(
                    [username, random_password(), myCSV.lastname[i].strip(), myCSV.firstname[i].strip(),
                     myCSV.middlename[i].strip(),
                     email(username), namespace.cohort], headers)
            else:
                df.loc[i] = pd.Series(
                    [username, random_password(), myCSV.lastname[i].strip(), myCSV.firstname[i].strip(),
                     myCSV.middlename[i].strip(),
                     email(username), myCSV.cohort1[i]], headers)
        else:
            if namespace.cohort:
                df.loc[i] = pd.Series(
                    [username, random_password(), myCSV.lastname[i].strip(), myCSV.firstname[i].strip(),
                     myCSV.middlename[i].strip(),
                     myCSV.email[i].strip(), namespace.cohort.strip()], headers)
            else:
                df.loc[i] = pd.Series(
                    [username, random_password(), myCSV.lastname[i].strip(), myCSV.firstname[i].strip(),
                     myCSV.middlename[i].strip(),
                     myCSV.email[i].strip(), myCSV.cohort1[i]], headers)

    df.to_csv(newFile, sep=";", header=True, index=False)
    print(df.all)
