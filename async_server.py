import asyncio
import socket
import sqlite3

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


def AMOZNO(INF: str) -> str:
    """Asks for permission to disclose information"""
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_sock.connect(('vragi-vezde.to.digital', 51624))
    client_sock.send(f"АМОЖНА? РКСОК/1.0\n{INF}\r\n\r\n".encode("utf-8"))
    data = client_sock.recv(1024).decode("utf-8")
    client_sock.close()
    print(data.split(" ")[0])
    return data.split(" ")[0]


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



async def my_server(reader, writer):
    data = await reader.read(1024)
    received_data = data.decode('utf-8')
    print(f'принял: {received_data}')

    inf_clint = received_data.split(" ")

    # inf_client_name = received_data.rpartition("РКСОК")[0][7:]
    # print(f"ПРЕОБРАЗОВАНИЕ {inf_client_name}")
    inf_client_name = received_data.split(" ")[1:-1]
    if len(inf_client_name) == 1:
        inf_client_name.append(" ")
        
    inf_client_phone = received_data.split("\r\n")[-3:-2]

    print(f"{inf_clint}\n{inf_client_name}\n{inf_client_phone}")

    if AMOZNO(inf_clint).split(" ")[0] == "МОЖНА":
        if inf_clint[0] == "ОТДОВАЙ":
            if inf_clint[0] == "ОТДОВАЙ" and check_record_db(" ".join(inf_client_name)) == True:                   
                response = f"НОРМАЛДЫКС РКСОК/1.0\n{transaction_select(' '.join(inf_client_name))}\r\n\r\n"                  
            else:
                response = "НИНАШОЛ РКСОК/1.0"


        elif inf_clint[0] == "ЗОПИШИ":
            if inf_clint[0] == "ЗОПИШИ" and check_record_db(" ".join(inf_client_name)) == True \
                or transaction_insert(" ".join(inf_client_name), inf_client_phone[0]) == False:
                response = f"НИЛЬЗЯ РКСОК/1.0\nУже едем\r\n\r\n"
            else:
                transaction_insert(" ".join(inf_client_name), inf_client_phone[0])
                response = "НОРМАЛДЫКС РКСОК/1.0"

        elif inf_clint[0] == "УДОЛИ":
            if inf_clint[0] == "УДОЛИ" and check_record_db(" ".join(inf_client_name)) == True:
                transaction_delete(" ".join(inf_client_name))
                response = "НОРМАЛДЫКС РКСОК/1.0"
            else:
                response = "НИНАШОЛ РКСОК/1.0"

        elif inf_clint[0] == "GET" or "POST" or "PUT" or "DELETE":
            response = f"HTTP/1.1 200 OK\nContent-Type: text/html; charset=utf-8\n\n" \
                    f"Привет! отживший своё протокол HTTP(S),<br /> Это Рабоче-Крестьянский Стандарт Отправки Команд 'РКСОК'"
        else:
            response = "НИПОНЯЛ РКСОК/1.0"
    else:
        response = f"НИЛЬЗЯ РКСОК/1.0\nЧто ещё за {' '.join(inf_client_name)} такой? Он тебе зачем?\r\n\r\n"

    print(f"Send: {response}")
    writer.write(response.encode("utf-8"))
    await writer.drain()

    print("Close the connection")
    writer.close()


async def main():
    server = await asyncio.start_server(
        my_server, '127.0.0.1', 8000)

    addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
    print(f'Serving on {addrs}')

    async with server:
        await server.serve_forever()

asyncio.run(main())