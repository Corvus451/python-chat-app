import asyncio
import json

from ws.wshandler import WsHandler
from ui.ui import UI
from ui.keybinder import Key_binder
from utility.logger import Logger
from command_registry.command_list import commands
from command_registry.command_registry import Command_registry


class App:
    def __init__(self, logger: Logger, ws_handler: WsHandler, ui: UI, key_binder: Key_binder, command_registry: Command_registry, commands):
        self.__logger = logger
        self.ws_handler = ws_handler
        self.ui = ui
        self.__key_binder = key_binder
        self.command_registry = command_registry

        self.ui.set_input_handler(self.input_handler)
        self.ui.set_keybindings(self.__key_binder.bind_keys())
        self.ws_handler.set_handlers(self.msg_handler, self.close_handler)
        self.command_registry.register_commands(commands)


    def msg_handler(self, msg: str):
        parsed: dict = json.loads(msg)
        if parsed.get("message"):
            self.ui.add_message(parsed["message"])

    async def connect(self, address: str, nickname: str):
        if await self.ws_handler.connect(address):
            connect_msg = json.dumps({
                "type": "join",
                "nickname": nickname
            })

            await self.ws_handler.send_message(connect_msg)
            success = await self.ws_handler.get_msg()

            if not success:
                self.ws_handler.clear_ws()
                return
            
            self.ui.add_message("Successfully connected")

            asyncio.create_task(self.ws_handler.listen())


    def close_handler(self):
        self.ui.add_message("Connection closed.")

    def create_message(self, msg_type: str, text: str):
        return json.dumps({
        "type": msg_type,
        msg_type: text
        })

    async def input_handler(self, text: str):
        if text.startswith("/"):
            await self.command_registry.run_command(text, self)
        
        elif self.ws_handler.is_connected():
            msg = self.create_message("message", text)
            await self.ws_handler.send_message(msg)

        else:
            self.ui.add_message(text)


    async def run(self):
        await self.ui.run()
