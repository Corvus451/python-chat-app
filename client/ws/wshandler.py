import asyncio
import websockets
from utility.logger import Logger

class WsHandler:
    def __init__(self, on_message: function, on_close: function, logger: Logger):
        self.__ws: websockets.ClientConnection = None
        self.__on_message = on_message
        self.__on_close = on_close
        self.__logger = logger

    def is_connected(self) -> bool:
        return self.__ws and self.__ws.state == websockets.State.OPEN
    
    async def connect(self, address: str):
        async def receive(ws: websockets.ClientConnection):

            try:
                async for msg in ws:
                    self.__on_message(msg)

            except Exception as e:
                self.__logger.log(e)

            finally:
                self.__on_close()
                self.__ws = None

        try:
            connection = await websockets.connect(f"ws://{address}")
            self.__ws = connection
            asyncio.create_task(receive(self.__ws))
            return True
        except Exception as e:
            self.__logger.log(e)
            return False
        
    async def disconnect(self):
        if self.is_connected():
            await self.__ws.close()

    async def send_message(self, msg: str):
        if msg and self.is_connected():
            try:
                await self.__ws.send(msg)
                return True
            except Exception as e:
                self.__logger.log(e)
                return False
    