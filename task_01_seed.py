from datetime import datetime
import faker
from random import choice
import sqlite3

# Кількість записів для кожної таблиці
NUMBER_STATUSES = 3
NUMBER_USERS = 10
NUMBER_TASKS = 20

def generate_fake_data(number_statuses, number_users, number_tasks) -> tuple:
    fake_statuses = []
    fake_users = []
    fake_tasks = []
    fake_data = faker.Faker()

    statuses = ['new', 'in progress', 'completed']
    fake_statuses.extend(statuses)

    for _ in range(number_users):
        fake_users.append((fake_data.name(), fake_data.email()))

    for _ in range(number_tasks):
        fake_tasks.append((
            fake_data.sentence(nb_words=6),
            fake_data.text(max_nb_chars=200),
        ))

    return fake_statuses, fake_users, fake_tasks

def prepare_data(statuses, users, tasks) -> tuple:
    for_statuses = [(status,) for status in statuses]
    for_users = users
    for_tasks = []
    
    return for_statuses, for_users, for_tasks

def insert_data_to_db(statuses, users, tasks) -> None:
    fake_data = faker.Faker()
    
    try:
        with sqlite3.connect('database.db') as con:
            cur = con.cursor()

            # Вставка статусів
            sql_to_statuses = """INSERT OR IGNORE INTO status(name) VALUES (?);"""
            cur.executemany(sql_to_statuses, statuses)

            # Вставка користувачів
            sql_to_users = """INSERT OR IGNORE INTO users(fullname, email) VALUES (?, ?);"""
            cur.executemany(sql_to_users, users)

            # Отримання ID статусів і користувачів
            cur.execute("SELECT id, name FROM status;")
            status_id_map = {row[1]: row[0] for row in cur.fetchall()}

            cur.execute("SELECT id FROM users;")
            user_ids = [row[0] for row in cur.fetchall()]

            # Перевірка: Друк статусів і користувачів для діагностики
            print("Status ID Map:", status_id_map)
            print("User IDs:", user_ids)

            if not status_id_map:
                print("Error: No statuses found in the database.")
            if not user_ids:
                print("Error: No users found in the database.")

            for_tasks = []
            for _ in range(NUMBER_TASKS):
                title = fake_data.sentence(nb_words=6)
                description = fake_data.text(max_nb_chars=200)
                status_id = choice(list(status_id_map.values())) if status_id_map else None
                user_id = choice(user_ids) if user_ids else None
                if status_id is not None and user_id is not None:
                    for_tasks.append((title, description, status_id, user_id))
                else:
                    print("Skipping task due to missing status_id or user_id")

            if for_tasks:
                sql_to_tasks = """INSERT INTO tasks(title, description, status_id, user_id) VALUES (?, ?, ?, ?);"""
                cur.executemany(sql_to_tasks, for_tasks)
            else:
                print("No tasks to insert.")

            con.commit()
    except sqlite3.Error as e:
        print(f"Помилка при вставленні даних: {e}")

if __name__ == "__main__":
    statuses, users, tasks = generate_fake_data(NUMBER_STATUSES, NUMBER_USERS, NUMBER_TASKS)
    prepared_statuses, prepared_users, prepared_tasks = prepare_data(statuses, users, tasks)
    insert_data_to_db(prepared_statuses, prepared_users, prepared_tasks)
