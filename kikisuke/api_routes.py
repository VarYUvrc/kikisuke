
import logging
from fastapi import APIRouter, UploadFile, File
import speech_recognition as sr
from pydub import AudioSegment
import io
import reflex as rx

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

api_router = APIRouter()

@api_router.post("/handle_audio_chunk")
async def handle_audio_chunk(audio_file: UploadFile = File(...)):
    logging.info("Received audio chunk for transcription.")
    recognizer = sr.Recognizer()
    text = ""
    try:
        contents = await audio_file.read()
        logging.info(f"Audio file received: {audio_file.filename}, size: {len(contents)} bytes")
        # Assuming the chunk is a webm file, we need to convert it to wav
        audio_segment = AudioSegment.from_file(io.BytesIO(contents), format="webm")
        wav_data = io.BytesIO()
        audio_segment.export(wav_data, format="wav")
        wav_data.seek(0)
        logging.info("Audio converted to WAV format.")
        with sr.AudioFile(wav_data) as source:
            audio = recognizer.record(source)
        
        text = recognizer.recognize_google(audio, language='ja-JP')
        logging.info(f"Transcription successful. Text: {text}")
    except sr.UnknownValueError:
        logging.warning("Speech Recognition could not understand audio.")
        text = "Could not understand audio."
    except sr.RequestError as e:
        logging.error(f"Could not request results from Google Speech Recognition service; {e}")
        text = "Speech recognition service error."
    except Exception as e:
        logging.error(f"Error transcribing audio: {e}", exc_info=True)
        text = "Could not transcribe audio due to an unexpected error."
    
    return {"transcribed_text": text}
