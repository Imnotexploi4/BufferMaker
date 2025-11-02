#!/usr/bin/env python3
"""
Video Buffer Generator (Cross-Platform: iSH / a-Shell / Termux / iPhone / Android)
Lists all supported video formats (.mp4, .mov, .avi, .mkv, .flv, .webm, .wav, etc.)
After selecting a file, automatically converts it to MP4 (if needed),
then joins it with a glitch buffer using FFmpeg.

Educational purposes only.
"""

import os
import subprocess
import time
import platform

# === Configuration ===
SYSTEM = platform.system().lower()

if "linux" in SYSTEM:  # Termux or Android/Linux
    DEFAULT_SEARCH_DIR = os.path.expanduser("~/storage/shared") if os.path.exists(os.path.expanduser("~/storage/shared")) else os.path.expanduser("~")
elif "darwin" in SYSTEM:  # iOS (a-Shell / iSH)
    DEFAULT_SEARCH_DIR = os.path.expanduser("~/Documents")
else:
    DEFAULT_SEARCH_DIR = os.path.expanduser("~")

# Supported formats
SUPPORTED_FORMATS = (
    ".mp4", ".mov", ".avi", ".mkv", ".flv", ".webm",
    ".mpeg", ".mpg", ".m4v", ".3gp", ".wav"
)

# === Utility Functions ===
def list_all_videos(base_dir):
    """
    Recursively search for all supported video files (except MP3).
    """
    video_files = []
    for root, _, files in os.walk(base_dir):
        for name in files:
            ext = os.path.splitext(name.lower())[1]
            if ext in SUPPORTED_FORMATS and ext != ".mp3":
                full_path = os.path.join(root, name)
                video_files.append(full_path)
    return sorted(video_files)

def convert_to_mp4(input_path):
    """
    Converts the given video/audio file to MP4 format using FFmpeg.
    Returns the new file path.
    """
    base, _ = os.path.splitext(input_path)
    output_path = base + "_converted.mp4"

    print(f"\n🎞️  Converting '{os.path.basename(input_path)}' → MP4...")
    cmd = [
        "ffmpeg", "-y", "-i", input_path,
        "-c:v", "libx264", "-c:a", "aac",
        "-strict", "experimental", output_path
    ]

    try:
        subprocess.run(cmd, check=True)
        print(f"✅ Converted successfully: {output_path}\n")
        return output_path
    except subprocess.CalledProcessError:
        print(f"❌ Failed to convert {input_path}")
        return None

def select_video(videos):
    """
    Let the user select a video file from the list.
    """
    if not videos:
        print(f"\nNo supported video files found in {DEFAULT_SEARCH_DIR}.")
        print("Please copy videos there and try again.\n")
        return None

    print("\n=== Found All Videos File ===")
    for i, path in enumerate(videos, 1):
        print(f"{i}. {os.path.basename(path)}")
    print()

    while True:
        choice = input("Select your video to make Buffer Video: ").strip()
        if choice.isdigit():
            index = int(choice)
            if 1 <= index <= len(videos):
                return videos[index - 1]
            else:
                print("That number doesn’t match any file — try again.\n")
        else:
            print("Please enter a number from the list above.\n")

def main():
    print("=== Video Buffer Generator ===\n")

    # 1. Search for videos
    print(f"Scanning for videos in: {DEFAULT_SEARCH_DIR} ...")
    videos = list_all_videos(DEFAULT_SEARCH_DIR)

    video_path = select_video(videos)
    if not video_path:
        return

    # 2. Convert to MP4 if needed
    if not video_path.lower().endswith(".mp4"):
        converted = convert_to_mp4(video_path)
        if not converted:
            return
        video_path = converted

    # 3. Check glitch buffer video
    glitch_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "RawBuffer", "glitch.mp4")
    if not os.path.exists(glitch_path):
        print(f"❌ Missing glitch video at {glitch_path}")
        return

    # 4. Ask for custom output filename
    print()
    buffer_name = input("Name your Buffer Video file (without .mp4): ").strip()
    if not buffer_name:
        buffer_name = os.path.splitext(os.path.basename(video_path))[0] + "_buffered"

    # Ensure .mp4 extension
    if not buffer_name.lower().endswith(".mp4"):
        buffer_name += ".mp4"

    base_dir = os.path.dirname(video_path)
    output_path = os.path.join(base_dir, buffer_name)

    # 5. Create temporary concat list
    concat_list = os.path.join(base_dir, "temp_list.txt")
    with open(concat_list, "w", encoding="utf-8") as f:
        f.write(f"file '{video_path}'\n")
        f.write(f"file '{glitch_path}'\n")

    # 6. Combine files using FFmpeg
    print("\nGenerating your buffer video...")
    time.sleep(1)
    print("Please wait ⏳")

    cmd = ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", concat_list, "-c", "copy", output_path]

    try:
        subprocess.run(cmd, check=True)
        os.remove(concat_list)
        time.sleep(0.5)
        print("\n✅ Done!")
        print(f"Your new video is ready:\n{output_path}\n")
        print("All set — enjoy your glitch buffer video! 🎬")
    except subprocess.CalledProcessError:
        print("\n❌ FFmpeg failed. Make sure it's installed and working in your terminal.")

if __name__ == "__main__":
    main()
