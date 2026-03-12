import asyncio

from app import App
from ws.wshandler import WsHandler
from ui.ui import UI
from ui.keybinder import Key_binder
from utility.logger import Logger
from command_registry.command_registry import Command_registry
from command_registry.command_list import commands


async def main():
    command_registry = Command_registry()
    logger = Logger("testlog.txt")
    ui = UI()
    ws_handler = WsHandler(logger, ui)
    key_binder = Key_binder(ui, ws_handler)
    app = App(logger, ws_handler, ui, key_binder, command_registry, commands)

    await app.run()


if __name__ == "__main__":
    asyncio.run(main())