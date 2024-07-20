import sqlite3

def create_db():
    database = "database.db"

    sql_create_users_table = """
    DROP TABLE IF EXISTS users;
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fullname TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL
    );
    """

    sql_create_status_table = """
    DROP TABLE IF EXISTS status;
    CREATE TABLE IF NOT EXISTS status (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL
    );
    """

    sql_create_tasks_table = """
    DROP TABLE IF EXISTS tasks;
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        status_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        FOREIGN KEY (status_id) REFERENCES status (id),
        FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
    );
    """

    # Підключення до бази даних
    try:
        with sqlite3.connect(database) as con:
            cur = con.cursor()
            # Створення таблиць
            cur.executescript(sql_create_users_table)
            cur.executescript(sql_create_status_table)
            cur.executescript(sql_create_tasks_table)
            print("Таблиці успішно створено.")
    except sqlite3.Error as e:
        print(f"Помилка при створенні бази даних: {e}")

if __name__ == "__main__":
    create_db()
