#script to truncate the tables
import sqlite3
path_to_db = r"C:\Users\cavazzinil\Dropbox\naval battle code + ideas\naval_battle\naval_battle.db"



with sqlite3.connect(path_to_db) as conn:
     conn.execute("DELETE FROM battle_table")

   
     conn.commit()