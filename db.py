import sqlite3

class Database:
    def __init__(self):
        self.connection = sqlite3.connect('data.db')
        self.cursor = self.connection.cursor()

    def create_database(self):
        '''Creating database'''
        with self.connection:
            return self.cursor.execute("""CREATE TABLE IF NOT EXISTS data (
            token TEXT,
            ownerid TEXT,
            userid TEXT,
            username TEXT
        )""")
        
    def populate_data(self, token, owner_id, user_id, username):
        '''Populating data in database'''
        with self.connection:
            return self.cursor.execute(f"INSERT INTO data VALUES (?, ?, ?, ?)", (token, owner_id, user_id, username))
        
    def takes_all_data(self):
        '''Takes all data'''
        with self.connection:
            return self.cursor.execute("SELECT * FROM data").fetchone()
        
    def add_token_and_user_id(self, token, user_id):
        '''Puts the token and user_id in the table'''
        with self.connection:
            return self.cursor.execute(f"INSERT INTO data VALUES (?, ?, ?, ?)", (token, None, user_id, None))
        