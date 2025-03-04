import os
import logging

from pytubefix import YouTube


logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


class YoutubeDownloader:
    def __init__(self, url: str, output_path: str):
        self.url = url
        self.output_path = output_path

    def download_youtube_audio(self) -> str:
        yt = YouTube(
            self.url,
            client='IOS'
        )
        stream = yt.streams.filter(only_audio=True).first()
        audio_file_path = os.path.join(self.output_path, f"audio_{yt.video_id}.mp3")
        logging.info(f"Start downloading audio from: {self.url}")

        stream.download(output_path=self.output_path, filename=f"audio_{yt.video_id}.mp3")
        logging.info(f"Audio downloaded and saved to: {audio_file_path}")

        return audio_file_path
