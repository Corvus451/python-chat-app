class Command_registry:

    def __init__(self):
        self.__registry = {}    

    def command(self, name: str):
        def decorator(func):
            self.__registry[name] = func
            return func
        return decorator
    
    async def run_command(self, text: str, app):
        args = text.split()
        cmd = self.__registry.get(args[0])
        if not cmd:
            return False
        await cmd(args, app)

    def register_commands(self, commands):
        if commands and type(commands) == dict:
            for key, value in commands.items():
                self.command(key)(value)

    def list_commands(self, app):
        for key, value in self.__registry.items():
            app.ui.add_message(f"{key} : {value.__doc__}")


    