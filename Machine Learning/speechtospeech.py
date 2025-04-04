# Bonus Implementation for audio synthesis
import json
from gtts import gTTS # google text to speech

# Loading the translated text from a JSON file
with open("translated.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Combine all text fields from json file
all_text = " ".join(item.get("text", "") for item in data if "text" in item)

if all_text:
    # Convert to speech in required language
    tts = gTTS(text=all_text, lang='te')
    
    # Save as MP3 audio file
    tts.save("output_audio.mp3")
    print("Speech generated in required language and saved to output_audio.mp3")
else:
    print("Caution! No valid text entries found in the JSON file.")