import asyncio

from elevenlabs.client import ElevenLabs

from secrets import ELEVENLABS_API_KEY

elevenlabs = ElevenLabs(api_key=ELEVENLABS_API_KEY)


async def generate_sound_effect(text: str, output_path: str):
    print(f"Generating sound effect: {text}")
    await asyncio.sleep(3)

    result = elevenlabs.text_to_sound_effects.convert(
        text=text,
        # duration_seconds=12,
        prompt_influence=0.5,  # Optional, if not provided will use the default value of 0.3
    )

    with open(output_path, "wb") as f:
        for chunk in result:
            f.write(chunk)

    print(f"Audio saved to {output_path}")
