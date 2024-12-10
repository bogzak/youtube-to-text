# YouTube Video to Text Transcription Tool

## Overview

This tool is designed to process YouTube videos, extract their audio, and transcribe it into text using OpenAI's Whisper model. It supports processing large audio files by splitting them into smaller chunks, and it also provides post-processing capabilities to refine the transcription using a GPT model.

## Features

1. **YouTube Audio Extraction**: Automatically downloads and extracts audio from YouTube videos.
2. **Audio Splitting**: Handles large audio files by splitting them into manageable chunks.
3. **Whisper Model Transcription**: Transcribes audio into text using OpenAI's Whisper model.
4. **Post-Processing**: Enhances transcription quality using GPT-based post-processing.
5. **Error Handling**: Logs errors for failed video/audio processing.

---

## Project Structure

### 1. Utilities Module (`utils`)
Contains helper functions for file operations and OpenAI client initialization:
- **`read_file`**: Reads a file and returns its content as a string.
- **`read_file_lines`**: Reads a file and returns a list of non-empty lines.
- **`get_file_size`**: Retrieves the size of a file in bytes.
- **`save_transcription_to_file`**: Saves a transcription to a text file.
- **`initialize_client`**: Initializes an OpenAI client using an API key.

### 2. Main Module (`__main__`)
Orchestrates the entire process, from downloading audio to transcription and saving results:
- **`split_audio`**: Splits large audio files into smaller chunks.
- **`transcribe_audio`**: Sends audio data to OpenAI Whisper for transcription.
- **`post_process_text`**: Refines transcriptions using GPT-based models.
- **`process_audio_file`**: Manages audio splitting and transcription processes.
- **`download_youtube_audio`**: Downloads audio from YouTube videos.
- **Entry Point**: Processes all video URLs listed in a configuration file.

## Requirements

To use this tool, ensure the following dependencies and prerequisites are met:

### Software and Libraries

1. **Python 3.8+**: The tool is built in Python and requires version 3.8 or later.
2. **OpenAI Python SDK**: For interfacing with OpenAI's Whisper and GPT models.
3. **pytubefix**: To handle YouTube video downloading and audio extraction.
4. **pydub**: For audio file manipulation and splitting.
5. **dotenv**: To manage environment variables securely.
6. **ffmpeg**: Required for processing and converting audio files.

### Installation Instructions

1. Ensure Python 3.8+ and all required dependencies are installed on your system.
2. Create a `.env` file in the root directory with the following content:
   ```plaintext
   OPENAI_API_KEY=your_api_key_here
   GPT_MODEL=gpt-3.5-turbo
3. Prepare the `files/` directory and include the following:

   - **`video_urls.txt`**: A plain text file containing the YouTube video URLs to process, with one URL per line.
   - **`prompt_preprocess.txt`**: A text file that contains the preprocessing instructions for the Whisper transcription model.
   - **`prompt_postprocess.txt`** (optional): A text file with post-processing instructions for refining the transcription using the GPT model.
4. Run the program using the following command:
   ```bash
   python voice_to_text.py
5. The output transcriptions will be saved in the `transcriptions/` directory:
   - Files will be named in the format `transcription_<index>.txt`, where `<index>` corresponds to the order of URLs in `video_urls.txt`.

6. Check the console or logs for detailed processing information:
   - Successful downloads and transcriptions will be logged.
   - Errors during processing will also be logged for troubleshooting.

7. Ensure that `ffmpeg` is correctly installed and accessible from the command line:
   - Use the command `ffmpeg -version` to verify the installation.
   - If not installed, follow the instructions in the "Requirements" section.

8. Modify the configuration as needed:
   - Update the `.env` file with the appropriate OpenAI API key and GPT model.
   - Adjust prompts in `prompt_preprocess.txt` and `prompt_postprocess.txt` for custom transcription and refinement behavior.

9. To process additional videos:
   - Add new URLs to `video_urls.txt`.
   - Rerun the program to generate new transcriptions.

10. Troubleshooting:

    - **Audio Not Downloading**: Ensure the YouTube URL is correct and accessible. Use a VPN if regional restrictions apply.
    - **ffmpeg Issues**: Confirm `ffmpeg` is installed and added to your system's PATH.
    - **OpenAI API Errors**: Verify your API key in the `.env` file and check your OpenAI usage limits.
    - **Large Audio Files**: Ensure the `split_audio` function is correctly splitting large audio files into manageable chunks.

11. Customization:

    - **Change Models**: Update the `GPT_MODEL` in the `.env` file to use a different OpenAI model.
    - **Prompts**: Tailor the `prompt_preprocess.txt` and `prompt_postprocess.txt` files to suit your transcription needs.
    - **Output Paths**: Modify the output file paths in the code to save transcriptions in a custom directory.

12. Logging:

    - The program logs all operations, including errors, to the console.
    - Use logs to monitor progress and identify any issues during execution.

13. Limitations:

    - **File Size**: Audio files larger than 25MB are automatically split into smaller chunks, which may slightly affect transcription continuity.
    - **YouTube Video Restrictions**: Videos with restrictions (e.g., private, age-restricted) cannot be processed.
    - **Network Dependency**: A stable internet connection is required for downloading videos and accessing OpenAI APIs.

14. Future Enhancements:

    - **Batch Processing**: Add support for parallel processing to speed up large-scale transcription tasks.
    - **Custom Models**: Integrate support for additional models and fine-tuning capabilities.
    - **Detailed Logs**: Implement advanced logging for more granular monitoring and debugging.

15. Support:

    - For questions or issues, create an issue in the repository or contact the project maintainer.
    - Contributions are welcome! Feel free to fork the repository and submit a pull request.

16. Example Directory Structure:

    ```
    project_root/
    ├── files/
    │   ├── video_urls.txt
    │   ├── prompt_preprocess.txt
    │   ├── prompt_postprocess.txt
    ├── transcriptions/
    │   ├── transcription_1.txt
    │   ├── transcription_2.txt
    ├── voice_to_text.py
    ├── utils.py
    ├── .env
    ├── requirements.txt
    ```

17. Additional Notes:

    - Ensure that the `transcriptions/` directory exists before running the script, as the program will attempt to save results there.
    - Audio files downloaded during processing are temporarily stored in the working directory and should be manually cleaned up if no longer needed.