import sqlite3

# Підключення до бази даних
conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# Отримати всі завдання певного користувача
def get_tasks_by_user(user_id):
    cursor.execute("SELECT * FROM tasks WHERE user_id = ?;", (user_id,))
    return cursor.fetchall()

# Вибрати завдання за певним статусом
def get_tasks_by_status(status_name):
    cursor.execute("SELECT * FROM tasks WHERE status_id = (SELECT id FROM status WHERE name = ?);", (status_name,))
    return cursor.fetchall()

# Оновити статус конкретного завдання
def update_task_status(task_id, new_status):
    cursor.execute("UPDATE tasks SET status_id = (SELECT id FROM status WHERE name = ?) WHERE id = ?;", (new_status, task_id))
    conn.commit()

# Отримати список користувачів, які не мають жодного завдання
def get_users_without_tasks():
    cursor.execute("SELECT * FROM users WHERE id NOT IN (SELECT DISTINCT user_id FROM tasks);")
    return cursor.fetchall()

# Додати нове завдання для конкретного користувача
def add_task_for_user(title, description, user_id):
    cursor.execute("INSERT INTO tasks (title, description, status_id, user_id) VALUES (?, ?, (SELECT id FROM status WHERE name = 'new'), ?);", (title, description, user_id))
    conn.commit()

# Отримати всі завдання, які ще не завершено
def get_uncompleted_tasks():
    cursor.execute("SELECT * FROM tasks WHERE status_id != (SELECT id FROM status WHERE name = 'completed');")
    return cursor.fetchall()

# Видалити конкретне завдання
def delete_task(task_id):
    cursor.execute("DELETE FROM tasks WHERE id = ?;", (task_id,))
    conn.commit()

# Знайти користувачів з певною електронною поштою
def find_users_by_email_domain(domain):
    cursor.execute("SELECT * FROM users WHERE email LIKE ?;", ('%' + domain,))
    return cursor.fetchall()

# Оновити ім'я користувача
def update_user_name(user_id, new_name):
    cursor.execute("UPDATE users SET fullname = ? WHERE id = ?;", (new_name, user_id))
    conn.commit()

# Отримати кількість завдань для кожного статусу
def get_task_count_by_status():
    cursor.execute("SELECT s.name, COUNT(t.id) FROM tasks t JOIN status s ON t.status_id = s.id GROUP BY s.name;")
    return cursor.fetchall()

# Отримати завдання, які призначені користувачам з певною доменною частиною електронної пошти
def get_tasks_by_user_email_domain(domain):
    cursor.execute("SELECT t.* FROM tasks t JOIN users u ON t.user_id = u.id WHERE u.email LIKE ?;", ('%' + domain,))
    return cursor.fetchall()

# Отримати список завдань, що не мають опису
def get_tasks_without_description():
    cursor.execute("SELECT * FROM tasks WHERE description IS NULL;")
    return cursor.fetchall()

# Вибрати користувачів та їхні завдання, які є у статусі 'in progress'
def get_users_and_tasks_in_progress():
    cursor.execute("SELECT u.*, t.* FROM users u JOIN tasks t ON u.id = t.user_id WHERE t.status_id = (SELECT id FROM status WHERE name = 'in progress');")
    return cursor.fetchall()

# Отримати користувачів та кількість їхніх завдань
def get_users_and_task_counts():
    cursor.execute("SELECT u.id, u.fullname, COUNT(t.id) AS task_count FROM users u LEFT JOIN tasks t ON u.id = t.user_id GROUP BY u.id, u.fullname;")
    return cursor.fetchall()

# Друк результатів для тестування
print("Tasks for user with ID 1:", get_tasks_by_user(1))
print("Tasks with status 'new':", get_tasks_by_status('new'))
update_task_status(1, 'completed')
print("Users without tasks:", get_users_without_tasks())
add_task_for_user('New Task', 'This is a new task', 1)
print("Uncompleted tasks:", get_uncompleted_tasks())
delete_task(1) # Для прикладу
print("Users with '@example.com' domain:", find_users_by_email_domain('example.com'))
update_user_name(1, 'Updated Name')
print("Task count by status:", get_task_count_by_status())
print("Tasks by users with email domain 'example.com':", get_tasks_by_user_email_domain('example.com'))
print("Tasks without description:", get_tasks_without_description())
print("Users and their tasks in progress:", get_users_and_tasks_in_progress())
print("Users and their task counts:", get_users_and_task_counts())

# Закриття підключення
cursor.close()
conn.close()
