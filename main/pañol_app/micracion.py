import sqlite3
from sqlite3 import Error

import pandas as pd

df = pd.read_csv('csv/hechos.csv')
conn = sqlite3.connect('db.sqlite3')
df.to_sql('pañol_app_equiposretirados', conn, index=True, index_label='id',  if_exists='replace')
print(df)


df = pd.read_csv('lista_tecnicos.csv')
conn = sqlite3.connect('db.sqlite3')
df.to_sql('pañol_app_tecnico', conn, index=True, index_label='id',  if_exists='replace')
print(df)