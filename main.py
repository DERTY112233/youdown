import os
import subprocess
import sys

REQUIRED_PACKAGES = ["streamlit", "yt-dlp"]

def install_missing_packages():
    for package in REQUIRED_PACKAGES:
        try:
            __import__(package)
        except ImportError:
            print(f"Package '{package}' not found. Installing...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])

install_missing_packages()

import streamlit as st
from yt_dlp import YoutubeDL

DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

def main():
    st.title("YouTube to MP3 Downloader")
    st.write("Enter a YouTube URL of the sermon below to download the audio as an MP3 file.")

    url = st.text_input("YouTube URL", "")

    if st.button("Download MP3"):
        if not url:
            st.error("Please enter a valid YouTube URL.")
        else:
            try:
                ydl_opts = {
                    "format": "bestaudio/best",
                    "outtmpl": os.path.join(DOWNLOAD_FOLDER, "%(title)s.%(ext)s"),
                    "postprocessors": [{
                        "key": "FFmpegExtractAudio",
                        "preferredcodec": "mp3",
                        "preferredquality": "192",
                    }],
                }
                
                with YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    title = info.get("title", "Unknown Title")
                    st.success(f"Downloaded '{title}.mp3' successfully!")
                    st.write(f"File saved in '{DOWNLOAD_FOLDER}' folder.")
                    
            except Exception as e:
                st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()

