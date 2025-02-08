from pydub import AudioSegment


class AudioProcessing:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def split_audio(self, max_file_size: int = 25 * 1024 * 1024) -> list:
        audio = AudioSegment.from_file(self.file_path)
        file_size = len(audio)
        if file_size <= max_file_size:
            return [self.file_path]

        chunks = []
        chunk_length = max_file_size * 1000 // len(audio) # in milliseconds
        for i in range(0, len(audio), chunk_length):
            chunk = audio[i:i+chunk_length]
            chunk_path = f"{self.file_path}_chunk_{i // chunk_length}.mp3"
            chunk.export(chunk_path, format="mp3")
            chunks.append(chunk_path)
        return chunks
