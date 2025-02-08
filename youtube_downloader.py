import os

from pytubefix import YouTube


class YoutubeDownloader:
    def __init__(self, url: str, output_path: str):
        self.url = url
        self.output_path = output_path

    def download_youtube_audio(self) -> str:
        yt = YouTube(self.url, "IOS")
        stream = yt.streams.filter(only_audio=True).first()
        audio_file_path = os.path.join(self.output_path, f"audio/audio_{yt.video_id}.mp3")

        stream.download(output_path=self.output_path, filename=f"audio/audio_{yt.video_id}.mp3")

        return audio_file_path
