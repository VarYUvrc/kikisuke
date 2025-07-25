import reflex as rx
import logging
from kikisuke.api_routes import api_router

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class State(rx.State):
    """The app state."""
    is_recording: bool = False
    transcribed_text: str = ""

    def toggle_recording(self):
        self.is_recording = not self.is_recording

    def start_recording(self):
        logging.info("Attempting to start recording.")
        return rx.call_script("startRecording()")

    def stop_recording(self):
        logging.info("Attempting to stop recording.")
        return rx.call_script("stopRecording()")

    def set_transcribed_text(self, text: str):
        logging.info(f"Transcribed text received: {text}")
        self.transcribed_text = text

def index() -> rx.Component:
    return rx.container(
        rx.vstack(
            rx.heading("Voice-to-Text App", size="9"),
            rx.button(
                rx.cond(State.is_recording, "Stop Recording", "Start Recording"),
                on_click=[State.toggle_recording, rx.cond(State.is_recording, State.stop_recording, State.start_recording)],
                width="100%",
            ),
            rx.text(
                rx.cond(State.is_recording, "Recording...", "Click to start"),
                margin_top="1em",
            ),
            rx.text_area(
                value=State.transcribed_text,
                placeholder="Transcribed text will appear here...",
                width="100%",
                height="200px",
                margin_top="1em",
            ),
            spacing="5",
            justify="center",
            min_height="85vh",
        ),
    )


app = rx.App(head_components=[rx.script(src="/custom.js")])
app.api = api_router
app.add_page(index)
