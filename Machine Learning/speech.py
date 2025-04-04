# Importing necessary libraries
import whisper # Importing OpenAI Whisper library for speech recognition
import json 
import os
import yt_dlp # Importing yt_dlp libraru=y for extracting transcript from yt

# Function defined for downloading the youtube audio
def download_youtube_audio(url, output_path="audio.mp3"):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'temp.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl: # Used yt_dlp for extracting yt audio
        ydl.download([url])
    os.rename("temp.mp3", output_path)
    print(f"Audio saved as {output_path}")

# Function defined for transcribing audio using openai whisper
def transcribe_audio_whisper(audio_path="audio.mp3", output_json="transcript.json"):
    model = whisper.load_model("base")  # Loading openai whisper base model for it's ease of use
    result = model.transcribe(audio_path, verbose=True)

    transcript_data = []
    for segment in result["segments"]: # Retriving using segments
        transcript_data.append({
            "start": segment["start"],
            "end": segment["end"],
            "text": segment["text"]
        })

    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(transcript_data, f, indent=4, ensure_ascii=False)

    print(f"Transcript saved to {output_json}")

if __name__ == "__main__":
    youtube_url = input("Enter The YouTube Video URL To Transcribe The Audio: ")
    download_youtube_audio(youtube_url)
    transcribe_audio_whisper()