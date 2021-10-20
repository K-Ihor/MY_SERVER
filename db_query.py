import asyncio
import sqlite3

def create_db():
    try:
        sqliteConnection = sqlite3.connect('SQLite_Python.db')
        sqlit_create_table_query = '''CREATE TABLE User_data (
                                    id INTEGER PRIMARY KEY,
                                    name TEXT NOT NULL UNIQUE,
                                    phone TEXT NOT NULL UNIQUE);'''

        cursor = sqliteConnection.cursor()
        print("Database created and Successfully Connected to SQLite")
        cursor.execute(sqlit_create_table_query)
        sqliteConnection.commit()
        print("SQLite table created")
        cursor.close()
    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")

def transaction_select(user_name: str):
    try:
        sqliteConnection = sqlite3.connect('SQLite_Python.db')
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")

        sqlite_select_query = f"""SELECT name, phone FROM User_data WHERE name = '{user_name}'"""
        cursor.execute(sqlite_select_query)
        records = cursor.fetchall()
        print("Total rows are:  ", len(records))
        print("Printing each row")
        for row in records:
            print("name: ", row[0])
            print("tel: ", row[1])
            print("\n")
            return row[1]

        cursor.close()

    except sqlite3.Error as error:
        print("Failed to read data from sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")



def transaction_insert(user_name: str, tel: str):
    try:
        sqliteConnection = sqlite3.connect('SQLite_Python.db')
        cursor = sqliteConnection.cursor()
        print("Successfully Connected to SQLite")
        sqlite_query = f"""INSERT INTO User_data (name, phone) VALUES ('{user_name}','{tel}')"""
        count = cursor.execute(sqlite_query)
        sqliteConnection.commit()
        print("Record inserted successfully into SqliteDb_developers table ", cursor.rowcount)
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to insert data into sqlite table", error)
        return False
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")


def transaction_delete(user_name: str):
    try:
        sqliteConnection = sqlite3.connect('SQLite_Python.db')
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")

        # Deleting single record now
        sql_delete_query = f"""DELETE from User_data WHERE name = '{user_name}'"""
        cursor.execute(sql_delete_query)
        sqliteConnection.commit()
        print("Record deleted successfully ")
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to delete record from sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("the sqlite connection is closed")


def check_record_db(user_name: str) -> bool:
    try:
        sqliteConnection = sqlite3.connect('SQLite_Python.db')
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")

        # Deleting single record now
        sql_check_query = f"""SELECT name, phone FROM User_data WHERE name = '{user_name}'"""
        cursor.execute(sql_check_query)
        sqliteConnection.commit()
        data=cursor.fetchone()
        cursor.close()
        if data is None:
            print(user_name, "no record")
            return False
        else:
            print(f"record {data[0]} exists ")
            return True
        print("Record check successfully ")
        

    except sqlite3.Error as error:
        print("Failed to check record from sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("the sqlite connection is closed")


