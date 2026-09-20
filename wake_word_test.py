from openwakeword.model import Model
import numpy as np
from scipy.io.wavfile import read
from scipy.signal import resample_poly

print("Loading Hey Jarvis model...")

model = Model(
    wakeword_models=["hey_jarvis_v0.1.onnx"],
    inference_framework="onnx"
)

print("✅ Model loaded.")

sample_rate, audio = read("test_recording.wav")

if len(audio.shape) > 1:
    audio = audio[:, 0]

audio = audio.astype(np.float32)

if sample_rate != 16000:
    audio = resample_poly(audio, 16000, sample_rate)

audio = np.clip(audio, -32768, 32767).astype(np.int16)

print("\nChecking model output...")

chunk_size = 1280

for i in range(0, len(audio), chunk_size):

    chunk = audio[i:i + chunk_size]

    if len(chunk) < chunk_size:
        break

    prediction = model.predict(chunk)

    print(prediction)

print("\nTest complete.")