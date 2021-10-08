import socket
import sqlite3


def connect_db():
    try:
        sqliteConnection = sqlite3.connect('SQLite_Python.db')
        cursor = sqliteConnection.cursor()
        print("Database created and Successfully Connected to SQLite")

        sqlite_select_Query = "select sqlite_version();"
        cursor.execute(sqlite_select_Query)
        record = cursor.fetchall()
        print("SQLite Database Version is: ", record)
        cursor.close()

    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")



data_base = {
    "Vasy": "0367788555",
    "Alex": "0258795864"
}

def AMOZNO(INF: str) -> str:
    """Asks for permission to disclose information"""
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_sock.connect(('vragi-vezde.to.digital', 51624))
    client_sock.send(f"АМОЖНА? РКСОК/1.0\n{INF}\r\n\r\n".encode("utf-8"))
    data = client_sock.recv(1024).decode("utf-8")
    client_sock.close()
    print(data)
    return data

server = socket.create_server(("127.0.0.1", 8000))
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server.listen(10)
try:
    while True:
        client_socket, address = server.accept()
        received_data = client_socket.recv(1024).decode('utf-8')

        print(received_data)

        inf_clint = received_data.split(" ")


        if AMOZNO(inf_clint).split(" ")[0] == "МОЖНА":
            if inf_clint[0] == "ОТДОВАЙ":
                if inf_clint[0] == "ОТДОВАЙ" and data_base.get(inf_clint[1], ) != None:
                    response = f"НОРМАЛДЫКС РКСОК/1.0\n{data_base.get(inf_clint[1], )}\r\n\r\n"
                else:
                    response = "НИНАШОЛ РКСОК/1.0"
            elif inf_clint[0] == "ЗОПИШИ":
                if inf_clint[0] == "ЗОПИШИ" and data_base.get(inf_clint[1], ) == inf_clint[2].split("\r\n")[1]:
                    response = f"НИЛЬЗЯ РКСОК/1.0\nУже едем\r\n\r\n"
                else:
                    data_base.update({inf_clint[1]: inf_clint[2].split("\r\n")[1]})
                    print(data_base)
                    response = "НОРМАЛДЫКС РКСОК/1.0"
            elif inf_clint[0] == "УДОЛИ":
                if inf_clint[0] == "УДОЛИ" and data_base.get(inf_clint[1], ) != None:  
                    data_base.pop(inf_clint[1], )
                    response = "НОРМАЛДЫКС РКСОК/1.0"
                else:
                    response = "НИНАШОЛ РКСОК/1.0"
            elif inf_clint[0] == "GET" or "POST" or "PUT" or "DELETE":
                response = f"HTTP/1.1 200 OK\nContent-Type: text/html; charset=utf-8\n\n" \
                        f"Привет! отживший своё протокол HTTP(S),<br /> Это Рабоче-Крестьянский Стандарт Отправки Команд 'РКСОК'"
            else:
                response = "НИПОНЯЛ РКСОК/1.0"
        else:
            response = f"НИЛЬЗЯ РКСОК/1.0\nЧто ещё за {inf_clint[1]} такой? Он тебе зачем?\r\n\r\n"


        client_socket.send(response.encode("utf-8"))
        client_socket.shutdown(socket.SHUT_RDWR)
except:        
    server.shutdown(socket.SHUT_RDWR)
    server.close()