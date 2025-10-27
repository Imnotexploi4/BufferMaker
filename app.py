#!/usr/bin/env python3
"""
Video Buffer Generator (iSH / a-Shell / iPhone-Friendly)
Automatically scans for MP4 videos in your Documents folder (a-Shell files)
and joins the selected one with a glitch buffer using FFmpeg.

Educational purposes only.
"""

import os
import subprocess
import time

# === Configuration ===
# This is where a-Shell stores your files (Documents folder on iPhone)
DEFAULT_SEARCH_DIR = os.path.expanduser("~/Documents")

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
        print(f"No MP4 files found in {DEFAULT_SEARCH_DIR}.")
        print("You can copy videos into a-Shell's Documents folder and try again.\n")
        return None

    print("\n=== Found MP4 Videos ===")
    for i, path in enumerate(videos, 1):
        # Show just filename, but store full path
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

    # 1. Search for all MP4 videos in ~/Documents
    print(f"Scanning for videos in: {DEFAULT_SEARCH_DIR} ...")
    videos = list_all_videos(DEFAULT_SEARCH_DIR)

    video_path = select_video(videos)
    if not video_path:
        return

    # 2. Glitch buffer video
    glitch_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "RawBuffer", "glitch.mp4")
    if not os.path.exists(glitch_path):
        print(f"Oops! Missing glitch video at {glitch_path}")
        return

    # 3. Output path
    base_dir = os.path.dirname(video_path)
    output_path = os.path.join(base_dir, f"{os.path.splitext(os.path.basename(video_path))[0]}_buffered.mp4")

    # 4. Create temporary concat list
    concat_list = os.path.join(base_dir, "temp_list.txt")
    with open(concat_list, "w", encoding="utf-8") as f:
        f.write(f"file '{video_path}'\n")
        f.write(f"file '{glitch_path}'\n")

    # 5. Run FFmpeg
    print("\nAlright, generating your buffer video...")
    time.sleep(1)
    print("This might take a few seconds, hang tight ⏳")

    cmd = ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", concat_list, "-c", "copy", output_path]

    try:
        subprocess.run(cmd, check=True)
        os.remove(concat_list)
        time.sleep(0.5)
        print("\n✅ Done!")
        time.sleep(0.3)
        print(f"Your new video is ready:\n{output_path}\n")
        time.sleep(0.3)
        print("All set — enjoy your glitch buffer video! 🎬")
    except subprocess.CalledProcessError:
        print("\n❌ FFmpeg failed. Make sure it's installed and working in a-Shell.")

if __name__ == "__main__":
    main()
