from datetime import datetime
import json
from typing import List


class Settings:
    token: str
    channels: List[str]
    checkpoint_datetime: datetime

    def __init__(self):
        settings = self._read()
        self.token = settings.get('token')
        self.channels = settings.get('channels')
        if settings.get('checkpoint_timestamp'):
            self.checkpoint_datetime = datetime.fromtimestamp(settings.get('checkpoint_timestamp'))
        else:
            self.checkpoint_datetime = None

    def add_channel(self, channel_id: str):
        self.channels.append(channel_id)
        self.update()

    def update(self):
        self.checkpoint_datetime = datetime.now()
        self._save()

    def _read(self):
        with open('settings.json', 'r') as f:
            return json.load(f)

    def _save(self):
        with open('settings.json', 'w') as f:
            json.dump(self._to_json(), f)

    def _to_json(self):
        return {
            'token': self.token,
            'channels': self.channels,
            'checkpoint_timestamp': self.checkpoint_datetime.timestamp()
        }


settings = Settings()
