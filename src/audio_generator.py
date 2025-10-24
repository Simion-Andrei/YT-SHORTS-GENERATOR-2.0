import os
from f5_tts.api import F5TTS
from importlib.resources import files

class AudioGenerator:
    def __init__(self, voice1, voice2, script):
        self.voices = {
            "peter": {
                "path": "assets/ref_audio/peter.WAV",
                "ref_text": "I'll tell you, Bob, I just got in my car and drove it. And when there was a guy in my way, I killed him.",
                "speed": 0.6
            },
            "stewie": {
                "path": "assets/ref_audio/stewie.mp3",
                "ref_text": "I am a big fan of sundresses.",
                "speed": 1.2
            },
        }

        self.voice1 = self.voices[voice1]
        self.voice2 = self.voices[voice2]
        self.script = script

        self.f5tts = F5TTS(model="F5TTS_v1_Base", device="cuda")

    def generate_audio(self):
        for i, msg in enumerate(self.script):
            output_file = f"assets/tmp/audio/audio{i}.wav"
            ref_file = self.voice1["path"] if i % 2 == 0 else self.voice2["path"]
            ref_text = self.voice1["ref_text"] if i % 2 == 0 else self.voice2["ref_text"]
            speed = self.voice1["speed"] if i % 2 == 0 else self.voice2["speed"]

            self.f5tts.infer(
                ref_file=ref_file,
                ref_text=ref_text,
                gen_text=msg,
                file_wave=output_file,
                nfe_step=32,
                speed=speed,
                seed=153,
            )