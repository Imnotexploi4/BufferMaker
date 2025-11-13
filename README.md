# BufferMaker Mobile Version

# DISCLAIMER
This repository is forked from **BufferMaker**. I do **not** claim copyright on the original repository.  
Use responsibly; this script is for **educational purposes** only.

---

# Video Buffer Generator (Mobile Version)

A small Python utility that **stitches an MP4 file to a short glitch clip (`glitch.mp4`)** using `ffmpeg`.  
It provides a **clean buffer between scenes**, fast and without re-encoding (stream copy), so quality is preserved.

---

## What it does
- CLI menu interface – select file, enter output name, done
- Concatenates your clip with `RawBuffer/glitch.mp4`
- Lets you pick the output name and folder
- Optional one-line credit or description you can edit

---

## Before you start
You’ll need:
- Python 3.8 or newer
- FFmpeg installed and in your path

---

## Installing on Mobile

### Android (Termux)
Run each command **separately**:

```bash
pkg update
pkg upgrade
pkg install python
pkg install ffmpeg
termux-setup-storage  # optional, allows Termux to access Downloads
````

### iOS (a-Shell / iSH / a-Shell mini)

* Python 3.8+ (usually preinstalled)
* FFmpeg comes preinstalled in a-Shell
* Place MP4 files in `~/Documents`

---

## Quick Setup

1. Clone or unzip this repo into a folder on your device.
2. Place your MP4 files in the same folder as `app.py`.
3. Ensure `RawBuffer/glitch.mp4` exists.
4. Open terminal / a-Shell and navigate to the folder:

```bash
cd ~/Documents/BufferMaker   # iOS
cd ~/storage/downloads/BufferMaker  # Termux
python3 app.py
```

5. Select your video, enter output name and folder.
6. The new file will appear in your chosen folder (default `output/`).

> **Important:** If you intend to upload a crash video to TikTok or other platforms, this only works if uploading from a PC-side uploader.

---

**Note:**
*This script is created for educational purposes. I am **not responsible** for misuse.*
