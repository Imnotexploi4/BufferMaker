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

SUPPORTED_FORMATS = (
    ".mp4", ".mov", ".avi", ".mkv", ".flv", ".webm",
    ".mpeg", ".mpg", ".m4v", ".3gp", ".wav", ".flac"
)


# === Utility Functions ===
def list_all_videos(base_dir):
    """Recursively search for all supported video/audio files."""
    video_files = []
    for root, _, files in os.walk(base_dir):
        for name in files:
            ext = os.path.splitext(name.lower())[1]
            if ext in SUPPORTED_FORMATS and ext != ".mp3":
                video_files.append(os.path.join(root, name))
    return sorted(video_files)


def ffmpeg_supports_libx264():
    """Check if FFmpeg supports libx264 encoder."""
    try:
        result = subprocess.run(["ffmpeg", "-hide_banner", "-codecs"], capture_output=True, text=True)
        return "libx264" in result.stdout
    except Exception:
        return False


def is_ios_shell():
    """Detect if running in a-Shell or iSH (iOS)."""
    shell = os.environ.get("SHELL", "").lower()
    return "ish" in shell or "a-shell" in shell or "ios" in SYSTEM


def convert_to_mp4(input_path):
    """
    Converts any video/audio file to MP4 format using FFmpeg.
    Removes unsupported options automatically for a-Shell/iSH.
    """
    base, _ = os.path.splitext(input_path)
    output_path = base + "_converted.mp4"

    if os.path.exists(output_path):
        print(f"\n⚠️  Converted file already exists: {output_path}")
        return output_path

    print(f"\n🎞️  Converting '{os.path.basename(input_path)}' → MP4...")

    # Detect if input has a video stream
    probe = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v",
         "-show_entries", "stream=codec_type", "-of", "csv=p=0", input_path],
        capture_output=True, text=True
    )
    is_audio_only = (probe.returncode == 0 and "video" not in probe.stdout)

    # Decide codecs
    ios_mode = is_ios_shell()
    use_libx264 = ffmpeg_supports_libx264()

    if is_audio_only:
        # Convert audio-only to mp4 container
        cmd = [
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-i", input_path,
            "-c:a", "aac", "-b:a", "192k",
            "-vn", "-movflags", "+faststart",
            output_path
        ]
    else:
        # Use libx264 if available; else fallback to mpeg4
        vcodec = "libx264" if use_libx264 else "mpeg4"
        cmd = [
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-i", input_path,
            "-c:v", vcodec,
            "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "192k",
            "-movflags", "+faststart",
            output_path
        ]

        # Add preset only if NOT in a-Shell / iSH
        if not ios_mode and vcodec == "libx264":
            cmd.insert(cmd.index("-pix_fmt"), "-preset")
            cmd.insert(cmd.index("-pix_fmt") + 1, "fast")

    try:
        subprocess.run(cmd, check=True)
        print(f"✅ Converted successfully: {output_path}\n")
        return output_path
    except subprocess.CalledProcessError:
        print(f"❌ Conversion failed for {input_path}")
        print("⚠️ Make sure FFmpeg is installed and supports your input codec.")
        return None


def select_video(videos):
    """Let the user select a video file from the list."""
    if not videos:
        print(f"\nNo supported video files found in {DEFAULT_SEARCH_DIR}.")
        print("Please copy videos there and try again.\n")
        return None

    print("\n=== Found Video/Audio Files ===")
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

    print(f"Scanning for videos in: {DEFAULT_SEARCH_DIR} ...")
    videos = list_all_videos(DEFAULT_SEARCH_DIR)

    video_path = select_video(videos)
    if not video_path:
        return

    if not video_path.lower().endswith(".mp4"):
        converted = convert_to_mp4(video_path)
        if not converted:
            return
        video_path = converted

    glitch_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "RawBuffer", "glitch.mp4")
    if not os.path.exists(glitch_path):
        print(f"❌ Missing glitch video at {glitch_path}")
        return

    print()
    buffer_name = input("Name your Buffer Video file (without .mp4): ").strip()
    if not buffer_name:
        buffer_name = os.path.splitext(os.path.basename(video_path))[0] + "_buffered"

    if not buffer_name.lower().endswith(".mp4"):
        buffer_name += ".mp4"

    base_dir = os.path.dirname(video_path)
    output_path = os.path.join(base_dir, buffer_name)

    concat_list = os.path.join(base_dir, "temp_list.txt")
    with open(concat_list, "w", encoding="utf-8") as f:
        f.write(f"file '{video_path}'\n")
        f.write(f"file '{glitch_path}'\n")

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
