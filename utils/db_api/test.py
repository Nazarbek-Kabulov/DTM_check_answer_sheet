import sqlite3


def create_table():
    # Ma'lumotlar bazasiga bog'liq bo'lgan yo'ldagi faylni o'zgartiring
    db_path = '/home/nazarbek/Portfolio/Check-answer-sheet/data/main.db'

    # SQLite bog'lanishini ochamiz
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    # CREATE TABLE so'rovini ishga tushiramiz
    create_table_query = """
        CREATE TABLE IF NOT EXISTS TEST_ANSWERS (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            book_number INTEGER NOT NULL,
            answers TEXT NOT NULL
        );
    """
    cursor.execute(create_table_query)

    # Bog'lanishni yopamiz
    connection.close()
    print('Successful create table!')

# Table yaratishni chaqirib ko'ramiz
create_table()
