import pandas as pd
from transliterate import translit
import string
import random
from sys import argv

file, email = argv

def randompassword():
  chars = string.ascii_uppercase + string.ascii_lowercase + string.digits
  size = random.randint(8, 12)
  return ''.join(random.choice(chars) for x in range(size))

newFile = r'D:\Dev\PythonProjects\csvTranslit\new_username.csv'
file = r'D:\Dev\PythonProjects\csvTranslit\username.csv'
headers = ['username', 'password', 'lastname', 'firstname', 'middlename', 'email', 'cohort1']
myCSV = pd.read_csv(file, sep=';')
df = pd.DataFrame(index=range(0, len(myCSV)), columns=headers)

def translit_row(row):
    username = translit(row[0], "ru", reversed=True).lower()
    email = username.replace("'", "")+"@example.com"
    return pd.Series([username.replace("'", ""), randompassword(), row[2].replace(" ", ""),
                      row[3].replace(" ", ""), row[4].replace(" ", ""), email, row[6].replace(" ", "")], headers)


for i, row in enumerate(myCSV.values):
    df.loc[i] = translit_row(row)

df.to_csv(newFile, sep=";", header=True, index=False)
print(df.all)
