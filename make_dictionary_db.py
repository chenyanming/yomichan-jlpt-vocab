#!/usr/bin/env python3
import csv
import sqlite3
import glob
import os
# Connect to SQLite database
conn = sqlite3.connect('japanese.db')
def insert_csv_to_db(csv_file):
    c = conn.cursor()
    # Create table
    c.execute('''
        CREATE TABLE IF NOT EXISTS jlpt_table (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            jmdict_seq INTEGER,
            kanji TEXT,
            kana TEXT,
            waller_definition TEXT,
            origin TEXT,
            original TEXT,
            level TEXT
        )
    ''')
    # Read and insert data from CSV
    with open(csv_file, 'r') as f:
        dr = csv.DictReader(f)
        csv_file_name = os.path.basename(csv_file)
        csv_file_base_name = os.path.splitext(csv_file_name)[0]
        to_db = [(i['jmdict_seq'], i['kanji'], i['kana'], i['waller_definition'], i['origin'], i['original'], csv_file_base_name) for i in dr]
    c.executemany('''
        INSERT INTO jlpt_table (
            jmdict_seq,
            kanji,
            kana,
            waller_definition,
            origin,
            original,
            level
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)''', to_db)
    # Save (commit) the changes
    conn.commit()
# Get a list of csv files in the data folder
csv_files = glob.glob("data/*.csv")
# Insert each csv file to the database
for csv_file in csv_files:
    insert_csv_to_db(csv_file)

# Create indexes
conn.execute('CREATE INDEX IF NOT EXISTS idx_kanji ON jlpt_table (kanji)')
conn.execute('CREATE INDEX IF NOT EXISTS idx_kana ON jlpt_table (kana)')

# Close connection
conn.close()
