import yaml
import os

class Config:
    CONFIG_PATH = "config.yaml"

    def __init__(self):
        try:
            with open(self.CONFIG_PATH, 'r') as file:
                self.config_data = yaml.safe_load(file)
                if self.config_data is None:  # Handle empty file case
                    self.config_data = {}
        except FileNotFoundError:
            print(f"Error: Config file not found at {self.CONFIG_PATH}")
        except Exception as e:
            print(f"Error reading YAML: {e}")

    def _save_yaml(self):
        with open(self.CONFIG_PATH, 'w') as file:
            yaml.dump(self.config_data, file)

    def modify_video_output_dir(self, path: str):
        if os.path.isdir(path):
            self.config_data.setdefault('paths', {})['video_output_dir'] = path
        else:
            raise NotADirectoryError()
        self._save_yaml()

    def modify_tts_model_name(self, name: str):
        self.config_data.setdefault('audio', {}).setdefault('tts_model', {})['model_name'] = name
        self._save_yaml()

    def modify_tts_device(self, device: str):
        self.config_data.setdefault('audio', {}).setdefault('tts_model', {})['device'] = device
        self._save_yaml()

    def modify_inference_params_nfe_step(self, nfe_step: int):
        self.config_data.setdefault('audio', {}).setdefault('inference_params', {})['nfe_step'] = nfe_step
        self._save_yaml()

    def modify_inference_params_seed(self, seed: int):
        self.config_data.setdefault('audio', {}).setdefault('inference_params', {})['seed'] = seed
        self._save_yaml()

    def add_voice(self, name:str, ref_file: str, ref_text: str, speed: float):
        if os.path.isfile(ref_file):
            self.config_data.setdefault('audio', {}).setdefault('voices', {}).setdefault(name, {})
            self.config_data['audio']['voices'][name]['ref_file'] = ref_file
            self.config_data['audio']['voices'][name]['ref_text'] = ref_text
            self.config_data['audio']['voices'][name]['speed'] = speed
        else:
            raise FileNotFoundError()
        self._save_yaml()

    def modify_char1_image_default(self, image: str):
        if os.path.isfile(image):
            self.config_data.setdefault('video', {}).setdefault('characters', {}).setdefault('char1', {})['image_default'] = image
        else:
            raise FileNotFoundError()

    def modify_char2_image_default(self, image: str):
        if os.path.isfile(image):
            self.config_data.setdefault('video', {}).setdefault('characters', {}).setdefault('char2', {})['image_default'] = image
        else:
            raise FileNotFoundError()

    def modify_char1_image_pointing(self, image: str):
        if os.path.isfile(image):
            self.config_data.setdefault('video', {}).setdefault('characters', {}).setdefault('char1', {})['image_pointing'] = image
        else:
            raise FileNotFoundError()

    def modify_char2_image_pointing(self, image: str):
        if os.path.isfile(image):
            self.config_data.setdefault('video', {}).setdefault('characters', {}).setdefault('char2', {})['image_pointing'] = image
        else:
            raise FileNotFoundError()

    def modify_char1_position_default(self, pos: [str, int]):
        self.config_data.setdefault('video', {}).setdefault('characters', {}).setdefault('char1', {})['position_default'] = pos

    def modify_char2_position_default(self, pos: [str, int]):
        self.config_data.setdefault('video', {}).setdefault('characters', {}).setdefault('char2', {})['position_default'] = pos

    def modify_char1_position_pointing(self, pos: [int, int]):
        self.config_data.setdefault('video', {}).setdefault('characters', {}).setdefault('char1', {})['position_pointing'] = pos

    def modify_char2_position_pointing(self, pos: [int, int]):
        self.config_data.setdefault('video', {}).setdefault('characters', {}).setdefault('char2', {})['position_pointing'] = pos

    def modify_char1_size_ratio(self, size_ratio: float):
        self.config_data.setdefault('video', {}).setdefault('characters', {}).setdefault('char1', {})['size_ratio'] = size_ratio

    def modify_char2_size_ratio(self, size_ratio: float):
        self.config_data.setdefault('video', {}).setdefault('characters', {}).setdefault('char2', {})['size_ratio'] = size_ratio

    def modify_image_overlay_size_ratio(self, size_ratio: float):
        self.config_data.setdefault('video', {}).setdefault('image_overlays', {})['size_ratio'] = size_ratio

    def modify_image_overlay_position_char1(self, pos: [int, int]):
        self.config_data.setdefault('video', {}).setdefault('image_overlays', {})['position_char1'] = pos

    def modify_image_overlay_position_char2(self, pos: [int, int]):
        self.config_data.setdefault('video', {}).setdefault('image_overlays', {})['position_char2'] = pos

    def modify_caption_font(self, font: str):
        self.config_data.setdefault('video', {}).setdefault('captions', {})['font'] = font
        self._save_yaml()

    def modify_caption_font_size(self, font_size: int):
        self.config_data.setdefault('video', {}).setdefault('captions', {})['font_size'] = font_size
        self._save_yaml()

    def modify_caption_max_line_length(self, max_len: int):
        self.config_data.setdefault('video', {}).setdefault('captions', {})['max_line_length'] = max_len
        self._save_yaml()

    def modify_caption_max_width_ratio(self, width_ratio: float):
        self.config_data.setdefault('video', {}).setdefault('captions', {})['max_width_ratio'] = width_ratio
        self._save_yaml()

    def modify_caption_position(self, pos: [str, int]):
        self.config_data.setdefault('video', {}).setdefault('captions', {})['position'] = pos
        self._save_yaml()

    def modify_caption_color_rgb(self, color: [int, int, int]):
        self.config_data.setdefault('video', {}).setdefault('captions', {})['color_rgb'] = color
        self._save_yaml()

    def modify_caption_stroke_color_rgb(self, color: [int, int, int]):
        self.config_data.setdefault('video', {}).setdefault('captions', {})['stroke_color_rgb'] = color
        self._save_yaml()

    def modify_caption_stroke_width(self, width: int):
        self.config_data.setdefault('video', {}).setdefault('captions', {})['stroke_width'] = width
        self._save_yaml()

    def modify_caption_margin(self, margin: [int, int]):
        self.config_data.setdefault('video', {}).setdefault('captions', {})['margin'] = margin
        self._save_yaml()

    def modify_render_codec(self, codec: str):
        self.config_data.setdefault('video', {}).setdefault('render', {})['codec'] = codec
        self._save_yaml()

    def modify_render_audio_codec(self, audio_codec: str):
        self.config_data.setdefault('video', {}).setdefault('render', {})['audio_codec'] = audio_codec
        self._save_yaml()

    def modify_render_threads(self, threads: int):
        self.config_data.setdefault('video', {}).setdefault('render', {})['threads'] = threads
        self._save_yaml()

    def modify_render_ffmpeg_params(self, params: [str]):
        self.config_data.setdefault('video', {}).setdefault('render', {})['ffmpeg_params'] = params
        self._save_yaml()