#!/usr/bin/env python3
"""
Video Buffer Generator (iSH / iPhone-Friendly)
Joins an MP4 video with a glitch buffer using FFmpeg.

Educational purposes only.
"""

import os
import subprocess

def get_file_path(prompt):
    """
    Ask user to provide the full path to a file.
    On iOS, you can copy the path from the Files app.
    """
    path = input(prompt).strip()
    if not os.path.exists(path):
        print(f"Error: File not found: {path}")
        return None
    return path

def main():
    print("=== Video Buffer Generator ===\n")

    # 1. Get input MP4 video
    while True:
        video_path = get_file_path("Enter path to input MP4 video: ")
        if video_path:
            break

    # 2. Glitch buffer video
    glitch_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "RawBuffer", "glitch.mp4")
    if not os.path.exists(glitch_path):
        print(f"Error: Missing glitch video at {glitch_path}")
        return

    # 3. Output path
    while True:
        output_path = input("Enter output path (including filename, .mp4): ").strip()
        if output_path:
            output_dir = os.path.dirname(output_path)
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            break

    # 4. Create temporary concat list for FFmpeg
    concat_list = os.path.join(output_dir, "temp_list.txt")
    with open(concat_list, "w", encoding="utf-8") as f:
        f.write(f"file '{video_path}'\n")
        f.write(f"file '{glitch_path}'\n")

    # 5. Run FFmpeg
    cmd = ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", concat_list, "-c", "copy", output_path]
    print("\nGenerating video buffer... This may take a moment.")

    try:
        subprocess.run(cmd, check=True)
        os.remove(concat_list)
        print(f"\nSuccess! Video saved to: {output_path}")
    except subprocess.CalledProcessError:
        print("\nError: FFmpeg failed to generate video. Make sure FFmpeg is installed and working.")

if __name__ == "__main__":
    main()
