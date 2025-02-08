import logging

from dotenv import dotenv_values
from youtube_downloader import YoutubeDownloader
from audio_process import AudioProcessing

from utils import (
    initialize_client,
    get_file_size,
    read_file,
    read_file_lines,
    save_transcription_to_file
)


# Настройка логирования
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


# Загрузка конфигурации из файла .env
config = dotenv_values(".env")


def process_audio_file(api_key: str, file_path: str, prompt="") -> str:
    client = initialize_client(api_key)

    if get_file_size(file_path) <= 25 * 1024 * 1024:  # 25 MB
        chunks = [file_path]
    else:
        audio_process = AudioProcessing(file_path)
        chunks = audio_process.split_audio()

    full_transcription = "\n".join(
        transcribe_audio(client, chunk, prompt=prompt) for chunk in chunks
    )
    return full_transcription


if __name__ == "__main__":
    api_key = config["OPENAI_API_KEY"]
    gpt_model = config["GPT_MODEL"]
    prompt_param = read_file("files/prompt_preprocess.txt")
    prompt_postprocess = read_file("files/prompt_postprocess.txt")
    video_urls = read_file_lines("files/video_urls.txt")

    for i, url in enumerate(video_urls):
        try:
            youtube_downloader = YoutubeDownloader(url=url, output_path=".")
            audio_path = youtube_downloader.download_youtube_audio()
            logging.info(f"Processing audio file: {audio_path}")           
            transcription = process_audio_file(api_key, audio_path, prompt=prompt_param)          
            if prompt_postprocess:
                transcription = post_process_text(api_key, transcription, gpt_model=gpt_model, prompt_postprocess=prompt_postprocess)         
            output_file_path = f"transcriptions/transcription_{i+1}.txt"
            save_transcription_to_file(transcription, output_file_path)
            logging.info(f"Transcription saved to {output_file_path}")      
        except Exception as e:
            logging.error(f"Error processing {url}: {e}")
