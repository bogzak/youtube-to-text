import os


def read_file(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read().strip()
    

def read_file_lines(file_path: str) -> list[str]:
    with open(file_path, "r", encoding="utf-8") as file:
        return [line.strip() for line in file if line.strip()]
    

def get_file_size(file_path: str) -> int:
    return os.path.getsize(file_path)


def save_transcription_to_file(text: str, output_file_path: str) -> None:
    with open(output_file_path, "w", encoding="utf-8") as file:
        file.write(text)

