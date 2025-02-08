from openai import OpenAI


class OpenAIWhisper:
    def __init__(self, audio_path: str, model: str, api_key: str):
        self.audio_path = audio_path
        self.model = model
        self.api_key = api_key

    def initialize_client(self) -> OpenAI:
        return OpenAI(api_key=self.api_key)

    def transcribe_audio(self, prompt: str, response_format: str = "text") -> str:
        with open(self.audio_path, "rb") as audio_file:
            client = self.initialize_client()
            transcription = client.audio.transcriptions.create(
                model=self.model,
                file=audio_file,
                response_format=response_format,
                prompt=prompt
            )
        return transcription

    def post_process_text(self, text: str, gpt_model: str, prompt_postprocess: str):
        client = self.initialize_client()
        response = client.chat.completions.create(
            model=gpt_model,
            messages=[
                {"role": "system", "content": prompt_postprocess},
                {"role": "user", "content": text}
            ]
        )
        return response.choices[0].message.content
