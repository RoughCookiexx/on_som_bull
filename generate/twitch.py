from datetime import datetime

from openai import OpenAI
from twitchAPI.eventsub.websocket import EventSubWebsocket
from twitchAPI.object.eventsub import ChatMessage
from twitchAPI.twitch import Twitch
from twitchAPI.oauth import UserAuthenticator, UserAuthenticationStorageHelper
from twitchAPI.type import AuthScope, ChatEvent
from twitchAPI.chat import Chat, EventData

import asyncio
import pygame
import yt_dlp

import chatgpt
from secrets import CLIENT_ID, CLIENT_SECRET

# Replace these values with your client_id and client_secret
TARGET_CHANNEL_ID = '38606166'
ALL_MESSAGES = ''


class TwitchInput:
    TARGET_CHANNEL_ID = '38606166'
    TARGET_SCOPES = [AuthScope.CHAT_READ]

    def __init__(self, callback):
        self.chat_messages = []
        self.add_ensemble_message = callback

    async def read_message(self, message: ChatMessage):
        if 'Cheer' not in message.text:
            self.add_ensemble_message(message)

        print(self.chat_messages)

    async def on_ready(self, ready_event: EventData):
        await ready_event.chat.join_room('roughcookie')

    async def begin(self):
        await asyncio.sleep(.1)
        twitch = await Twitch(CLIENT_ID, CLIENT_SECRET)
        auth = UserAuthenticator(twitch, [AuthScope.CHAT_READ, AuthScope.CHAT_EDIT])

        # Authenticate the user and get the token
        token, refresh_token = await auth.authenticate()

        # Set the token
        await twitch.set_user_authentication(token, [AuthScope.CHAT_READ], refresh_token)

        chat = await Chat(twitch)
        chat.register_event(ChatEvent.READY, self.on_ready)
        chat.register_event(ChatEvent.MESSAGE, self.read_message)
        chat.start()

        # Keep it alive
        while True:
            await asyncio.sleep(1)


if __name__ == '__main__':
    pygame.mixer.init()
