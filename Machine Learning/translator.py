# Importing necessary libraries
import json
import time
from deep_translator import GoogleTranslator # imported googledeeptranslator for translating audio into required language

# Loading transcript.json to translate into telugu language
with open("transcript.json", "r", encoding="utf-8") as f:
    transcript = json.load(f)

translated_segments = []

# Translating each audio segment with retry logic
for idx, segment in enumerate(transcript):
    text = segment["text"]
    for attempt in range(3):  # Retry up to 3 times
        try:
            print(f"Translating segment {idx+1}/{len(transcript)}")
            translated_text = GoogleTranslator(source='auto', target='te').translate(text)
            translated_segments.append({
                "start": segment.get("start", ""),
                "end": segment.get("end", ""),
                "text": translated_text
            })
            break
        except Exception as e:
            print(f"Failed to attempt {attempt+1}: {e}")
            time.sleep(5)
    else:
        translated_segments.append({
            "start": segment.get("start", ""),
            "end": segment.get("end", ""),
            "text": "[Translation Failed]"
        })

# Saving translated transcript into translated.json file
with open("translated.json", "w", encoding="utf-8") as f:
    json.dump(translated_segments, f, ensure_ascii=False, indent=2)

print("Translation complete. Saved to output file")