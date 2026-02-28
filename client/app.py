import asyncio
from ws.wshandler import WsHandler
from ui.ui import UI
from utility.logger import Logger


def msg_handler(msg: str):
    pass

def close_handler():
    pass

def input_handler(text: str, ui: UI):
    if text == "/quit":
        ui.stop()
    else:
        ui.set_message_display(text=text)



async def main():
    
    logger = Logger("testlog.txt")
    # wsHandler = WsHandler(msg_handler, close_handler, logger)
    ui = UI(input_handler)

    await ui.run()


if __name__ == "__main__":
    asyncio.run(main())