import asyncio

from server import Server
from ws.ws_handler import Ws_handler

async def main():
    ws_handler = Ws_handler()
    server = Server(ws_handler)

    await server.start()



if __name__ == "__main__":
    asyncio.run(main())