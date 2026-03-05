import asyncio

from ui.ui import UI
from ws.wshandler import WsHandler

from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.filters import FilterOrBool
from prompt_toolkit.filters import has_focus

class Key_binder:
    def __init__(self, ui: UI, ws: WsHandler):
        self.__ui = ui
        self.__ws_handler = ws

        self.__bind_list = {
            "c-c": self.__bind_exit_program,
            "enter": self.__bind_enter_input,
            "f1": self.__bind_test,
            "f2": self.__bind_disconnect,
        }

    def bind_keys(self) -> KeyBindings:
        kb = KeyBindings()

        for key, value in self.__bind_list.items():

            kb.add(key)(value)
        
        return kb

    def __bind_exit_program(self, e):
        self.__ui.stop()

    def __bind_enter_input(self, e):
        self.__ui.on_input()
    
    def __bind_test(self, e):
        self.__ui.add_message("this is from the keybind")

    def __bind_disconnect(self, e):
        asyncio.create_task(self.__ws_handler.disconnect())