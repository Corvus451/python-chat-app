import asyncio
from prompt_toolkit.widgets import TextArea, Frame
from prompt_toolkit.layout import Layout, HSplit, VSplit
from prompt_toolkit.application import Application
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.shortcuts import clear

class UI:
    def __init__(self):
        self.__input_handler = None
        self.__message_history = []
        self.__app = Application()
        # self.__screen_height = self.__app.output.get_size().rows
        # self.__max_msg = self.__screen_height - 10
        # self.__app.on_invalidate += self.__update_max_msg

        self.__input = TextArea(
            text="",
            multiline=False,
            focusable=True,
        )

        self.__message_display = TextArea(
            text="",
            multiline=True,
            focusable=False,
            read_only=True,
        )

        self.__info_display = TextArea(
            text="",
            multiline=True,
            focusable=False,
            read_only=True
        )

        self.__layout = Layout(
            HSplit([
                VSplit([
                    Frame(self.__message_display, "messages"),
                    Frame(self.__info_display, "info")
                ]),
                Frame(self.__input, "Enter command/message")
            ])
        )
        self.__app.layout = self.__layout

        # self.__kb = KeyBindings()

        # @self.__kb.add('enter')
        # def _(e):
        #     self.on_input()

        # @self.__kb.add("c-c")
        # def _(e):
        #     self.__app.exit()

        # self.__app.key_bindings = self.__kb

    async def run(self):
        clear()
        await self.__app.run_async()
        clear()

    def stop(self):
        self.__app.exit()

    def set_input_handler(self, handler):
        self.__input_handler = handler

    def on_input(self):
        text = self.__input.text
        self.__input.text = ""
        if self.__input_handler and text:
            asyncio.create_task(self.__input_handler(text))

    def add_message(self, text: str):
        self.__message_history.append(text)
        self.__message_display.text = '\n'.join(self.__message_history[-10:])

    def set_info(self, text: str):
        self.__info_display.text = text

    def set_keybindings(self, kb: KeyBindings):
        self.__app.key_bindings = kb
