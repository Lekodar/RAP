import openpyxl
import sqlite3


# Создаем и подключаемся к БД
try:
    Session = sqlite3.connect('bot.db', check_same_thread=False)
    cursor = Session.cursor()
    sqlite_select_query = "select sqlite_version();"
    cursor.execute(sqlite_select_query)
    cursor.execute('''
       CREATE TABLE IF NOT EXISTS users(
           user_id integer,
           fullname text,
           delays_number integer,
           passes_number integer,
           date text
       )''')
except sqlite3.Error as error:
    print(f"Error when connecting to sqlite: {error}")


workbook = openpyxl.Workbook()
worksheet = workbook.active
# Функции для взаимодействия с БД


def put(user_id, fullname, delays_number, passes_number, date):
    params = int(user_id), fullname, delays_number, passes_number, date
    cursor.execute(f'INSERT INTO users VALUES(?, ?, ?, ?, ?)', params)
    Session.commit()


def fetchall():
    fullnames = cursor.execute('SELECT fullname FROM users').fetchall()
    return fullnames


def rep(filename):
    cursor.execute("SELECT * FROM users")
    data = cursor.fetchall()
    headers = [column[0] for column in cursor.description]
    worksheet.append(headers)

    for row in data:
        worksheet.append(row)

    workbook.save(f'{filename}.xlsx')


def delete(fullname):
    cursor.execute('DELETE FROM users WHERE fullname = ?', (fullname, ))
    Session.commit()


def mark(fullname, value):
    if value == 'опоздал':
        value = 'delays_number'
    if value == 'пропустил':
        value = 'passes_number'
    number = cursor.execute(f'SELECT {value} FROM users WHERE fullname == ?', (fullname, )).fetchone()[0]
    number = int(number) + 1
    cursor.execute(f'UPDATE users SET {value} = {number} where fullname == ?', (fullname, ))
    Session.commit()
