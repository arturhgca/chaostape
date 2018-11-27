from datetime import datetime
from typing import List

from discord import Channel

from chaostape import bot
from chaostape.persistence import read_messages, write_messages


@bot.client.event
async def on_ready():
    await bot.on_ready()
    for channel_id in bot.settings.channels:
        print(f'Monitoring channel {channel_id}')
        await _dump_messages_from_channel(bot.client.get_channel(channel_id), bot.settings.checkpoint_datetime)
    bot.settings.update()


@bot.client.command(name='full_mixtape', pass_context=True)
async def dump_channel_links(context):
    # TODO: improve presentation
    # TODO: automated YouTube playlist
    await bot.client.say(f'```\n{read_messages(context.message.channel.id)}\n```')


@bot.client.command(name='add_to_deck', pass_context=True)
async def monitor_channel(context):
    if context.message.channel.id in bot.settings.channels:
        await bot.client.say('This channel is already on deck!')
        return
    bot.settings.add_channel(context.message.channel.id)
    await _dump_messages_from_channel(context.message.channel)
    await bot.client.say('This channel has been added to the deck! Mixtapes will be available shortly.')
    print(
        f'Monitoring channel {context.message.channel.server}:{context.message.channel.name} with ID {context.message.channel.id}')


async def _dump_messages_from_channel(channel: Channel, checkpoint_datetime: datetime = None):
    messages = []
    args = {
        'channel': channel
    }
    if checkpoint_datetime:
        args['after'] = checkpoint_datetime
    async for message in bot.client.logs_from(**args):
        messages.append(message.clean_content)
    messages = _pick_messages(messages)
    write_messages(messages, channel.id)


def _pick_messages(messages: List[str]):
    return [message for message in messages if
            (
                    ('https://youtube.com/' in message)
                    or ('https://www.youtube.com/' in message)
                    or ('https://youtu.be/' in message)
            )]
