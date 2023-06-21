import sqlite3

conn = sqlite3.connect('db/database.sqlite', check_same_thread=False)
cursor = conn.cursor()


def db_add_user(user_id: int, username: str):
    cursor.execute(
        'INSERT INTO user (user_id, username) VALUES (?, ?)', (user_id, username, ))
    conn.commit()


def db_update_income(user_id: int, income: float):
    cursor.execute(
        "UPDATE user SET income = income + ? WHERE user_id = ?", (income, user_id,))
    conn.commit()


def db_update_expenses(user_id: int, expenses: float):
    cursor.execute(
        "UPDATE user SET expenses = expenses + ? WHERE user_id = ?", (expenses, user_id,))
    conn.commit()


def db_update_savings(user_id: int):
    cursor.execute(
        "UPDATE user SET savings = savings + (?) - (?)  WHERE user_id = ?", (income, expenses, user_id,))
    conn.commit()


def db_get_savings(user_id: int):
    cursor.execute(
        "SELECT savings FROM user WHERE user_id = ?", (user_id, ))
    current_savings = cursor.fetchall()
    return current_savings[0][0]


def db_get_income(user_id: int):
    cursor.execute(
        "SELECT income FROM user WHERE user_id = ?", (user_id, ))
    current_savings = cursor.fetchall()
    return current_savings[0][0]


def db_get_expenses(user_id: int):
    cursor.execute(
        "SELECT expenses FROM user WHERE user_id = ?", (user_id, ))
    current_savings = cursor.fetchall()
    return current_savings[0][0]
