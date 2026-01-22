import random
import os
from .utils import gen_paths, chunk_caption_text
from .config import Config
from moviepy import VideoFileClip, AudioFileClip, ImageClip, TextClip, concatenate_audioclips, CompositeVideoClip


class VideoRenderer:
    def __init__(self, imgChar1, imgChar2, imgChar1Pointing, imgChar2Pointing, script):
        # Inițializăm configurația
        self.cfg = Config()
        self.config_data = self.cfg.config_data

        self.imgChar1 = imgChar1
        self.imgChar2 = imgChar2
        self.imgChar1Pointing = imgChar1Pointing
        self.imgChar2Pointing = imgChar2Pointing
        self.script = script["msg"]
        self.imgs = script["img"]

        # Folosim calea din config pentru videoclipurile de fundal
        bg_path_config = self.config_data['paths']['background_videos']
        bgVideos = gen_paths(bg_path_config)

        if not bgVideos:
            raise Exception(f"Nu s-au găsit videoclipuri de fundal în: {bg_path_config}")

        self.bgVideoPath = bgVideos[random.randint(0, len(bgVideos) - 1)]

    def render_video(self, index):
        bgVideo = None
        finalAudio = None
        allAudioClips = []

        try:
            # Setări video/render din config
            video_conf = self.config_data['video']
            paths_conf = self.config_data['paths']

            bgVideo = VideoFileClip(self.bgVideoPath)
            video_w, video_h = bgVideo.size

            overlayClips = []
            currentTime = 0.0

            # Directorul pentru fișierele audio temporare
            temp_audio_dir = paths_conf['temp_audio']

            for i in range(len(self.script)):
                # Construim calea către audio generat
                audio_path = os.path.join(temp_audio_dir, f"audio{i}.wav")
                if not os.path.exists(audio_path):
                    # Fallback simplu dacă path-ul din config nu are slash la final sau e diferit
                    audio_path = f"assets/tmp/audio/audio{i}.wav"

                audioClip = AudioFileClip(audio_path)
                clipDuration = audioClip.duration
                allAudioClips.append(audioClip)

                # --- LOGICA PENTRU IMAGINI (PERSONAJE & OVERLAYS) ---
                is_char1 = (i % 2 == 0)  # Index par = Personaj 1

                # Încărcăm setările specifice personajului din config
                char_key = 'char1' if is_char1 else 'char2'
                char_settings = video_conf['characters'][char_key]

                if i in self.imgs:
                    # Cazul când personajul arată spre ceva (Pointing)
                    charPath = self.imgChar1Pointing if is_char1 else self.imgChar2Pointing

                    # Poziția și dimensiunea din config
                    charPos = tuple(char_settings['position_pointing'])

                    # Imaginea Overlay (ex: mâncarea/obiectul)
                    img = self.imgs[i]
                    overlay_settings = video_conf['image_overlays']

                    # Poziția imaginii overlay în funcție de cine vorbește
                    overlay_pos_key = 'position_char1' if is_char1 else 'position_char2'
                    imgPos = tuple(overlay_settings[overlay_pos_key])
                    imgSizeRatio = overlay_settings['size_ratio']

                    imgClip = (ImageClip(img, transparent=False, duration=clipDuration)
                               .with_start(currentTime)
                               .resized(width=int(video_w * imgSizeRatio))
                               .with_position(imgPos)
                               )
                    overlayClips.append(imgClip)
                else:
                    # Cazul standard (Default)
                    charPath = self.imgChar1 if is_char1 else self.imgChar2

                    # Verificăm dacă poziția e specificată ca listă sau string (ex: 'center')
                    raw_pos = char_settings['position_default']
                    charPos = (raw_pos[0], raw_pos[1]) if isinstance(raw_pos, list) else tuple(raw_pos)

                # Adăugăm clipul cu personajul
                charSizeRatio = char_settings['size_ratio']

                charImgClip = (ImageClip(charPath, transparent=True, duration=clipDuration)
                               .with_start(currentTime)
                               .resized(height=int(video_h * charSizeRatio))
                               .with_position(charPos)
                               )
                overlayClips.append(charImgClip)

                # --- LOGICA PENTRU SUBTITRĂRI (CAPTIONS) ---
                captions_conf = video_conf['captions']

                # Chunking text
                max_line_len = captions_conf.get('max_line_length', 15)
                captionChunks = chunk_caption_text(self.script[i], max_len=max_line_len)

                totalChars = len(self.script[i])
                chunkStartTime = 0.0

                for chunkText in captionChunks:
                    chunkChars = len(chunkText)
                    # Evităm împărțirea la zero
                    proportion = chunkChars / totalChars if totalChars > 0 else 1
                    chunkDuration = clipDuration * proportion

                    maxCaptionW = int(video_w * captions_conf['max_width_ratio'])

                    # Parametrii fontului din config
                    txtClip = (TextClip(text=chunkText,
                                        font_size=captions_conf['font_size'],
                                        color=tuple(captions_conf['color_rgb']),
                                        stroke_color=tuple(captions_conf['stroke_color_rgb']),
                                        stroke_width=captions_conf['stroke_width'],
                                        font=captions_conf['font'],
                                        method='caption',
                                        size=(maxCaptionW, None),
                                        margin=tuple(captions_conf.get('margin', [15, 15])),
                                        text_align='center'
                                        )
                               .with_start(currentTime + chunkStartTime)
                               .with_duration(chunkDuration)
                               .with_position(tuple(captions_conf['position']))
                               )

                    chunkStartTime += chunkDuration
                    overlayClips.append(txtClip)

                currentTime += clipDuration

            # --- ASAMBLAREA FINALĂ ---
            finalAudio = concatenate_audioclips(allAudioClips)
            totalVideoDuration = currentTime

            finalBg = bgVideo.subclipped(0, totalVideoDuration)
            finalComposition = CompositeVideoClip([finalBg] + overlayClips, size=finalBg.size)
            finalVideo = finalComposition.with_audio(finalAudio)

            # Output path
            output_dir = paths_conf['video_output_dir']
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)

            output_filename = os.path.join(output_dir, f"vid{index}.mp4")

            # Render settings din config
            render_conf = video_conf['render']

            finalVideo.write_videofile(
                output_filename,
                codec=render_conf['codec'],
                audio_codec=render_conf['audio_codec'],
                temp_audiofile=paths_conf.get('temp_mux_audio', 'temp-audio.m4a'),
                remove_temp=True,
                ffmpeg_params=render_conf['ffmpeg_params'],
                threads=render_conf['threads']
            )

            # Cleanup
            finalBg.close()
            finalVideo.close()

        except Exception as e:
            print(f"Unexpected error: {e}")
            import traceback
            traceback.print_exc()
        finally:
            if bgVideo: bgVideo.close()
            if finalAudio: finalAudio.close()
            if 'allAudioClips' in locals():
                for clip in allAudioClips:
                    try:
                        clip.close()
                    except:
                        pass