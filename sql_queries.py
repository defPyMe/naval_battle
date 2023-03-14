import sqlite3

path_to_db = r"C:\Users\cavazzinil\Dropbox\naval battle code + ideas\naval_battle\naval_battle.db"

def checking_credentials(name):
    with sqlite3.connect(path_to_db) as conn:
        command = "SELECT name FROM users WHERE  name = (?)"
        result_of_name_fetch = conn.execute(command, (name,))
        fetching_the_result = result_of_name_fetch.fetchone()
        conn.commit()

    return fetching_the_result
        
