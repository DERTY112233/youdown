
import os
import streamlit as st
from yt_dlp import YoutubeDL

DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

st.set_page_config(page_title="YouTube to MP3", page_icon="🎵", layout="centered")

st.title("🎵 YouTube to MP3 Converter")
st.caption("Convert and download YouTube videos as MP3 files — simple and free.")

url = st.text_input("🔗 Paste YouTube Video URL below:")
download_button = st.button("Convert to MP3")

def download_audio(video_url):
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
        filename = os.path.join(DOWNLOAD_FOLDER, f"{title}.mp3")
        return title, filename, info

if download_button:
    if not url:
        st.error("⚠️ Please enter a valid YouTube URL.")
    else:
        with st.spinner("Downloading and converting... 🎧"):
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

                st.info(f"File saved locally in `{DOWNLOAD_FOLDER}/` folder.")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

st.markdown("---")
