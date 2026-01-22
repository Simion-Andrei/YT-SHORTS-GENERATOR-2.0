# 🎬 YT Shorts Generator 2.0 (Conversational AI)

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python)
![F5-TTS](https://img.shields.io/badge/AI_Voice-F5--TTS-orange?style=for-the-badge)
![MoviePy](https://img.shields.io/badge/Render-MoviePy-red?style=for-the-badge&logo=moviepy)
![Config](https://img.shields.io/badge/Config-YAML-purple?style=for-the-badge&logo=yaml)

**YT Shorts Generator 2.0** is an automated engine designed to create viral-style conversational short videos (Shorts/Reels/TikTok). 

Unlike generic automation tools, this project leverages **F5-TTS** (a state-of-the-art local voice cloning model) to generate high-fidelity dialogue between characters (e.g., Rick & Morty, Family Guy) without relying on expensive external APIs. It automatically handles video composition, dynamic character switching, contextual overlays, and stylized captions.

---

## ⚡ Key Features

- **🗣️ Local Voice Cloning (F5-TTS)**: Uses the `F5TTS_v1_Base` model to clone voices from reference audio files. Runs locally on your GPU (Free & Unlimited).
- **bust-style Animation**: Automatically switches visible characters based on who is speaking. Supports different states (e.g., "Default" vs "Pointing").
- **🖼️ Contextual Overlays**: Display specific images (like memes, charts, or objects) at exact moments in the dialogue, defined directly in the script.
- **📝 Auto-Captions**: Generates "burned-in" subtitles with customizable fonts, colors, and stroke effects. Handles text chunking for optimal readability.
- **🎥 Dynamic Backgrounds**: Randomly selects high-retention background videos (gameplay, satisfying loops) from your assets folder.

---

## 🛠️ Tech Stack

- **Language**: Python 3.10+
- **AI Audio**: [F5-TTS](https://github.com/SWivid/F5-TTS) (PyTorch/CUDA)
- **Video Engine**: MoviePy & FFmpeg
- **Configuration**: PyYAML

---

## 📂 Project Structure

```text
YT-SHORTS-GENERATOR-2.0/
├── app.py                 # Entry point: Define your scripts and choose characters here
├── src/
│   ├── audio_generator.py # Handles text-to-speech generation using F5-TTS
│   ├── video_renderer.py  # Assembles the video (images, audio, subtitles)
│   ├── utils.py           # Helper functions
│   └── config.py          # Config loader
├── assets/
│   ├── bgvideos/          # Folder for background videos
│   ├── characters/        # Character sprites (Rick, Morty, Peter, etc.)
│   ├── images/            # Overlay images used in scripts
│   ├── ref_audio/         # Reference audio files for voice cloning
│   └── tmp/               # Temporary generated files
└── output/                # Final rendered videos appear here
```

---

## ⚙️ Installation & Setup

### 1. Prerequisites
- **Python 3.10+**
- **NVIDIA GPU** (Required for efficient F5-TTS generation).
- **FFmpeg** installed and added to your system PATH.
- **PyTorch** with CUDA support.

### 2. Install Dependencies

```bash
git clone https://github.com/YourUsername/YT-SHORTS-GENERATOR-2.0
cd YT-SHORTS-GENERATOR-2.0

# Create a virtual environment (Recommended)
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install PyTorch with CUDA first (adjust for your CUDA version)
pip3 install torch torchvision torchaudio --index-url [https://download.pytorch.org/whl/cu118](https://download.pytorch.org/whl/cu118)

# Install project requirements
pip install f5-tts moviepy pyyaml
```
---

## 🎮 How to Use

### 1. Write the Script
Open `app.py`. The `scripts` list contains the dialogue and visual cues.

```python
scripts = [
    {
        "msg": [
            "Hey Morty, look at this readme file!",  # Index 0
            "Aw geez Rick, it looks pretty complicated.", # Index 1
            "It's not complicated, Morty! It's YAML!" # Index 2
        ],
        "img": {
            # At Index 0 (Rick speaks), show 'logo.png' overlay
            0: "assets/images/logo.png" 
        }
    }
]
```

### 2. Select Characters
In `app.py`, set the `idx` variable to choose the character pair defined in your logic:
```python
# 1 = Rick & Morty
# 2 = Peter & Stewie
idx = 1 
```

### 3. Run the Generator
```bash
python app.py
```
*Note: The first run might take longer as it downloads the F5-TTS model weights.*

### 4. Find your Video
The final `.mp4` file will be saved in the `output/` folder defined in your config.

---

## ⚠️ Notes

- **GPU Memory**: F5-TTS is resource-intensive. If you run out of VRAM, try generating shorter scripts or closing other GPU-heavy applications.
- **Asset Rights**: Ensure you have the rights to use the characters, background videos, and fonts in your commercial projects.

---