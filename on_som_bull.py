import asyncio
import glob
import os
import time

import pygame
import requests
from mutagen.mp3 import MP3

from openai import OpenAI

import chatgpt
from generate.image import queue_image_generation
from generate.song import generate_song, download_audio_stream
from generate.sound_effect import generate_sound_effect
from generate.twitch import TwitchInput
from secrets import CHATGPT_API_KEY
import time

import pygame
import speech_recognition as sr

# from gtts import gTTS


class OnSomBull:

    def __init__(self):
        self.chat_gpt_client = OpenAI(api_key=CHATGPT_API_KEY)
        self.recognizer = sr.Recognizer()
        self.all_messages = ''

    async def sound_effect_task(self, directory):
        sound_effect_description = chatgpt.send_message_to_chatgpt(
            f"Take all of these messages, and compress them down into just the essence of what's been said. Take that essence and create a prompt for generating a sound effect. Use 200 characters or fewer. Make it a simple sound effect.Only return the description, no introduction. no conclusion. no 'here is your summary bullshit'. just get to the point. be as descriptive as possible.:  {','.join(self.all_messages)}",
            self.chat_gpt_client)
        sound_effect_filename = f'{directory}\\sound_effect.mp3'
        await generate_sound_effect(sound_effect_description, sound_effect_filename)

    async def song_task(self, directory):
        song_description = chatgpt.send_message_to_chatgpt(
            f"Summarize all of this content and turn it into a song description. Include the genre and emotions this song should invoke. Keep the description between 100 and 200 characters. Only return the summary, no introduction. no conclusion. no 'here is your summary bullshit'. just get to the point. be as descriptive as possible.:  {','.join(self.all_messages)}",
            self.chat_gpt_client)

        song_title = chatgpt.send_message_to_chatgpt(
            f"Take the following song description and give me back a title. respond with ONLY the title. :  {song_description}",
            self.chat_gpt_client)

        song_data = await generate_song(song_description)
        await download_audio_stream(song_data[0]['audio_url'], f'{directory}\\song.mp3')
        image_url = song_data[0]['image_url']
        lyrics = song_data[0]['lyric']

        print(f'{song_title}: {song_description}')

    async def prep_sierra(self):
        request_message = '. '.join(self.all_messages)

        chat_payload = {
            "character": "Other Poop",  # Example character name, change as needed
            "message": request_message,  # Example message, change as needed
            "source": "on_som_bull"  # Example source, change as needed
        }
        headers = {
            "Content-Type": "application/json"
        }

        response_chat = requests.post("http://localhost:8008/chat", json=chat_payload, headers=headers)
        print("Response from /chat:", response_chat.status_code, response_chat.text)

    async def create_on_som_bull(self):

        directory = f'out\\{time.strftime("%y%m%d%H%M%S", time.localtime())}'
        os.makedirs(directory, exist_ok=True)

        tasks = [

            # self.song_task(directory),
            self.sound_effect_task(directory),
            self.prep_sierra()
        ]

        await asyncio.gather(*tasks)
        await self.play_on_som_bull(directory)

    async def play_on_som_bull(self, path):
        audio_length = MP3(f'{path}/sound_effect.mp3').info.length
        pygame.mixer.music.load(f'{path}/sound_effect.mp3')
        pygame.mixer.music.play()
        await asyncio.sleep(audio_length)
        pygame.mixer.music.unload()

        sierra_file_name = self.get_latest_mp3()
        audio_length = MP3(f'{sierra_file_name}').info.length
        await self.trigger_sierra()
        await asyncio.sleep(audio_length)

        audio_length = MP3(f'{path}/sound_effect.mp3').info.length
        pygame.mixer.music.load(f'{path}/song.mp3')
        pygame.mixer.music.play()
        await asyncio.sleep(audio_length)
        pygame.mixer.music.unload()

    def add_message(self, message):
        self.all_messages = f'{self.all_messages}. {message}'

    async def trigger_sierra(self):
        response_chat = requests.post("http://localhost:8008/play")
        print("Response from /chat:", response_chat.status_code, response_chat.text)

    def get_latest_mp3(self):
        # Get a list of all mp3 files in the directory
        mp3_files = glob.glob(os.path.join('C:\\Users\\Tommy\\PycharmProjects\\sierra-v3 - Copy\\temp', "*.mp3"))

        # If there are no mp3 files, return None
        if not mp3_files:
            return None

        # Sort by modification time and get the latest one
        latest_mp3 = max(mp3_files, key=os.path.getmtime)
        return latest_mp3

    async def listen(self):
        await asyncio.sleep(0.1)
        with sr.Microphone() as source:
            print("Listening...")

            self.recognizer.adjust_for_ambient_noise(source, duration=1)

            last_run_time = time.time()

            while True:
                try:
                    if time.time() > last_run_time + 15:
                        await self.create_on_som_bull()
                        last_run_time = time.time()
                    audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=10)
                    spoken_words = self.recognizer.recognize_google(audio).lower()
                    self.all_messages = f'{self.all_messages}. {spoken_words}'
                    print(f"Recognized: {spoken_words}")

                except sr.WaitTimeoutError:
                    print("Listening timeout, still listening...")
                    # recognized_label.config(text="Listening timeout, still listening...")
                except sr.UnknownValueError:
                    print("Couldn't understand the audio, try again...")
                    # recognized_label.config(text="Couldn't understand, try again...")
                except sr.RequestError as e:
                    print(f"Error with the API: {e}")
                    # recognized_label.config(text="API error")
                    break
    async def begin(self):
        twitch = TwitchInput(self.add_message)

        tasks = [
            twitch.begin(),
            self.listen()
        ]

        await asyncio.gather(*tasks)
        # await ensemble.create_on_som_bull(
        #     ['this is a test message', 'good idea, we should test', 'you stink why does anyone watch this shit?'])


if __name__ == '__main__':
    ensemble = OnSomBull()
    pygame.mixer.init()
    asyncio.run(ensemble.begin())
