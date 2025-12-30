import threading
import whisper
import os

# Lazy load the model when needed
_model = None
_model_lock = threading.Lock()

# Model name from environment or default to 'base'
WHISPER_MODEL = os.getenv('WHISPER_MODEL', 'base')

def get_model():
    """
    Thread-safe lazy loading of the Whisper model.
    Model name can be configured via WHISPER_MODEL environment variable.
    """
    global _model
    if _model is None:
        with _model_lock:
            # Double-check pattern to avoid race conditions
            if _model is None:
                _model = whisper.load_model(WHISPER_MODEL)
    return _model

def transcribe_audio(file_path: str) -> str:
    model = get_model()
    result = model.transcribe(file_path, language="en")
    return result.get("text", "")