import socket


def AMOZNO(INF: str) -> str:
    """Asks for permission to disclose information"""
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_sock.connect(('vragi-vezde.to.digital', 51624))
    client_sock.send(f"АМОЖНА? РКСОК/1.0\n{INF}\r\n\r\n".encode("utf-8"))
    data = client_sock.recv(1024).decode("utf-8")
    client_sock.close()
    print(data.split(" ")[0])
    return data.split(" ")[0]


# async def AMOZNO(*INF: str) -> str:
#     """Asks for permission to disclose information"""
#     client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     client_sock.connect(('vragi-vezde.to.digital', 51624))
#     client_sock.send(f"АМОЖНА? РКСОК/1.0\n{INF}\r\n\r\n".encode("utf-8"))
#     data = client_sock.recv(1024).decode("utf-8")
#     client_sock.close()
#     print(data.split(" ")[0])
#     return data.split(" ")[0]
