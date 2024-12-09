import os

from openai import OpenAI


def read_file(file_path) -> str:
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read().strip()
    

def read_file_lines(file_path) -> list[str]:
    with open(file_path, "r", encoding="utf-8") as file:
        return [line.strip() for line in file if line.strip()]
    

def get_file_size(file_path) -> int:
    return os.path.getsize(file_path)


def save_transcription_to_file(text, output_file_path):
    with open(output_file_path, "w", encoding="utf-8") as file:
        file.write(text)


def initialize_client(api_key) -> OpenAI:
    return OpenAI(api_key=api_key)
