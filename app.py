import streamlit as st
import whisper
import time
import google.generativeai as genai
import PIL.Image
import os
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from constants import PROMPT, MODEL_NAME
import yt_dlp
import subprocess
import sys
import platform
import shutil

load_dotenv()

genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
gemini_model = genai.GenerativeModel(model_name=MODEL_NAME)

whisper_model = whisper.load_model("base")

st.set_page_config(
    layout="wide"
)

def install_ffmpeg():
    system = platform.system().lower()
    if system == "windows":
        ffmpeg_url = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-full.7z"
        ffmpeg_extracted_path = "ffmpeg-release-full"
        ffmpeg_exe_path = os.path.join(ffmpeg_extracted_path, "bin", "ffmpeg.exe")
    elif system == "linux":
        ffmpeg_url = "https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-64bit-static.tar.xz"
        ffmpeg_extracted_path = "ffmpeg-release-64bit-static"
        ffmpeg_exe_path = os.path.join(ffmpeg_extracted_path, "ffmpeg")
    elif system == "darwin":
        ffmpeg_url = "https://evermeet.cx/ffmpeg/ffmpeg-5.0.1.zip"
        ffmpeg_extracted_path = "ffmpeg-5.0.1"
        ffmpeg_exe_path = os.path.join(ffmpeg_extracted_path, "ffmpeg")
    else:
        raise Exception(f"Unsupported platform: {system}")

    ffmpeg_download_path = "ffmpeg_download"

    if not os.path.exists(ffmpeg_exe_path):
        # Download ffmpeg
        st.info("Downloading ffmpeg...")
        if not os.path.exists(ffmpeg_download_path):
            os.makedirs(ffmpeg_download_path)
        ffmpeg_download_file = os.path.join(ffmpeg_download_path, os.path.basename(ffmpeg_url))

        if not os.path.exists(ffmpeg_download_file):
            import requests
            response = requests.get(ffmpeg_url, stream=True)
            with open(ffmpeg_download_file, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
        
        # Extract ffmpeg
        st.info("Extracting ffmpeg...")
        if system == "windows":
            import py7zr
            with py7zr.SevenZipFile(ffmpeg_download_file, 'r') as archive:
                archive.extractall(ffmpeg_download_path)
        elif system == "linux":
            subprocess.run(["tar", "-xf", ffmpeg_download_file, "-C", ffmpeg_download_path])
        elif system == "darwin":
            subprocess.run(["unzip", ffmpeg_download_file, "-d", ffmpeg_download_path])

    os.environ["PATH"] += os.pathsep + os.path.abspath(ffmpeg_extracted_path)

def prompt_node(text):
    prompt_template = PromptTemplate(template=PROMPT, input_variables=["context"])
    prompt_formatted_str: str = prompt_template.format(context=text)
    return prompt_formatted_str

def download_video(url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'downloads/%(title)s.%(ext)s',
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        file_path = ydl.prepare_filename(info_dict)
    return file_path

def transcribe_audio(file_path):
    output = whisper_model.transcribe(file_path)
    output = output["text"]
    return output

def main():
    install_ffmpeg()

    # Set the title and background color
    st.title("YouTube Video Summarizer 🎥")
    st.markdown('<style>h1{color: orange; text-align: center;}</style>', unsafe_allow_html=True)
    st.subheader('Built with the Gemini 1.5 Flash, Whisper, Streamlit')
    st.markdown('<style>h3{color: pink;  text-align: center;}</style>', unsafe_allow_html=True)

    # Expander for app details
    with st.expander("About the App"):
        st.write("This app allows you to summarize while watching a YouTube video.")
        st.write("Enter a YouTube URL in the input box below and click 'Submit' to start. This app is built by AI Anytime.")

    # Input box for YouTube URL
    youtube_url = st.text_input("Enter YouTube URL")

    # Submit button
    if st.button("Submit") and youtube_url:
        start_time = time.time()  # Start the timer
        # Download video
        file_path = download_video(youtube_url)

        model = gemini_model

        text = transcribe_audio(file_path)
        
        prompt = prompt_node(text)

        output = gemini_model.generate_content(prompt)
        output = output.text

        print("Final Output:= ",output)

        end_time = time.time()  # End the timer
        elapsed_time = end_time - start_time

        # Display layout with 2 columns
        col1, col2 = st.columns([1,1])

        os.remove(file_path)

        # Column 1: Video view
        with col1:
            st.video(youtube_url)

        # Column 2: Summary View
        with col2:
            st.header("Summarization of YouTube Video")
            st.write(output)
            st.write(f"Time taken: {elapsed_time:.2f} seconds")

if __name__ == "__main__":
    main()
