import json
from json import JSONDecodeError


def write_messages(messages, channel_id: str):
    previous_messages = read_messages(channel_id)
    total_messages = _create_unique_set(messages, previous_messages)
    _save(total_messages, channel_id)


def read_messages(channel_id: str):
    try:
        with open(f'{channel_id}.json', 'r') as f:
            messages = json.load(f)
    except JSONDecodeError:
        messages = []
    return messages


def _create_unique_set(new_messages, previous_messages):
    return set(new_messages + previous_messages)


def _save(messages, channel_id):
    with open(f'{channel_id}.json', 'w') as f:
        json.dump(list(messages), f)
