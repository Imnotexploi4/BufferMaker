#!/usr/bin/env python3
"""
Video Buffer Generator (Cross-Platform: iSH / a-Shell / Termux / iPhone / Android)
Automatically scans for MP4 videos in your Documents (or home) folder
and joins the selected one with a glitch buffer using FFmpeg.

Educational purposes only.
"""

import os
import subprocess
import time
import platform

# === Configuration ===
# Default search directory (depends on system)
SYSTEM = platform.system().lower()

if "linux" in SYSTEM:  # Termux or Android/Linux
    DEFAULT_SEARCH_DIR = os.path.expanduser("~/storage/shared") if os.path.exists(os.path.expanduser("~/storage/shared")) else os.path.expanduser("~")
elif "darwin" in SYSTEM:  # iOS (a-Shell / iSH)
    DEFAULT_SEARCH_DIR = os.path.expanduser("~/Documents")
else:
    DEFAULT_SEARCH_DIR = os.path.expanduser("~")

# === Utility Functions ===
def list_all_videos(base_dir):
    """
    Recursively search for all .mp4 files in the base_dir and its subfolders.
    """
    video_files = []
    for root, _, files in os.walk(base_dir):
        for name in files:
            if name.lower().endswith(".mp4"):
                full_path = os.path.join(root, name)
                video_files.append(full_path)
    return sorted(video_files)

def select_video(videos):
    """
    Let the user select a video file from the list.
    """
    if not videos:
        print(f"\nNo MP4 files found in {DEFAULT_SEARCH_DIR}.")
        print("Please copy videos there and try again.\n")
        return None

    print("\n=== Found MP4 Videos ===")
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

    # 1. Search for all MP4 videos
    print(f"Scanning for videos in: {DEFAULT_SEARCH_DIR} ...")
    videos = list_all_videos(DEFAULT_SEARCH_DIR)

    video_path = select_video(videos)
    if not video_path:
        return

    # 2. Glitch buffer video
    glitch_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "RawBuffer", "glitch.mp4")
    if not os.path.exists(glitch_path):
        print(f"❌ Missing glitch video at {glitch_path}")
        return

    # 3. Ask for custom output filename
    print()
    buffer_name = input("Name your Buffer Video file (without .mp4): ").strip()
    if not buffer_name:
        buffer_name = os.path.splitext(os.path.basename(video_path))[0] + "_buffered"

    # Ensure .mp4 extension
    if not buffer_name.lower().endswith(".mp4"):
        buffer_name += ".mp4"

    base_dir = os.path.dirname(video_path)
    output_path = os.path.join(base_dir, buffer_name)

    # 4. Create temporary concat list
    concat_list = os.path.join(base_dir, "temp_list.txt")
    with open(concat_list, "w", encoding="utf-8") as f:
        f.write(f"file '{video_path}'\n")
        f.write(f"file '{glitch_path}'\n")

    # 5. Run FFmpeg
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
