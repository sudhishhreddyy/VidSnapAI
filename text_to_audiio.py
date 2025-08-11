import os 
import uuid
from elevenlabs import VoiceSettings
from elevenlabs.client import ElevenLabs
from config import ELEVENLABS_API_KEY

client = ElevenLabs(
    api_key= ELEVENLABS_API_KEY
)

def text_to_speech_file(text: str, folder: str) -> str:
    response = client.text_to_speech.convert(
        voice_id="pNInz6obpgDQGcFmaJgB",  
        output_format="mp3_22050_32",
        model_id="eleven_turbo_v2_5",
        voice_settings=VoiceSettings(
            stability=0.0,
            similarity_boost=1.0,
            use_speaker_boost=True,
            speed=1.0
        ),
        text=text
    )
    
    # folder should already be like "user_uploads/<uuid>"
    save_file_path = os.path.join(folder, "audio.mp3")
    os.makedirs(folder, exist_ok=True)  # make sure folder exists
    
    with open(save_file_path, "wb") as f:
        for chunk in response:
            if chunk:
                f.write(chunk)
            
    print(f"{save_file_path}: A new audio file was saved successfully!")
    return save_file_path
