import os
import sys
import code
import sqlite3
from datetime import datetime
from termcolor import colored
from tabulate import tabulate

DEFAULT_PATH = os.path.join(os.path.dirname(__file__), 'database.sqlite3')
conn = sqlite3.connect(DEFAULT_PATH)

sql = """
	CREATE TABLE IF NOT EXISTS todos(
    id INTEGER PRIMARY KEY,
    body TEXT NOT NULL,
    due_date TEXT NOT NULL,
    status TEXT DEFAULT "incomplete"
    )
"""
cur = conn.cursor()
cur.execute(sql)


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def add():
    print(colored('*' * 24, 'green'))
    print(colored('* input ":c" to cancel *', 'green'))
    print(colored('*' * 24, 'green'))
    print('What would you like to add? ')
    body = input()
    if body != ':c':
        print(colored('Adding Todo:', 'green'), body)
        sql = """
			INSERT INTO todos (body, due_date) VALUES (?, ?)
		"""
        cur.execute(sql, (body, datetime.now()))
        conn.commit()


def show_list():
    print('Filter by(done/undone/all): ', end='')
    status = input()

    if status == 'done' or status == 'd':
        sql = """
            SELECT * FROM todos
            WHERE status = 'completed'
        """
    elif status == "undone" or status == 'u':
        sql = """
            SELECT * FROM todos
            WHERE status = 'incomplete'
        """
    else:
        sql = """
            SELECT * FROM todos
            ORDER BY status DESC
        """
    cur.execute(sql)
    results = cur.fetchall()
    conn.commit()

    print(colored('Todo List:', 'green'), len(results), 'todos')
    if len(results) > 0:
        table = []
        header = ['ID', 'TASK', 'DUE DATE', 'STATUS']
        for row in results:
            table = [*table, row]
        print(colored(tabulate(table, header, tablefmt='fancy_grid'), 'cyan'))


def find(id):
    sql = """
        SELECT id FROM todos
        WHERE id = (?)
    """
    cur.execute(sql, (id,))
    result = cur.fetchall()
    conn.commit()
    return len(result) > 0


def do():
    print(colored('*' * 24, 'green'))
    print(colored('* input ":c" to cancel *', 'green'))
    print(colored('*' * 24, 'green'))
    print('Todo id: ', end='')
    id = input()
    if id != ':c':
        if find(id):
            sql = """
                UPDATE todos
                SET status = 'completed'
                WHERE id == (?)
            """
            cur.execute(sql, id)
            conn.commit()
        else:
            print(colored('ID NOT EXIST!', 'red'))


def undo():
    print(colored('*' * 24, 'green'))
    print(colored('* input ":c" to cancel *', 'green'))
    print(colored('*' * 24, 'green'))
    print('Todo id: ', end='')
    id = input()
    if id != ':c':
        print('Todo id: ', end='')
        id = input()
        if find(id):
            sql = """
                UPDATE todos
                SET status = 'incomplete'
                WHERE id == (?)
            """
            cur.execute(sql, id)
            conn.commit()
        else:
            print(colored('ID NOT EXIST!', 'red'))


def remove():
    print('Todo id: ', end='')
    id = input()
    print("Are you sure (y/n)? ", end='')
    confirm = input()
    if confirm == 'yes' or confirm == 'y':
        if find(id):
            sql = """
                DELETE FROM todos
                WHERE id = (?)
            """
            cur.execute(sql, id)
            conn.commit()
        else:
            print(colored('ID NOT EXIST!', 'red'))


def show_usage():
    print(colored('*' * 24, 'green'))
    print(colored('          USEAGE', 'green'))
    print(colored('-' * 24, 'green'))
    print(colored('help[h]: show help menu ', 'green'))
    print(colored('quit[q]: quit the app ', 'green'))
    print(colored('*' * 24, 'green'))


def show_help_menu():
    print(colored('*' * 40, 'green'))
    print(colored('*            *HELP MENU*               *', 'green'))
    print(colored('*' * 40, 'green'))
    table = [
        ['list', 'l', 'List all todos'],
        ['add', 'a', 'Add a new todo'],
        ['done', 'd', 'Done a todo'],
        ['undone', 'u', 'Undone a  todo'],
        ['remove', 'r', 'Remove a todo'],
        ['help', 'h', 'Show help menu'],
        ['quit', 'q', 'Quit todos']
    ]
    header = ['Name', 'Shortcut', 'Description']
    print(colored(tabulate(table, header,  tablefmt="fancy_grid"), 'green'))


if __name__ == '__main__':
    try:
        clear_screen()
        show_usage()
        while True:
            print('What do you want to do?')
            choice = input()
            if choice == 'help' or choice == 'h':
                clear_screen()
                show_help_menu()
            elif choice == 'add' or choice == 'a':
                clear_screen()
                add()
                show_usage()
            elif choice == 'list' or choice == 'l':
                clear_screen()
                show_list()
                show_usage()
            elif choice == 'do' or choice == 'd':
                do()
            elif choice == 'undo' or choice == 'u':
                undo()
            elif choice == 'remove' or choice == 'r':
                remove()
            elif choice == 'quit' or choice == 'q':
                break
    except:
        print('Failed to upload to ftp: ' + str(e))
sys.exit(1)
