import sqlite3


def create_database():
    try:
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            telegram_user_id INTEGER,
            total_gpt_tokens INTEGER,
            total_stt_blocks INTEGER)
            ''')
    except Expection as e:
        return None


def add_new_user(user_id):
    try:
        with sqlite3.connect(DB_LIFE) as conn:
            cursor = conn.cursor()
            cursor.execute('''
            INSERT INTO users (telegram_user_id, total_gpt_tokens, total_stt_blocks)
            VALUES (?, ?, ?)''',
                           (user_id, 0, 0)
                           )
            conn.commit()
    except Expection as e:
        return None


def update_user_tokens(user_id, add_tokens):
    try:
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute(
                f'UPDATE users SET total_gpt_tokens = total_gpt_tokens + {add_tokens}) WHERE telegram_user_id = {user_id}'
            )
            conn.commit()
    except Expection as e:
        return None

def  select_all_users():
    users = []
    try:
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute('''SELECT telegram_user_id FROM users''')
            data = cursor.fetchall()
            if data and data[0]:
                for user in data:
                    users.append(user[0])
                return users
    except Exception as e:
        return users


def get_tokens_for_user(user_id):
    try:
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute(f'''SELECT total_gpt_tokens FROM users WHERE user_id=?''', (user_id,))
            data = cursor.fetchone()
                if data and data[0]:
                    return data[0]
                else:
                    return 0
                except Exception as e:
            return 0
