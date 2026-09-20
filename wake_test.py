import sounddevice as sd
from scipy.io.wavfile import write
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

SAMPLE_RATE = 44100
RECORD_SECONDS = 5


print("================================")
print("     JARVIS WAKE WORD TEST")
print("================================")

print("\n🎤 Get ready...")
input("Press ENTER, then say 'Hey Jarvis': ")

print("\n👂 Listening...")

audio = sd.rec(
    int(RECORD_SECONDS * SAMPLE_RATE),
    samplerate=SAMPLE_RATE,
    channels=1
)

sd.wait()

filename = "wake_word.wav"
write(filename, SAMPLE_RATE, audio)

print("✅ Recording complete.")

print("🧠 Transcribing...")

with open(filename, "rb") as audio_file:
    transcription = client.audio.transcriptions.create(
        model="gpt-4o-mini-transcribe",
        file=audio_file
    )

text = transcription.text.strip()

print(f"\n👂 Heard: {repr(text)}")

if "jarvis" in text.lower():
    print("\n🤖 JARVIS ACTIVATED!")
else:
    print("\n❌ JARVIS was not activated.")