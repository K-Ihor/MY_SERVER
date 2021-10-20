import asyncio
from loguru import logger
from ask_permission_query import AMOZNO
from db_query import *
from config import HOST, PORT
from create_response import formation_response

create_db()


@logger.catch
async def my_server(reader, writer):
    data = b""
    while True:
        chunk = await reader.read(1024)
        data += chunk
        if not chunk or chunk.endswith(b"\r\n\r\n"):
            break

    received_data = data.decode('utf-8')
    logger.info(f"Received: {received_data!r}")

    print(f'принял: {received_data}')

    response = formation_response(received_data)   #  "НИПОНЯЛ РКСОК/1.0"

    print(f"Send: {response}")
    writer.write(response.encode("utf-8")) #.encode("utf-8")
    logger.info(f"Sent: {response!r}")
    await writer.drain()

    print("Close the connection")
    writer.close()


async def main():
    logger.add("logs/rksok.log",
                format="{time} {level} {message}",
                level="INFO",
                rotation="100 KB",
                compression="zip",
    )

    server = await asyncio.start_server(
        my_server, HOST, PORT)

    addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
    print(f'Serving on {addrs}')
    logger.info(f"Serving on {addrs}")

    async with server:
        await server.serve_forever()

asyncio.run(main())