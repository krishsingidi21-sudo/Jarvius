import sounddevice as sd
from scipy.io.wavfile import write

sample_rate = 44100
duration = 5

print("🎤 Recording for 5 seconds...")
audio = sd.rec(
    int(duration * sample_rate),
    samplerate=sample_rate,
    channels=1
)

sd.wait()

write("test_recording.wav", sample_rate, audio)

print("✅ Recording saved as test_recording.wav")