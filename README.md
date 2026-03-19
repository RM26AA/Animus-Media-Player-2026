# Animus Media Player

Animus Media Player is a custom-built media player inspired by the Assassin’s Creed Animus interface.

This project was created to solve a simple frustration — the lack of basic playback controls in certain cinematic sequences. Instead of accepting it, I built my own solution that allows full control over video and audio playback.

---

## Features

* Play MP4 and MP3 files
* Pause, rewind, and fast-forward controls
* Interactive timeline slider
* Volume control
* Fullscreen mode
* Keyboard shortcuts (space, arrows, etc.)
* Startup intro animation
* Custom UI styling inspired by Assassin’s Creed
* Button click sound effects

---

## Controls

* **Space** → Pause / Resume
* **Left Arrow** → Rewind 10 seconds
* **Right Arrow** → Forward 10 seconds
* **F** → Toggle fullscreen
* **ESC** → Exit fullscreen

---

## Requirements

* Python 3
* PyQt6
* VLC (installed on system)
* python-vlc

---

## Installation

1. Install dependencies:

```bash
pip install PyQt6 python-vlc
```

2. Make sure VLC Media Player is installed on your system.

3. Place all required files in the same folder:

```
main.py
intro.mp4
click.wav
wallpaper-ezio-1.jpg
WatatsukiTechSans-GOJxA.ttf
Assassins_creed_logo.png
```

4. Run the application:

```bash
python main.py
```

---

## Project Motivation

While watching cinematic content, I noticed the lack of basic playback controls such as pause, rewind, and skip. Instead of working around the limitation, I built a custom media player that restores full control and enhances the experience.

---

## Future Improvements

* Playlist system
* Timestamp display
* Album art for audio
* UI animations and transitions
* Enhanced media library

---

## Disclaimer

This project is a personal, educational project inspired by the Assassin’s Creed aesthetic. It is not affiliated with or endorsed by Ubisoft.
