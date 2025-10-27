#!/usr/bin/env python3
"""
Video Buffer Generator (iSH / iPhone-Friendly)
Joins an MP4 video with a glitch buffer using FFmpeg.

Educational purposes only.
"""

import os
import subprocess
import time

def list_videos_in_directory(directory="."):
    """List all MP4 files in the specified directory."""
    return [f for f in os.listdir(directory) if f.lower().endswith(".mp4")]

def select_video():
    """Let the user select a video file from a list of available MP4s."""
    while True:
        current_dir = os.getcwd()
        videos = list_videos_in_directory(current_dir)

        if not videos:
            print("Hmm, I didn’t find any MP4 videos in this folder.")
            print("You can paste a full file path manually instead.\n")
            path = input("Enter full path to MP4 video: ").strip()
            if os.path.exists(path):
                return path
            print("File not found — let’s try that again.\n")
            continue

        print("\n=== Available MP4 Videos ===")
        for i, vid in enumerate(videos, 1):
            print(f"{i}. {vid}")
        print("(Or type a full path manually)\n")

        choice = input("Select your video to make Buffer Video: ").strip()

        if choice.isdigit():
            index = int(choice)
            if 1 <= index <= len(videos):
                return os.path.join(current_dir, videos[index - 1])
            else:
                print("That number doesn’t match any file — try again.\n")
        else:
            if os.path.exists(choice):
                return choice
            else:
                print("File not found — check your path and try again.\n")

def main():
    print("=== Video Buffer Generator ===\n")

    video_path = select_video()

    glitch_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "RawBuffer", "glitch.mp4")
    if not os.path.exists(glitch_path):
        print(f"Oops! Missing glitch video at {glitch_path}")
        return

    while True:
        output_path = input("Enter output path (including filename, .mp4): ").strip()
        if output_path:
            output_dir = os.path.dirname(output_path)
            if output_dir and not os.path.exists(output_dir):
                os.makedirs(output_dir)
            break

    concat_list = os.path.join(output_dir or ".", "temp_list.txt")
    with open(concat_list, "w", encoding="utf-8") as f:
        f.write(f"file '{video_path}'\n")
        f.write(f"file '{glitch_path}'\n")

    print("\nAlright, generating your buffer video...")
    time.sleep(1)
    print("This might take a few seconds, hang tight ⏳")

    cmd = ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", concat_list, "-c", "copy", output_path]

    try:
        subprocess.run(cmd, check=True)
        os.remove(concat_list)
        time.sleep(0.5)
        print("\nDone! ✅")
        time.sleep(0.3)
        print(f"Your new video is ready and saved to:\n{output_path}\n")
        time.sleep(0.3)
        print("All set — enjoy your glitch buffer video! 🎬")
    except subprocess.CalledProcessError:
        print("\nHmm... something went wrong with FFmpeg.")
        print("Make sure it’s installed and try again.")

if __name__ == "__main__":
    main()
