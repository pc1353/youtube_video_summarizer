# YouTube Video Summarizer

## Overview

The YouTube Video Summarizer is a Python application designed to extract and summarize the content of YouTube videos. This tool is useful for quickly understanding the key points of lengthy videos without having to watch the entire content.

## Features

- Extracts video content using YouTube API.
- Summarizes extracted text using OpenAI Whisper.
- Provides concise summaries of video content using Gemini 1.5-flash.
- Easy-to-use interface.

## Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/pc1353/youtube_video_summarizer.git
    cd youtube_video_summarizer
    ```

2. **Install required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. **Set up YouTube API credentials:**
   - Obtain API key from [Google Developers Console](https://console.developers.google.com/).
   - Create a `constants.py` file with your API key:
     ```python
     API_KEY = 'YOUR_GEMINI_API_KEY'
     ```

2. **Run the application:**
    ```bash
    streamlit run app.py
    ```

## Files

- `app.py`: Main application script that handles video extraction and summarization.
- `constants.py`: Contains API key and other constants.
- `requirements.txt`: Lists all the dependencies required to run the application.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any features or fixes.

## License

This project is licensed under the MIT License.

## Contact

For any questions or suggestions, please contact [prnavchaniyara123@gmail.com].
