import asyncio

from config.config import Config
from server import Server
from ws.ws_handler import Ws_handler

async def main():
    cfg = Config("server.ini")
    ws_handler = Ws_handler(cfg)
    server = Server(ws_handler)

    await server.start()



if __name__ == "__main__":
    asyncio.run(main())