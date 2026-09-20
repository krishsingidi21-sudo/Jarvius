import os
import sounddevice as sd
from scipy.io.wavfile import write
from openai import OpenAI
from dotenv import load_dotenv
from playsound3 import playsound

load_dotenv()

client = OpenAI()

SAMPLE_RATE = 44100
RECORD_SECONDS = 5


def record_audio():
    print("\n🎤 Listening... Speak now!")

    audio = sd.rec(
        int(RECORD_SECONDS * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=1
    )

    sd.wait()

    filename = "voice_input.wav"
    write(filename, SAMPLE_RATE, audio)

    print("✅ Recording complete.")

    return filename


def transcribe_audio(filename):
    print("🧠 Understanding what you said...")

    with open(filename, "rb") as audio_file:
        transcription = client.audio.transcriptions.create(
            model="gpt-4o-mini-transcribe",
            file=audio_file
        )

    text = transcription.text.strip()

    return text


def ask_jarvis(text):
    # Prevent an empty request from being sent to OpenAI
    if not text:
        return "I didn't hear anything. Please try again."

    print("🤖 JARVIS is thinking...")

    response = client.responses.create(
        model="gpt-5.6",
        input=text
    )

    return response.output_text


def speak(text):
    print(f"\n🔊 JARVIS: {text}")

    speech_file = "jarvis_response.mp3"

    response = client.audio.speech.create(
        model="gpt-4o-mini-tts",
        voice="alloy",
        input=text
    )

    response.write_to_file(speech_file)

    try:
        playsound(speech_file)
    except Exception as e:
        print("⚠️ Could not play JARVIS audio:", e)


print("================================")
print("       JARVIS IS ONLINE")
print("================================")

while True:

    command = input(
        "\nPress ENTER to talk to JARVIS, "
        "or type 'exit' to quit: "
    )

    if command.lower().strip() == "exit":
        print("JARVIS: Goodbye!")
        break

    audio_file = record_audio()

    text = transcribe_audio(audio_file)

    print(f"\nYou: {repr(text)}")

    # Don't send empty transcription to the AI
    if not text:
        print("JARVIS: I didn't hear anything. Please try again.")
        continue

    answer = ask_jarvis(text)

    print(f"\n🤖 JARVIS: {answer}")

    speak(answer)