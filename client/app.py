import asyncio
import json

from ws.wshandler import WsHandler
from ui.ui import UI
from utility.logger import Logger


class App:
    def __init__(self, ui: UI, logger: Logger):
        self.__ws_handler = WsHandler(self.msg_handler, self.close_handler, logger)
        self.__ui = ui
        self.__logger = logger

        self.__ui.set_input_handler(self.input_handler)

    def msg_handler(self, msg: str):
        parsed: dict = json.loads(msg)
        if parsed.get("message"):
            self.__ui.add_message(parsed["message"])

    def close_handler(self):
        self.__ui.add_message("Connection closed.")

    async def cmd_handler(self, text: str):
        cmd = text.split(" ")
        if cmd[0] == "/quit":
            await self.__ws_handler.disconnect()
            self.__ui.stop()
        elif cmd[0] == "/connect":
            await self.__ws_handler.connect(cmd[1], cmd[2])
        elif cmd[0] == "/disconnect":
            await self.__ws_handler.disconnect()

    async def input_handler(self, text: str):
        if text.startswith("/"):
            await self.cmd_handler(text)
        
        elif self.__ws_handler.is_connected():
            await self.__ws_handler.send_message(text)

        else:
            self.__ui.add_message(text)


    async def run(self):
        await self.__ui.run()

async def main():
    
    logger = Logger("testlog.txt")
    ui = UI()
    app = App(ui, logger)
    await app.run()


if __name__ == "__main__":
    asyncio.run(main())