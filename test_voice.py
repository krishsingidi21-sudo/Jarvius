import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

print("Creating JARVIS voice...")

response = client.audio.speech.create(
    model="gpt-4o-mini-tts",
    voice="alloy",
    input="Hello! I am Jarvis. Your voice assistant is working."
)

response.write_to_file("jarvis_voice.mp3")

print("Voice file created successfully: jarvis_voice.mp3")