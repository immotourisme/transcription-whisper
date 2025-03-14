import streamlit as st
import whisper
import torch
import os
import os
import ffmpeg

# Assurer que FFmpeg est bien disponible
os.environ["PATH"] += os.pathsep + "/usr/bin/"

def transcribe_audio(file_path, model_size="tiny"):
    model = whisper.load_model(model_size)
    result = model.transcribe(file_path)
    return result["text"]

# Configuration Streamlit
st.set_page_config(page_title="Transcription Audio avec Whisper", layout="centered")
st.title("📝 Transcription Audio avec Whisper")

uploaded_file = st.file_uploader("Choisissez un fichier audio", type=["mp3", "wav", "m4a", "ogg", "flac"]) 

if uploaded_file is not None:
    st.audio(uploaded_file, format="audio/mpeg")
    
    # Sauvegarde temporaire du fichier
    file_path = os.path.join("temp_audio", uploaded_file.name)
    os.makedirs("temp_audio", exist_ok=True)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    st.write("🔄 Transcription en cours...")
    
    # Transcription Whisper
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
