import sqlite3, os
from pprint import pprint
from pathlib import Path
import click

class Storage:
    #Create the storage (.db file) by passing it a path.
    def __init__(self):
        # self.filename = str(Path.home()) + "/.todo-storage.db"
        self.filename = "./todo-storage.db"
    # The function to cr    eate the database with a given file name or to connect to a database
    # with a filename.
    def create_database(self):
        try:
            conn = sqlite3.connect(self.filename)
        except sqlite3.Error as error:
            print(error)
        else:
            conn.commit()
            conn.close()


    # Create a table in the given database.
    def create_table(self):
        with sqlite3.connect(self.filename) as conn:
            cursor = conn.cursor()
            sql_statement = ("CREATE TABLE IF NOT EXISTS todos"
                     + "(tid INT PRIMARY KEY, name TEXT, prio TEXT, deadline TEXT);"
                     )
            cursor.execute(sql_statement)
            # click.echo(cursor.fetchall())
    #Function to add data to todolist database etc.
    #There's no point having 2 todo lists so i will not implement "tablename" stuff here.
    def add_task(self, task):
        with sqlite3.connect(self.filename) as conn:
            #If the table is empty, the first task is assigned TID 1.
            cursor = conn.cursor()
            cursor.execute(("SELECT COUNT(*) FROM todos"))
            count = cursor.fetchone()[0]
            if count == 0:
                count += 1
                tid = count
            else:
                count += 1
                tid = count
            sql_statement = """INSERT INTO todos(tid,name,prio,deadline) VALUES(?,?,?,?)"""
            name, prio, deadline = task
            entry = list(task)
            entry.insert(0, tid)
            cursor.execute(sql_statement, entry)

    #Update an existing entry in the database:
    def update_existing(self, task_update):
        with sqlite3.connect(self.filename) as conn:
            tid, name, prio, deadline = task_update
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM todos WHERE tid=" + str(tid))
            current_info = list(cursor.fetchone())
            current_info.pop(0)
            click.echo(f"current info is...{current_info}")
            if name == "":
                namestatement = ""
                cursor.execute("SELECT name FROM todos WHERE tid=" + str(tid))
                name = str(cursor.fetchone()[0])
                namestatement = "name='" + name + "'"
            elif name:
                namestatement = "name='" + name + "'"
            if prio == "":
                priostatement = ""
                cursor.execute("SELECT prio FROM todos WHERE tid=" + str(tid))
                prio = str(cursor.fetchone()[0])
                priostatement = "prio='" + prio + "'"

            elif prio:
                cursor.execute("SELECT prio FROM todos WHERE tid=" + str(tid))
                priostatement = "prio='" + prio + "'"
            if deadline == "":
                deadline_statement = ""
                cursor.execute("SELECT deadline FROM todos WHERE tid=" + str(tid))
                deadline = str(cursor.fetchone()[0])
                deadline_statement = "deadline='" + deadline + "'"
            elif deadline:
                deadline_statement = "deadline='" + deadline + "'"
            statements = [namestatement, priostatement, deadline_statement]
            update_statement = [statement for statement in statements if statement != ""]
            # click.echo(update_statement)
            cursor.execute("SELECT * FROM todos WHERE tid=" + str(tid))
            row_update = [name, prio, deadline]
            click.echo(row_update)
            if row_update == current_info:
                click.secho("No inputs, no update made", fg="bright_red")

            cursor = conn.cursor()
            if len(update_statement) < 1:
                """UPDATE todos SET """ + "".join(update_statement[0]) + " WHERE tid=" + str(tid)
            else:
                sql_statement =   """UPDATE todos SET """ + ",".join(update_statement) + " WHERE tid=" + str(tid)
            # click.echo(sql_statement)
            cursor.execute(sql_statement)
    def view_todo(self):
        self.correct_entry_nos()
        with sqlite3.connect(self.filename) as conn:
            cursor = conn.cursor()
            cursor.execute("""SELECT * from todos""")
            todolist = cursor.fetchall()
            return todolist

    def delete_todo(self, taskid):
        with sqlite3.connect(self.filename) as conn:
            cursor = conn.cursor()
            sql_statement = """DELETE FROM todos WHERE tid=""" + str(taskid)
            cursor.execute(sql_statement)
            conn.commit()

    #This method ensures that when the view method is called, that each task is in the correct order with no gaps.
    def correct_entry_nos(self):
        with sqlite3.connect(self.filename) as conn:
            cursor = conn.cursor()
            sql_fetch = """SELECT tid FROM todos"""
            cursor.execute(sql_fetch)
            fetched_data = cursor.fetchall()
            current_tids = [tid[0] for tid in fetched_data]
            count = len(current_tids)

            updated_tids = [x + 1 for x in range(len(current_tids))]
            # click.echo(f"{updated_tids} {current_tids}")

            #Below implement SQL statement that assigns the updated and corrected
            #Entries to the TID slot so it is consistent after deleting an entry.
            for _ in range(count):
                cursor.execute("""UPDATE todos SET tid=""" + str(updated_tids[_]) + """ WHERE tid=""" + str(current_tids[_]))

                # click.echo((fetched_data[counter][0]))
                # counter += 1
            # click.echo(fetched_data)