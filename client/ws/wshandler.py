import asyncio
import json
import websockets
from utility.logger import Logger
from ui.ui import UI

class WsHandler:
    def __init__(self, on_message, on_close, logger: Logger, ui: UI):
        self.__ws: websockets.ClientConnection = None
        self.__on_message = on_message
        self.__on_close = on_close
        self.__logger = logger
        self.__ui = ui
        self.__is_connecting: bool = False
        self.__is_disconnecting: bool = False

    def is_connected(self) -> bool:
        return self.__ws and self.__ws.state == websockets.State.OPEN
    
    # def is_connecting(self) -> bool:
    #     return self.__ws and self.__ws.state == websockets.State.CONNECTING
    
    # def is_disconnecting(self) -> bool:
    #     return self.__ws and self.__ws.state == websockets.State.CLOSING
    
    async def connect(self, address: str, nickname: str):
        if self.__is_connecting or self.is_connected():
            return False
        
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
            self.__is_connecting = True

            self.__ui.add_message(f"connecting to {address}")

            connection = await websockets.connect(f"ws://{address}")
            self.__ws = connection

            connect_msg = json.dumps({
                "type": "join",
                "nickname": nickname
            })
            await self.__ws.send(connect_msg)
            successful = await self.__ws.recv()
            self.__on_message(successful)
            
            asyncio.create_task(receive(self.__ws))

            self.__is_connecting = False

            return True
        
        except Exception as e:
            self.__is_connecting = False
            self.__logger.log(e)
            self.__ui.add_message("connection failed")
            return False
        
    async def disconnect(self):
        if self.__is_disconnecting:
            return
        
        self.__is_disconnecting = True

        if self.is_connected():
            await self.__ws.close()

        self.__is_disconnecting = False

    def __create_message(self, text: str):
        return json.dumps({
        "type": "message",
        "message": text
    })

    async def send_message(self, msg: str):
        if msg and self.is_connected():
            try:
                await self.__ws.send(self.__create_message(msg))
                return True
            except Exception as e:
                self.__logger.log(e)
                return False
    