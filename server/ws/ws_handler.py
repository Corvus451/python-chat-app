import asyncio
import json
import websockets
from websockets.asyncio.server import serve
from websockets.asyncio.server import ServerConnection
from websockets import exceptions



class Ws_handler:
    def __init__(self):
        self.__clients: set[websockets.ServerConnection] = set()
        self.__join_handler = None
        self.__on_msg = None
        self.__on_close = None


    def set_handlers(self, join_handler, on_msg, on_close):
        self.__join_handler = join_handler
        self.__on_msg = on_msg
        self.__on_close = on_close


    def add_client(self, ws: ServerConnection):
        self.__clients.add(ws)


    def remove_client(self, ws: ServerConnection):
        self.__clients.discard(ws)


    async def drop_client(self, ws: ServerConnection, close_code: websockets.CloseCode):
        await ws.close(close_code)

   
    async def send_msg(self, ws: ServerConnection, msg_type, msg):
        message_to_send = json.dumps({"type": msg_type, msg_type: msg})
        await ws.send(message_to_send)


    async def broadcast_msg(self, msg_type, msg):
        for client in self.__clients:
            if client.state == websockets.State.OPEN:
                await self.send_msg(client, msg_type, msg)


    async def get_message(self, ws: ServerConnection):
        msg = await ws.recv()
        return msg


    async def receive(self, ws: ServerConnection):
        try:
            async for msg in ws:
                await self.__on_msg(ws, msg)
            
        except Exception as e:
            if not isinstance(e, exceptions.ConnectionClosedOK):
                print("connection closed unexpectedly")
            print(e)


    async def start(self):
        if not self.__join_handler or not self.__on_msg or not self.__on_close:
            print("handlers not set")
            return
        
        async with serve(self.__join_handler, "localhost", 8765) as server:
            await server.serve_forever()