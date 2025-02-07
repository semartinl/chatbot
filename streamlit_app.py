import streamlit as st
from io import BytesIO
import soundfile as sf
from streamlit_webrtc import webrtc_streamer, AudioProcessorBase
from streamlit_mic_recorder import mic_recorder
import IPython.display as ipd
import av


# Show title and description.
st.title("💬 Chatbot")
st.write(
    "This is a simple chatbot that uses OpenAI's GPT-3.5 model to generate responses. "
    "To use this app, you need to provide an OpenAI API key, which you can get [here](https://platform.openai.com/account/api-keys). "
    "You can also learn how to build this app step by step by [following our tutorial](https://docs.streamlit.io/develop/tutorials/llms/build-conversational-apps)."
)

def callback():
    if st.session_state.my_recorder_output:
        audio_bytes = st.session_state.my_recorder_output['bytes']
        st.audio(audio_bytes)

# Seleccionar modo de entrada
input_mode = st.radio("Selecciona el modo de entrada de audio:", ("Grabar Audio", "Subir Archivo de Audio"))

# Funciones de utilidad para grabación y carga
def process_audio(audio_data):
    # Procesamiento ficticio para la IA Text2Speech
    st.success("Audio recibido. Procesando con el modelo de IA...")
    # Simular una respuesta en audio (aquí debería ir la llamada real al modelo de IA)
    st.audio(audio_data, format='audio/wav')

# Procesador de audio para capturar el audio en tiempo real
class AudioProcessor(AudioProcessorBase):
    def recv(self, frame: av.AudioFrame) -> av.AudioFrame:
        audio_data = frame.to_ndarray()
        buffer = BytesIO()
        sf.write(buffer, audio_data, frame.sample_rate, format='WAV')
        process_audio(buffer.getvalue())
        return frame

# # Opción para grabar audio usando streamlit-webrtc
# def record_audio():
#     st.info("Presiona 'Start' para comenzar a grabar tu voz.")
#     webrtc_streamer(key="audio", audio_receiver_size=1024, media_stream_constraints={"audio": True, "video": False}, 
#                     audio_processor_factory=AudioProcessor)
def record_audio():
    audio = mic_recorder(
        start_prompt="Start recording",
        stop_prompt="Stop recording",
        just_once=False,
        format="wav",
        key="recorder"
    )
    # audio = mic_recorder(start_prompt="⏺️", stop_prompt="⏹️", key='recorder')
    return audio
# Opción para subir archivo de audio
def upload_audio():
    audio_file = st.file_uploader("Sube tu archivo de audio", type=["wav", "mp3", "ogg"])

    if audio_file is not None:
        audio_data = audio_file.read()
        st.audio(audio_data)
        process_audio(audio_data)

# Lógica principal
if input_mode == "Grabar Audio":
    ex_audio = record_audio()
    
    # Se muestra por pantalla el audio a analizar
    if ex_audio:
        st.audio(ex_audio['bytes'])



else:
    upload_audio()

