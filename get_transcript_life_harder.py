from playwright.sync_api import sync_playwright
import subprocess
import tempfile
import os
import whisper
from datetime import datetime

def get_video_url(lecture_url):
    """
    Extract the video URL from a UM-Canvas lecture page using the system-installed Chrome browser.
    """
    with sync_playwright() as p:
        # Launch Chrome with the default profile
        browser = p.chromium.launch(
            headless=False,
            executable_path="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

        )
        page = browser.new_page()

        print(f"🔍 Navigating to: {lecture_url}")
        page.goto(lecture_url)

        # Wait for the video element to appear
        try:
            page.wait_for_selector("video", timeout=60000)
            video_url = page.locator("video").get_attribute("src")
        except Exception as e:
            print(f"❌ Failed to find video: {e}")
            video_url = None

        browser.close()

        if video_url:
            print(f"🎯 Video URL found: {video_url}")
            return video_url
        else:
            print("⚠️ Video URL not found. Check if Canvas uses an iframe or different structure.")
            return None


# 🎯 Replace with an actual Canvas lecture URL
lecture_url = input("Input ur lecture url") #"https://leccap.engin.umich.edu/leccap/player/r/oTAiJl"
video_url = get_video_url(lecture_url)

if video_url:
    print("\n✅ Successfully extracted video URL:")
    print(video_url)
    video_url  = "https:" + video_url
else:
    print("\n❌ Failed to extract video URL. Please inspect the video element manually.")



def test_ffmpeg_audio(video_url):
    """
    Use FFmpeg to stream audio from the video URL and save it as a .wav file.
    """
    # Create a temporary file for the audio stream
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_audio_file:
        temp_path = temp_audio_file.name

    # FFmpeg command to stream audio from the video URL and save as WAV
    ffmpeg_cmd = [
        "ffmpeg",
        "-i", video_url,           # Input video URL
        "-vn",                     # Disable video (audio only)
        "-acodec", "pcm_s16le",    # WAV format (PCM 16-bit little-endian)
        "-ar", "16000",            # 16kHz sample rate (common for speech)
        "-ac", "1",                # Mono audio (faster and clearer for speech)
        "-f", "wav",               # Output format
        temp_path                  # Destination file
    ]

    print(f"🎧 Running FFmpeg to convert video to audio...")
    try:
        subprocess.run(ffmpeg_cmd, check=True)
        print(f"✅ Audio successfully extracted to: {temp_path}")
    except subprocess.CalledProcessError as e:
        print(f"❌ FFmpeg failed: {e}")
        return None

    # Return the file path so you can listen to the audio manually
    return temp_path


# 🎯 Step: Run FFmpeg on the extracted video URL
if video_url:
    audio_file_path = test_ffmpeg_audio(video_url)

    if audio_file_path:
        print(f"\n🎶 Audio saved here: {audio_file_path}")
        print("🔊 Open the file to check if the audio is correct.")
    else:
        print("❌ Failed to convert video to audio.")
else:
    print("❌ Video URL not found, cannot proceed with FFmpeg.")



def transcribe_audio(audio_file_path):
    """
    Transcribe the audio using Whisper and save the text to a file.
    """
    # Load the Whisper model (choose 'tiny' for faster results or 'base' for better accuracy)
    model = whisper.load_model("base")

    print("🧠 Transcribing audio with Whisper...")

    # Run the transcription
    result = model.transcribe(audio_file_path)

    # Generate a timestamped filename for the transcription file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"lecture_transcription_{timestamp}.txt"

    # Write the transcription to the file
    with open(output_file, "w") as f:
        f.write(result["text"])

    print(f"✅ Transcription saved to: {output_file}")

    return output_file


# 🎯 Step: Run Whisper on the extracted audio file
if audio_file_path:
    transcription_file = transcribe_audio(audio_file_path)

    if transcription_file:
        print(f"\n📝 Transcription completed. File saved at: {transcription_file}")
    else:
        print("❌ Transcription failed.")
else:
    print("❌ Audio file not found, cannot proceed with Whisper.")