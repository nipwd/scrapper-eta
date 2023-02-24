import pandas as pd

df = pd.read_excel('xlsx/devo.xlsx', na_values=['nan'])
df2 = df.ARTICULO
df2 =df2.value_counts()

df3 =pd.DataFrame(df2)
df3.to_csv('xlsx/devo.csv')
df3.sort_values('ARTICULO', ascending=False)

df3 = df3.sort_index(key=lambda x: x.str.lower())

df3.to_csv('xlsx/devo.csv')
print(df3)