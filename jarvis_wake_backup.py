import time
import sounddevice as sd
from scipy.io.wavfile import write
from openai import OpenAI
from dotenv import load_dotenv
from playsound3 import playsound

load_dotenv()

client = OpenAI()

SAMPLE_RATE = 44100

# How long JARVIS listens for each question
RECORD_SECONDS = 8


# ==========================================
# RECORD AUDIO
# ==========================================

def record_audio(filename, seconds):

    print("\n🎤 Listening... Speak now!")

    audio = sd.rec(
        int(seconds * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=1
    )

    sd.wait()

    write(
        filename,
        SAMPLE_RATE,
        audio
    )

    print("✅ Recording complete.")

    return filename


# ==========================================
# SPEECH TO TEXT
# ==========================================

def transcribe(filename):

    print("🧠 Understanding...")

    with open(filename, "rb") as audio_file:

        result = client.audio.transcriptions.create(
            model="gpt-4o-mini-transcribe",
            file=audio_file
        )

    return result.text.strip()


# ==========================================
# ASK JARVIS
# ==========================================

def ask_jarvis(question):

    print("🤖 JARVIS is thinking...")

    response = client.responses.create(
        model="gpt-5.6",
        input=question
    )

    return response.output_text


# ==========================================
# JARVIS SPEAKS
# ==========================================

def speak(text):

    print(f"\n🔊 JARVIS: {text}")

    speech_file = "jarvis_response.mp3"

    response = client.audio.speech.create(
        model="gpt-4o-mini-tts",
        voice="alloy",
        input=text
    )

    response.write_to_file(
        speech_file
    )

    try:

        playsound(speech_file)

    except Exception as e:

        print(
            "⚠️ Could not play audio:",
            e
        )


# ==========================================
# START JARVIS
# ==========================================

print("================================")
print("       JARVIS IS ONLINE")
print("================================")

print("🎙️ Continuous conversation mode")
print("Ask me anything.")
print("Say 'exit' or 'goodbye' to stop.")


# ==========================================
# CONTINUOUS CONVERSATION
# ==========================================

while True:

    # --------------------------------------
    # LISTEN
    # --------------------------------------

    audio_file = record_audio(
        "voice_input.wav",
        RECORD_SECONDS
    )


    # --------------------------------------
    # TRANSCRIBE
    # --------------------------------------

    question = transcribe(
        audio_file
    )

    print(
        f"\n👤 You: {question}"
    )


    # --------------------------------------
    # EMPTY AUDIO
    # --------------------------------------

    if not question:

        print(
            "⚠️ I didn't hear anything."
        )

        continue


    # --------------------------------------
    # EXIT
    # --------------------------------------

    command = question.lower().strip()

    if command in [
        "exit",
        "quit",
        "shutdown",
        "goodbye",
        "stop"
    ]:

        speak(
            "Goodbye. I'll be here when you need me."
        )

        break


    # --------------------------------------
    # ASK OPENAI
    # --------------------------------------

    answer = ask_jarvis(
        question
    )


    # --------------------------------------
    # SPEAK ANSWER
    # --------------------------------------

    speak(
        answer
    )


    # --------------------------------------
    # CONTINUE
    # --------------------------------------

    print(
        "\n🔄 Ready for your next question..."
    )