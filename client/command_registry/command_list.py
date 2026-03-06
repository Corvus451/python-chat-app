async def cmd_quit(args, app):
    """exit program"""
    app.ui.stop()

async def cmd_connect(args, app):
    """(/connect <address> <nickname>) connect to a server"""
    address = args[1]
    nickname = args[2]
    await app.ws_handler.connect(address, nickname)

async def cmd_disconnect(args, app):
    """disconnect from a server"""
    await app.ws_handler.disconnect()

async def cmd_help(args, app):
    """print this list"""
    app.command_registry.list_commands(app)

commands = {
    "/quit": cmd_quit,
    "/connect": cmd_connect,
    "/disconnect": cmd_disconnect,
    "/help": cmd_help,
}