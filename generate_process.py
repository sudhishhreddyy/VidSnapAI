import os
from text_to_audiio import text_to_speech_file
import time
import subprocess

DONE_FILE = "done.txt"
UPLOADS_DIR = "user_uploads"

def text_to_audio(folder):
    print(f"TTA - {folder}")
    desc_path = os.path.join(UPLOADS_DIR, folder, "description.txt")
    
    if not os.path.exists(desc_path):
        raise FileNotFoundError(f"Description file not found: {desc_path}")
    
    with open(desc_path, "r") as f:
        text = f.read().strip()

    if not text:
        raise ValueError(f"Description file is empty: {desc_path}")
    
    print(f"Description: {text}")

    # Save audio file in the same folder
    folder_path = os.path.join(UPLOADS_DIR, folder)
    text_to_speech_file(text, folder_path)

def create_reel(folder):
    folder_path = os.path.join(UPLOADS_DIR, folder)
    input_txt = os.path.join(folder_path, "input.txt")
    audio_file = os.path.join(folder_path, "audio.mp3")

    if not os.path.exists(input_txt):
        raise FileNotFoundError(f"Missing input.txt: {input_txt}")
    if not os.path.exists(audio_file):
        raise FileNotFoundError(f"Missing audio.mp3: {audio_file}")

    output_file = os.path.join("static/reels", f"{folder}.mp4")

    # Build ffmpeg command (unchanged from your requirement)
    command = f'''ffmpeg -f concat -safe 0 -i user_uploads/{folder}/input.txt -i user_uploads/{folder}/audio.mp3 \
    -vf "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black" \
    -c:v libx264 -c:a aac -shortest -r 30 -pix_fmt yuv420p {output_file}'''
    
    subprocess.run(command, shell=True, check=True)
    print(f"Reel created: {output_file}")

if __name__ == "__main__":
    while True:
        print("Processing queue.......")

        # Read already processed folders
        if os.path.exists(DONE_FILE):
            with open(DONE_FILE, "r") as f:
                done_folders = [line.strip() for line in f]
        else:
            done_folders = []

        # Check all folders in user_uploads
        for folder in os.listdir(UPLOADS_DIR):
            folder_path = os.path.join(UPLOADS_DIR, folder)
            if not os.path.isdir(folder_path):
                continue

            if folder not in done_folders:
                try:
                    text_to_audio(folder)
                    create_reel(folder)

                    # Mark as done
                    with open(DONE_FILE, "a") as f:
                        f.write(folder + "\n")

                except Exception as e:
                    print(f"Error processing {folder}: {e}")

        time.sleep(4)

