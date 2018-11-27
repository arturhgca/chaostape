from discord import Game
from discord.ext.commands import Bot

from .settings import settings as settings

COMMAND_PREFIX = ('!')

client = Bot(command_prefix=COMMAND_PREFIX)


def start():
    client.run(settings.token)


async def on_ready():
    await client.change_presence(game=Game(name='with mixtapes'))
    print(f'Logged in as {client.user.name}')
