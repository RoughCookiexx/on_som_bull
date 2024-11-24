import asyncio
import os
import time

import pygame

from openai import OpenAI

import chatgpt
from generate.sound_effect import generate_sound_effect
from generate.twitch import TwitchInput
from secrets import CHATGPT_API_KEY


async def sound_effect_task(description, directory):
    sound_effect_description = chatgpt.send_message_to_chatgpt(
        f"Take all of these messages, and compress them down into just the essence of what's been said. Take that essence and create a prompt for generating a sound effect. Use 200 characters or fewer. Make it a simple sound effect.Only return the description, no introduction. no conclusion. no 'here is your summary bullshit'. just get to the point. be as descriptive as possible.:  {','.join(description)}",
        client)
    sound_effect_filename = f'sound_effect.mp3'
    generate_sound_effect(sound_effect_description, sound_effect_filename)


async def task2():
    while True:
        print("Task 2 running")
        await asyncio.sleep(1)


async def task3():
    while True:
        print("Task 3 running")
        await asyncio.sleep(1)

async def create_on_som_bull(twitch_messages):
    tasks = [
        asyncio.create_task(sound_effect_task()),
        asyncio.create_task(task2()),
        asyncio.create_task(task3()),
    ]

    # Wait for all tasks to complete (they won't, in this example)
    await asyncio.gather(*tasks)
async def begin(jamsesh, chat_gpt_client):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(jamsesh.listen_to_redemptions())
    loop.run_until_complete(jamsesh.main_loop())

    out_directory = f'out{time.time()}'
    os.makedirs(out_directory, exist_ok=True)



if __name__ == '__main__':
    pygame.mixer.init()
    jam_sesh = TwitchInput()
    client = OpenAI(api_key=CHATGPT_API_KEY)
    asyncio.run(begin(client))
