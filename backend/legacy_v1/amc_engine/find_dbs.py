import os
import sqlite3

def find_dbs(folder):
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith('.db'):
                path = os.path.join(root, file)
                try:
                    c = sqlite3.connect(path).cursor()
                    tables = c.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
                    if tables:
                        print(f'Found DB: {path} with tables: {tables}')
                except Exception as e:
                    pass

find_dbs(r'c:\AI_MathMate\amc_engine')
