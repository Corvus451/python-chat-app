import asyncio
from prompt_toolkit.widgets import TextArea, Frame
from prompt_toolkit.layout import Layout, HSplit, VSplit
from prompt_toolkit.application import Application
from prompt_toolkit.key_binding import KeyBindings

class UI:
    def __init__(self, input_handler):
        self.__input_handler = input_handler

        self.__input = TextArea(
            text="",
            multiline=False,
            focusable=True,
        )

        self.__message_display = TextArea(
            text="",
            multiline=True,
            focusable=False,
            read_only=True
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

        self.__kb = KeyBindings()

        @self.__kb.add('enter')
        def _(e):
            text = self.__input.text
            self.__input.text = ""
            if text:
                self.__input_handler(text, self)

        @self.__kb.add("c-c")
        def _(e):
            self.__app.exit()

        self.__app = Application(layout=self.__layout, key_bindings=self.__kb)


    async def run(self):
        await self.__app.run_async()

    def stop(self):
        self.__app.exit()

    def set_input_handler(self, handler):
        self.__input_handler = handler

    def set_message_display(self, text: str):
        self.__message_display.text = text

    def set_info_display(self, text: str):
        self.__info_display.text = text