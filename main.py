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


# Настройка логирования
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


# Загрузка конфигурации из файла .env
config = dotenv_values(".env")

API_KEY = config["OPENAI_API_KEY"]
GPT_MODEL = config["GPT_MODEL"]
PROMPT_PREPROCESS = read_file("files/prompt_preprocess.txt")
PROMPT_POSTPROCESS = read_file("files/prompt_postprocess.txt")
VIDEO_URLS = read_file_lines("files/video_urls.txt")


def process_audio_file(file_path: str, prompt="") -> str:
    if get_file_size(file_path) <= 25 * 1024 * 1024:  # 25 MB
        chunks = [file_path]
    else:
        audio_process = AudioProcessing(file_path)
        chunks = audio_process.split_audio()

    openai_whisper = OpenAIWhisper(model="whisper-1", api_key=API_KEY)
    full_transcription = "\n".join(
        openai_whisper.transcribe_audio(audio_path=chunk, prompt=prompt) for chunk in chunks
    )
    return full_transcription


def main():
    for i, url in enumerate(VIDEO_URLS):
        try:
            youtube_downloader = YoutubeDownloader(url=url, output_path=".")
            audio_path = youtube_downloader.download_youtube_audio()
            logging.info(f"Processing audio file: {audio_path}")
            transcription = process_audio_file(api_key, audio_path, prompt=prompt_preprocess)
            if prompt_postprocess:
                transcription = post_process_text(api_key, transcription, gpt_model=gpt_model, prompt_postprocess=prompt_postprocess)
            output_file_path = f"transcriptions/transcription_{i+1}.txt"
            save_transcription_to_file(transcription, output_file_path)
            logging.info(f"Transcription saved to {output_file_path}")
        except Exception as e:
            logging.error(f"Error processing {url}: {e}")


if __name__ == "__main__":
    main()
