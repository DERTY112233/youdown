import os
import sys
import subprocess
import venv
import webbrowser

APP_FILE = "ytmp3_app.py"
VENV_DIR = os.path.join(os.path.dirname(__file__), "venv")
PYTHON_EXE = os.path.join(VENV_DIR, "Scripts", "python.exe")
def ensure_virtualenv():
    if not os.path.exists(PYTHON_EXE):
        print("🔧 Creating virtual environment...")
        venv.create(VENV_DIR, with_pip=True)
        print("✅ Virtual environment created.")

def install_dependencies():
    print("📦 Installing dependencies (Streamlit, yt-dlp)...")
    subprocess.check_call([PYTHON_EXE, "-m", "pip", "install", "--upgrade", "pip"])
    subprocess.check_call([PYTHON_EXE, "-m", "pip", "install", "streamlit", "yt-dlp"])
    print("✅ Dependencies installed successfully.\n")

def create_app_file():
    if os.path.exists(APP_FILE):
        return
    with open(APP_FILE, "w", encoding="utf-8") as f:
        f.write(APP_CODE)
    print(f"📝 Created {APP_FILE}")

def launch_app():
    print("🚀 Launching Streamlit app...")
    webbrowser.open("http://localhost:8501")
    subprocess.call([PYTHON_EXE, "-m", "streamlit", "run", APP_FILE])

APP_CODE = r'''
import os
import streamlit as st
from yt_dlp import YoutubeDL

DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

st.set_page_config(page_title="YouTube to MP3", page_icon="🎵", layout="centered")

st.title("🎵 YouTube to MP3 Converter")
st.caption("Convert and download YouTube videos as MP3 — fast, free, and local.")

url = st.text_input("🔗 Paste YouTube Video URL:")
download_button = st.button("🎧 Convert to MP3")

def download_audio(video_url):
    """Download a YouTube video's audio as an MP3 file."""
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": os.path.join(DOWNLOAD_FOLDER, "%(title)s.%(ext)s"),
        "quiet": True,
        "noprogress": True,
        "postprocessors": [
            {"key": "FFmpegExtractAudio", "preferredcodec": "mp3", "preferredquality": "192"},
            {"key": "EmbedThumbnail"},
            {"key": "FFmpegMetadata"},
        ],
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(video_url, download=True)
        title = info.get("title", "Unknown Title")
        file_path = os.path.join(DOWNLOAD_FOLDER, f"{title}.mp3")
        return title, file_path, info

if download_button:
    if not url.strip():
        st.error("⚠️ Please enter a valid YouTube URL.")
    else:
        with st.spinner("🎶 Downloading and converting, please wait..."):
            try:
                title, file_path, info = download_audio(url)
                thumbnail = info.get("thumbnail")

                if thumbnail:
                    st.image(thumbnail, caption=title, use_container_width=True)

                st.success(f"✅ '{title}' downloaded successfully!")

                with open(file_path, "rb") as f:
                    st.download_button(
                        label="⬇️ Download MP3",
                        data=f,
                        file_name=os.path.basename(file_path),
                        mime="audio/mpeg",
                    )

                st.info(f"File saved locally in `{DOWNLOAD_FOLDER}/`.")
            except Exception as e:
                st.error(f"❌ Error: {e}")

st.markdown("---")
'''

if __name__ == "__main__":
    ensure_virtualenv()
    install_dependencies()
    create_app_file()
    launch_app()
