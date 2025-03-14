import streamlit as st
import os
import asyncio
from faster_whisper import WhisperModel

# Fix pour éviter les erreurs asyncio sur Streamlit Cloud
try:
    asyncio.get_running_loop()
except RuntimeError:
    asyncio.set_event_loop(asyncio.new_event_loop())

def transcribe_audio(file_path, model_size="tiny"):
    model = WhisperModel(model_size, compute_type="int8")
    segments, _ = model.transcribe(file_path)
    transcript = " ".join(segment.text for segment in segments)
    return transcript

# Configuration Streamlit
st.set_page_config(page_title="Transcription Audio avec Faster Whisper", layout="centered")
st.title("📝 Transcription Audio avec Faster Whisper")

uploaded_file = st.file_uploader("Choisissez un fichier audio", type=["mp3", "wav", "m4a", "ogg", "flac"]) 

if uploaded_file is not None:
    st.audio(uploaded_file, format="audio/mpeg")
    
    # Sauvegarde temporaire du fichier
    file_path = os.path.join("temp_audio", uploaded_file.name)
    os.makedirs("temp_audio", exist_ok=True)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    st.write("🔄 Transcription en cours...")
    
    # Transcription avec Faster Whisper
    transcript = transcribe_audio(file_path)
    
    st.success("✅ Transcription terminée !")
    st.text_area("Texte transcrit :", transcript, height=200)
    
    # Permettre le téléchargement du texte
    txt_file = "transcription.txt"
    with open(txt_file, "w") as f:
        f.write(transcript)
    
    st.download_button("💾 Télécharger la transcription", txt_file, file_name="transcription.txt")
    
    # Nettoyage des fichiers temporaires
    os.remove(file_path)
