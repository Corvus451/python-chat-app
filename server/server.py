import json

from websockets.asyncio.server import ServerConnection
from websockets import CloseCode
from websockets import exceptions

from ws.ws_handler import Ws_handler


class Server:
    def __init__(self, ws_handler: Ws_handler):
        self.__ws_handler = ws_handler
        self.__ws_handler.set_handlers(self.__join_handler, self.__msg_handler, self.__close_handler)


    def __parse_message(self, msg: str) -> dict:
        try:
            parsed = json.loads(msg)
            if not isinstance(parsed, dict):
                return None
            return parsed
    
        except:
            return None


    async def __join_handler(self, ws: ServerConnection):
        try:
            join_msg = await self.__ws_handler.get_message(ws)
            join_msg = self.__parse_message(join_msg)
            if not join_msg:
                await self.__ws_handler.drop_client(ws, CloseCode.UNSUPPORTED_DATA)
                return
            
            if not join_msg.get("type")  == "join" or not join_msg.get("nickname"):
                self.__ws_handler.drop_client(ws, CloseCode.INVALID_DATA)
                return
            
            ws.nickname = join_msg["nickname"]
            self.__ws_handler.add_client(ws)

            await self.__ws_handler.send_msg(ws, "message", "successfully connected")

            await self.__ws_handler.receive(ws)
        
        except Exception as e:
            print("Exception at Server.__join_handler")
            print(e)

        finally:
            self.__close_handler(ws)


    async def __msg_handler(self, ws: ServerConnection, msg: dict):
        parsed = self.__parse_message(msg)
        if parsed and parsed.get("type") == "message" and parsed.get("message"):
            print(f"[{ws.nickname}] {parsed["message"]}")
            await self.__ws_handler.broadcast_msg("message", f"[{ws.nickname}] {parsed['message']}")


    def __close_handler(self, ws: ServerConnection):
        self.__ws_handler.remove_client(ws)
        print("client disconencted")


    async def start(self):
        await self.__ws_handler.start()