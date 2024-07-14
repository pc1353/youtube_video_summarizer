import streamlit as st
from pytube import YouTube
import whisper
import time
import google.generativeai as genai
import PIL.Image
import os
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from constants import PROMPT, MODEL_NAME


load_dotenv()

genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
gemini_model = genai.GenerativeModel(model_name=MODEL_NAME)

whisper_model = whisper.load_model("base")

st.set_page_config(
    layout="wide"
)

def prompt_node(text):
    prompt_template = PromptTemplate(template=PROMPT, input_variables=["context"])
    prompt_formatted_str: str = prompt_template.format(context=text)
    return prompt_formatted_str

def download_video(url):
    yt = YouTube(url)
    video = yt.streams.filter(only_audio=True).order_by('abr').desc().first()
    return video.download()

def transcribe_audio(file_path):
    output = whisper_model.transcribe(file_path)
    output = output["text"]
    return output

def main():

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
