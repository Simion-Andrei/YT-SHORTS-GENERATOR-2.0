import random
from .utils import gen_paths, chunk_caption_text
from moviepy import VideoFileClip, AudioFileClip, ImageClip, TextClip, concatenate_audioclips, CompositeVideoClip, VideoClip


class VideoRenderer:
    def __init__(self, imgChar1, imgChar2, imgChar1Pointing, imgChar2Pointing, script):
        self.imgChar1 = imgChar1
        self.imgChar2 = imgChar2
        self.imgChar1Pointing = imgChar1Pointing
        self.imgChar2Pointing = imgChar2Pointing
        self.script = script["msg"]
        self.imgs = script["img"]

        bgVideos = gen_paths("assets/bgvideos")
        self.bgVideoPath = bgVideos[random.randint(0, len(bgVideos) - 1)]

        self.characterSizeRatio = 0.4
        self.imageSizeRatio = 0.6
        self.captionFontsize = 80
        self.captionFont = 'arialbd'
        self.captionPosition = ('center', 500)

    def render_video(self, index):
        try:
            bgVideo = VideoFileClip(self.bgVideoPath)
            video_w, video_h = bgVideo.size

            allAudioClips = []
            overlayClips = []
            currentTime = 0.0

            for i in range(len(self.script)):
                audioClip = AudioFileClip(f"assets/tmp/audio/audio{i}.wav")
                clipDuration = audioClip.duration
                allAudioClips.append(audioClip)

                if i in self.imgs:
                    charPath = self.imgChar1Pointing if i % 2 == 0 else self.imgChar2Pointing
                    charPos = (-100, 1000) if i % 2 == 0 else (450, 1000)
                    img = self.imgs[i]
                    imgPosX = 400 if i % 2 == 0 else 50
                    imgClip = (ImageClip(img,
                                         transparent=False,
                                         duration=clipDuration)
                                   .with_start(currentTime)
                                   .resized(width=int(video_w * self.imageSizeRatio))
                                   .with_position((imgPosX, 800))
                                   )
                    overlayClips.append(imgClip)
                else:
                    charPath = self.imgChar1 if i % 2 == 0 else self.imgChar2
                    charPos = ('center', 1000)

                charImgClip = (ImageClip(charPath,
                                        transparent=True,
                                        duration=clipDuration)
                               .with_start(currentTime)
                               .resized(height=int(video_h * self.characterSizeRatio))
                               .with_position(charPos)
                               )
                overlayClips.append(charImgClip)

                captionChunks = chunk_caption_text(self.script[i], max_len=15)
                totalChars = len(self.script[i])
                chunkStartTime = 0.0
                for chunkText in captionChunks:
                    chunkChars = len(chunkText)
                    proportion = chunkChars / totalChars
                    chunkDuration = clipDuration * proportion

                    maxCaptionW = int(video_w * 0.6)
                    txtClip = (TextClip(text=chunkText,
                                        font_size=self.captionFontsize,
                                        color=(0, 0, 0),
                                        stroke_color=(255, 255, 255),
                                        stroke_width=6,
                                        font=self.captionFont,
                                        method='caption',
                                        size=(maxCaptionW, None),
                                        margin=(15, 15),
                                        text_align='center'
                                        )
                               .with_start(currentTime + chunkStartTime)
                               .with_duration(chunkDuration)
                               .with_position(self.captionPosition)
                               )

                    chunkStartTime += chunkDuration
                    overlayClips.append(txtClip)

                currentTime += clipDuration

            finalAudio = concatenate_audioclips(allAudioClips)
            totalVideoDuration = currentTime

            finalBg = bgVideo.subclipped(0, totalVideoDuration)

            finalComposition = CompositeVideoClip([finalBg] + overlayClips, size=finalBg.size)

            finalVideo = finalComposition.with_audio(finalAudio)

            finalVideo.write_videofile(f"vid{index}.mp4",
                                       codec="libx264",
                                       audio_codec='aac',
                                       temp_audiofile='temp-audio.m4a',
                                       remove_temp=True,
                                       ffmpeg_params=["-preset", "medium", "-crf", "23"],
                                       threads=12)

            finalBg.close()
            finalAudio.close()
            for clip in allAudioClips: clip.close()
            finalVideo.close()

        except Exception as e:
            print(f"Unexpected error: {e}")
            if 'bg_clip' in locals() and bgVideo: bgVideo.close()
            if 'finalAudio' in locals() and finalAudio: finalAudio.close()
            if 'allAudioClips' in locals():
                for clip in allAudioClips:
                    try: clip.close()
                    except: pass