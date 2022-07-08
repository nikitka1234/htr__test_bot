import sqlite3


# подключаем базу данных и создаем курсор для работы с таблицами
conn = sqlite3.connect('db/db.db', check_same_thread=False)
cursor = conn.cursor()


# функция для работы с таблицей
def db_table_val(user_id: int, user_name: str, user_surname: str, username: str):
    cursor.execute('INSERT INTO test_user_table (user_id, user_name, user_surname, username) VALUES (?, ?, ?, ?)',
                   (user_id, user_name, user_surname, username))
    conn.commit()
