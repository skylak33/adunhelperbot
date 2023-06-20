import sqlite3

conn = sqlite3.connect('db/database.sqlite', check_same_thread=False)
cursor = conn.cursor()


def db_add_user(user_id: int):
    cursor.execute('INSERT INTO user (user_id) VALUES (?)', (user_id, ))
    conn.commit()


def db_update_income(user_id: int, income: float):
    cursor.execute(
        "UPDATE user SET income = income + ? WHERE user_id = ?", (income, user_id,))
    conn.commit()


def db_update_expenses(user_id: int, expenses: float):
    cursor.execute(
        "UPDATE user SET expenses = expenses + ? WHERE user_id = ?", (expenses, user_id,))
    conn.commit()