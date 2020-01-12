import pandas as pd
from transliterate import translit

newFile = r'D:\Dev\csvTranslit\newUsers.csv'
file = r'D:\Dev\csvTranslit\users.csv'
headers = ['username', 'password', 'lastname', 'firstname', 'middlename', 'email']
myCSV = pd.read_csv(file, sep=';')
df = pd.DataFrame(index=range(0, len(myCSV)), columns=headers)


def translit_row(row):
    username = translit(row[0], "ru", reversed=True).lower()
    return pd.Series([username.replace("'", ""), row[1].replace(" ", ""), row[2].replace(" ", ""),
                      row[3].replace(" ", ""), row[4].replace(" ", ""), row[5].replace(" ", "")], headers)


for i, row in enumerate(myCSV.values):
    df.loc[i] = translit_row(row)

df.to_csv(newFile, sep=";", header=True, index=False)
print(df)
