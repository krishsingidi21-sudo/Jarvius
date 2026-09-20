
import time
import json
import sounddevice as sd
from scipy.io.wavfile import write
from openai import OpenAI
from dotenv import load_dotenv
from playsound3 import playsound

from jarvis_tools import (
    open_application,
    open_folder,
    create_folder,
    get_time
)

load_dotenv()

client = OpenAI()

SAMPLE_RATE = 44100

# How long JARVIUS listens for each question
RECORD_SECONDS = 8


# ==========================================
# TOOLS AVAILABLE TO JARVIUS
# ==========================================

TOOLS = [

    {
        "type": "function",
        "name": "open_application",
        "description": "Open an allowed Windows application such as Chrome, Notepad, Calculator, or File Explorer.",
        "parameters": {
            "type": "object",
            "properties": {
                "application_name": {
                    "type": "string",
                    "description": "The application to open. Examples: chrome, notepad, calculator, explorer."
                }
            },
            "required": ["application_name"]
        }
    },

    {
        "type": "function",
        "name": "open_folder",
        "description": "Open a folder on the Windows computer.",
        "parameters": {
            "type": "object",
            "properties": {
                "folder_path": {
                    "type": "string",
                    "description": "The full Windows path of the folder to open."
                }
            },
            "required": ["folder_path"]
        }
    },

    {
        "type": "function",
        "name": "create_folder",
        "description": "Create a folder on the Windows computer.",
        "parameters": {
            "type": "object",
            "properties": {
                "folder_path": {
                    "type": "string",
                    "description": "The full Windows path of the folder to create."
                }
            },
            "required": ["folder_path"]
        }
    },

    {
        "type": "function",
        "name": "get_time",
        "description": "Get the current local Windows time.",
        "parameters": {
            "type": "object",
            "properties": {}
        }
    }
]


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
# EXECUTE JARVIUS TOOL
# ==========================================

def execute_tool(name, arguments):

    print(f"\n🔧 JARVIUS TOOL: {name}")
    print(f"📋 Arguments: {arguments}")

    try:

        if name == "open_application":

            return open_application(
                arguments["application_name"]
            )

        elif name == "open_folder":

            return open_folder(
                arguments["folder_path"]
            )

        elif name == "create_folder":

            return create_folder(
                arguments["folder_path"]
            )

        elif name == "get_time":

            return get_time()

        else:

            return f"Unknown tool: {name}"

    except Exception as e:

        return f"Tool execution error: {e}"


# ==========================================
# ASK JARVIUS
# ==========================================

def ask_jarvius(question):

    print("\n🤖 JARVIUS is thinking...")

    response = client.responses.create(

        model="gpt-5.6",

        instructions="""
You are JARVIUS, a helpful Windows personal assistant.

You can answer normal questions.

You also have access to Windows tools.

Use a tool when the user asks you to perform an action
that one of your tools can perform.

Do not pretend that you performed an action if you did not
actually use the appropriate tool.

Keep your responses concise because they will be spoken aloud.
""",

        input=question,

        tools=TOOLS
    )

    # --------------------------------------
    # CHECK FOR TOOL CALLS
    # --------------------------------------

    while True:

        tool_calls = [
            item
            for item in response.output
            if item.type == "function_call"
        ]

        if not tool_calls:

            return response.output_text

        tool_outputs = []

        for tool_call in tool_calls:

            name = tool_call.name

            arguments = json.loads(
                tool_call.arguments
            )

            result = execute_tool(
                name,
                arguments
            )

            tool_outputs.append({

                "type": "function_call_output",

                "call_id": tool_call.call_id,

                "output": result

            })

        # ----------------------------------
        # SEND TOOL RESULT BACK TO OPENAI
        # ----------------------------------

        response = client.responses.create(

            model="gpt-5.6",

            previous_response_id=response.id,

            input=tool_outputs,

            tools=TOOLS

        )


# ==========================================
# JARVIUS SPEAKS
# ==========================================

def speak(text):

    print(f"\n🔊 JARVIUS: {text}")

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

        playsound(
            speech_file
        )

    except Exception as e:

        print(
            "⚠️ Could not play audio:",
            e
        )


# ==========================================
# START JARVIUS
# ==========================================

print("================================")
print("       JARVIUS IS ONLINE")
print("================================")

print("🎙️ Continuous conversation mode")
print("🧰 Windows tools enabled")
print("Ask me anything.")

print(
    "Say 'exit' or 'goodbye' to stop."
)

print("Jarvius is online. I'm ready to listen.")
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
    # ASK JARVIUS
    # --------------------------------------

    answer = ask_jarvius(
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