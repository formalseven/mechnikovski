from pathlib import Path
from importlib import import_module
import traceback
from bot.states.StateManager import StateManager

def _loadHandlers(basic_path: str):
    current_dir = Path(__file__).parent / "routes" / basic_path

    routes = {}

    for file in current_dir.glob("*.py"):
        module_name = f"{__package__}.routes.{basic_path}.{file.stem}"
        modul = import_module(module_name)
        routes[modul.name] = modul.exec

    return routes

def route(bot):
    commands = _loadHandlers("commands")
    callbacks = _loadHandlers("callbacks")
    states = _loadHandlers("states")

    @bot.message_handler(content_types=[
        'text',
        'audio',
        'document',
        'photo',
        'sticker',
        'video',
        'video_note',
        'voice',
        'contact',
        'animation',
    ])
    async def handle(message):
        if message.text in tuple(commands.keys()):
            try:
                await commands[message.text](bot, message)
            except Exception as err:
                print("Error | Command handler error")
                print(err)
                traceback.print_exc()
            return

        state = StateManager.get(message.from_user.id)
        if state is not None:
            try:
                await states.get(state.get("action"))(bot, message, state.get("args"))
            except Exception as err:
                print("Error | State handler error")
                print(err)
                traceback.print_exc()
            return

    @bot.callback_query_handler()
    async def handle(query):
        data = query.data.split(":")
        callback = callbacks.get(data[0])
        if not callback:
            return

        data.pop(0)
        try:
            await callback(bot, query, data)
        except Exception as err:
            print("Error | Callback handler error")
            print(err)
            traceback.print_exc()

        