import sqlite3


class Database:
    def __init__(self, db_name):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()

    def add_new_user(self, tg_id, username, f_name, l_name):
        self.cursor.execute(f"INSERT INTO users (tg_username, tg_firstname, tg_lastname, tg_id)"
                            f"VALUES (?, ?, ?, ?)", (username, f_name, l_name, tg_id))
        self.connection.commit()

    def update_user(self, tg_id, full_name, phone, email, birth_date):
        self.cursor.execute(F"UPDATE users SET full_name=?, tg_phone=?, email=?, birth_date=?"
                            F"WHERE tg_id=?", (full_name, phone, email, birth_date, tg_id))
        self.connection.commit()

    def get_user(self, tg_id):
        user = self.cursor.execute(f"SELECT * FROM users WHERE tg_id=?", (tg_id,))
        return user.fetchone()

    def get_user_by_username(self, user_name):
        user = self.cursor.execute(f"SELECT * FROM users WHERE tg_username=?", (user_name,))
        return user.fetchone()

    def up_url(self, tg_id):
        self.cursor.execute(f"UPDATE users SET url_count = url_count+1 WHERE tg_id=?", (tg_id,))
        self.connection.commit()

    def __del__(self):
        self.cursor.close()
        self.connection.close()
