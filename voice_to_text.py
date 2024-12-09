import os
import logging

from pytubefix import YouTube
from pydub import AudioSegment

from dotenv import dotenv_values

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


def split_audio(file_path, max_file_size=25 * 1024 * 1024) -> list:
    audio = AudioSegment.from_file(file_path)
    file_size = len(audio)
    if file_size <= max_file_size:
        return [file_path]

    chunks = []
    chunk_length = max_file_size * 1000 // len(audio)  # in milliseconds
    for i in range(0, len(audio), chunk_length):
        chunk = audio[i:i+chunk_length]
        chunk_path = f"{file_path}_chunk_{i // chunk_length}.mp3"
        chunk.export(chunk_path, format="mp3")
        chunks.append(chunk_path)
    return chunks


def transcribe_audio(client, audio_path, model="whisper-1", prompt="") -> str:
    with open(audio_path, "rb") as audio_file:
        transcription = client.audio.transcriptions.create(
            model=model,
            file=audio_file,
            response_format="text",
            prompt=prompt
        )
    return transcription


def post_process_text(api_key, text, gpt_model="", prompt_postprocess="") -> str:
    client = initialize_client(api_key)
    response = client.chat.completions.create(
        model=gpt_model,
        messages=[
            {"role": "system", "content": prompt_postprocess},
            {"role": "user", "content": text}
        ]
    )
    return response.choices[0].message.content


def process_audio_file(api_key, file_path, prompt="") -> str:
    client = initialize_client(api_key)

    if get_file_size(file_path) <= 25 * 1024 * 1024:  # 25 MB
        chunks = [file_path]
    else:
        chunks = split_audio(file_path)

    full_transcription = "\n".join(
        transcribe_audio(client, chunk, prompt=prompt) for chunk in chunks
    )
    return full_transcription


def download_youtube_audio(url, output_path) -> str:
    yt = YouTube(url, "IOS")
    stream = yt.streams.filter(only_audio=True).first()
    audio_file_path = os.path.join(output_path, f"audio/audio_{yt.video_id}.mp3")
    logging.info(f"Start downloading audio from: {url}")
    stream.download(output_path=output_path, filename=f"audio/audio_{yt.video_id}.mp3")
    logging.info(f"Audio downloaded and saved to: {audio_file_path}")
    return audio_file_path


if __name__ == "__main__":
    api_key = config["OPENAI_API_KEY"]
    gpt_model = config["GPT_MODEL"]
    prompt_param = read_file("files/prompt_preprocess.txt")
    prompt_postprocess = read_file("files/prompt_postprocess.txt")
    video_urls = read_file_lines("files/video_urls.txt")

    for i, url in enumerate(video_urls):
        try:
            audio_path = download_youtube_audio(url, ".")
            logging.info(f"Processing audio file: {audio_path}")           
            transcription = process_audio_file(api_key, audio_path, prompt=prompt_param)          
            if prompt_postprocess:
                transcription = post_process_text(api_key, transcription, gpt_model=gpt_model, prompt_postprocess=prompt_postprocess)         
            output_file_path = f"transcriptions/transcription_{i+1}.txt"
            save_transcription_to_file(transcription, output_file_path)
            logging.info(f"Transcription saved to {output_file_path}")      
        except Exception as e:
            logging.error(f"Error processing {url}: {e}")
