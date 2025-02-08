import logging

from dotenv import dotenv_values
from youtube_downloader import YoutubeDownloader
from audio_process import AudioProcessing
from openai_whisper import OpenAIWhisper

from utils import (
    get_file_size,
    read_file,
    read_file_lines,
    save_transcription_to_file
)


# Logging settings
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Loading the configuration from the .env file
config = dotenv_values(".env")

API_KEY = config["OPENAI_API_KEY"]
GPT_MODEL = config["GPT_MODEL"]
PROMPT_PREPROCESS = read_file("files/prompt_preprocess.txt")
PROMPT_POSTPROCESS = read_file("files/prompt_postprocess.txt")
VIDEO_URLS = read_file_lines("files/video_urls.txt")


def main():
    for i, url in enumerate(VIDEO_URLS):
        try:
            youtube_downloader = YoutubeDownloader(url=url, output_path=".")
            audio_path = youtube_downloader.download_youtube_audio()
            logging.info(f"Processing audio file: {audio_path}")

            if get_file_size(audio_path) <= 25 * 1024 * 1024:  # 25 MB
                chunks = [audio_path]
            else:
                audio_process = AudioProcessing(audio_path)
                chunks = audio_process.split_audio()

            openai_whisper = OpenAIWhisper(model="whisper-1", api_key=API_KEY)
            transcription = "\n".join(
                openai_whisper.transcribe_audio(audio_path=chunk, prompt=PROMPT_PREPROCESS) for chunk in chunks
            )

            if PROMPT_POSTPROCESS:
                transcription = openai_whisper.post_process_text(transcription, gpt_model=GPT_MODEL, prompt_postprocess=PROMPT_POSTPROCESS)
            output_file_path = f"transcriptions/transcription_{i+1}.txt"
            save_transcription_to_file(transcription, output_file_path)
            logging.info(f"Transcription saved to {output_file_path}")
        except Exception as e:
            logging.error(f"Error processing {url}: {e}")


if __name__ == "__main__":
    main()
