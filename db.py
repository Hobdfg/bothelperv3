import sqlite3

def create_table(db_name="speech_kit.db"):
    try:
        # Создаём подключение к базе данных
        with sqlite3.connect(db_name) as conn:
            cursor = conn.cursor()
            # Создаём таблицу messages
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY,
                user_id INTEGER,
                message TEXT,
                tts_symbols INTEGER)
            ''')
            # Сохраняем изменения
            conn.commit()
    except Exception as e:(
        print(f"Error: {e}"))


def insert_row(user_id, message, tts_symbols, db_name="speech_kit.db"):
    try:
        # Подключаемся к базе
        with sqlite3.connect( db_name ) as conn:
            cursor = conn.cursor()
            # Вставляем в таблицу новое сообщение
            cursor.execute( '''INSERT INTO messages (user_id, message, tts_symbols)VALUES (?, ?, ?)''',
                            (user_id, message, tts_symbols) )
            # Сохраняем изменения
            conn.commit()
    except Exception as e:  # обрабатываем ошибку и записываем её в переменную <e>
        print( f"Error: {e}" )  # выводим ошибку в консоль


def count_all_symbol(user_id, db_name="speech_kit.db"):
    try:
        # Подключаемся к базе
        with sqlite3.connect( db_name ) as conn:
            cursor = conn.cursor()
            # Считаем, сколько символов использовал пользователь
            cursor.execute( '''SELECT SUM(tts_symbols) FROM messages WHERE user_id=?''', (user_id,) )
            data = cursor.fetchone()
            # Проверяем data на наличие хоть какого-то полученного результата запроса
            # И на то, что в результате запроса мы получили какое-то число в data[0]
            if data and data[0]:
                # Если результат есть и data[0] == какому-то числу, то
                return data[0]  # возвращаем это число - сумму всех потраченных символов
            else:
                # Результата нет, так как у нас ещё нет записей о потраченных символах
                return 0  # возвращаем 0
    except Exception as e:
        print( f"Error: {e}" )
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
