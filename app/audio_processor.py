from faster_whisper import WhisperModel
import base64
import numpy as np
from pydub import AudioSegment
import io

class AudioProcessor:
    def __init__(self, model_size="base"):
        self.model = WhisperModel(model_size, device="cpu", compute_type="int8")

    def transcribe(self, audio_data):
        if not audio_data or "audio" not in audio_data:
            return ""
        # Decode base64 audio
        audio_bytes = base64.b64decode(audio_data["audio"])
        if not audio_bytes:
            return ""
        audio_stream = io.BytesIO(audio_bytes)
        
        # Convert WebM to WAV using pydub
        audio = AudioSegment.from_file(audio_stream, format="webm")
        wav_io = io.BytesIO()
        audio.export(wav_io, format="wav")
        wav_io.seek(0)
        
        # Convert to numpy array
        audio_array = np.frombuffer(wav_io.getvalue(), dtype=np.int16)
        audio_float32 = audio_array.astype(np.float32) / 32768.0

        # Transcribe
        segments, _ = self.model.transcribe(audio_float32, task="translate", language="en")
        return " ".join([segment.text for segment in segments])