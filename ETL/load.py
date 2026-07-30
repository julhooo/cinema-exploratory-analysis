import pandas as pd
import sqlite3 as sq
import os

"""
    All CSV files stored in the data/processed directory are loaded into the database, where they become available for querying and analysis.
"""

conn = sq.connect("../database/cinema.db")

def toDatabase(filename:str):
    df = pd.read_csv(f"../data/processed/{filename}.csv")
    
    df.to_sql(f"{filename}", conn, if_exists="replace")

files = os.listdir("../data/processed")

for i in files:
    i = i.split(".")
    toDatabase(i[0])

conn.close()    