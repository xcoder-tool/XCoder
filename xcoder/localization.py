import json
import os
from pathlib import Path

from xcoder.config import config

_DEFAULT_STRING = "NO LOCALE"
_LIBRARY_DIRECTORY = Path(__file__).parent
_LOCALES_DIRECTORY = _LIBRARY_DIRECTORY / "languages"


class Locale:
    def __init__(self):
        self.xcoder_header: str = _DEFAULT_STRING
        self.detected_os: str = _DEFAULT_STRING
        self.installing: str = _DEFAULT_STRING
        self.update_downloading: str = _DEFAULT_STRING
        self.crt_workspace: str = _DEFAULT_STRING
        self.verifying: str = _DEFAULT_STRING
        self.installed: str = _DEFAULT_STRING
        self.update_done: str = _DEFAULT_STRING
        self.not_installed: str = _DEFAULT_STRING
        self.clear_qu: str = _DEFAULT_STRING
        self.done: str = _DEFAULT_STRING
        self.done_qu: str = _DEFAULT_STRING
        self.choice: str = _DEFAULT_STRING
        self.to_continue: str = _DEFAULT_STRING
        self.experimental: str = _DEFAULT_STRING

        self.sc_label: str = _DEFAULT_STRING
        self.decode_sc: str = _DEFAULT_STRING
        self.encode_sc: str = _DEFAULT_STRING
        self.decode_by_parts: str = _DEFAULT_STRING
        self.encode_by_parts: str = _DEFAULT_STRING
        self.overwrite_by_parts: str = _DEFAULT_STRING
        self.decode_sc_description: str = _DEFAULT_STRING
        self.encode_sc_description: str = _DEFAULT_STRING
        self.decode_by_parts_description: str = _DEFAULT_STRING
        self.encode_by_parts_description: str = _DEFAULT_STRING
        self.overwrite_by_parts_description: str = _DEFAULT_STRING

        self.csv_label: str = _DEFAULT_STRING
        self.decompress_csv: str = _DEFAULT_STRING
        self.compress_csv: str = _DEFAULT_STRING
        self.decompress_csv_description: str = _DEFAULT_STRING
        self.compress_csv_description: str = _DEFAULT_STRING

        self.ktx_label: str = _DEFAULT_STRING
        self.ktx_from_png_label: str = _DEFAULT_STRING
        self.png_from_ktx_label: str = _DEFAULT_STRING
        self.ktx_from_png_description: str = _DEFAULT_STRING
        self.png_from_ktx_description: str = _DEFAULT_STRING

        self.other_features_label: str = _DEFAULT_STRING
        self.check_update: str = _DEFAULT_STRING
        self.reinit: str = _DEFAULT_STRING
        self.change_language: str = _DEFAULT_STRING
        self.clear_directories: str = _DEFAULT_STRING
        self.toggle_update_auto_checking: str = _DEFAULT_STRING
        self.exit: str = _DEFAULT_STRING
        self.version: str = _DEFAULT_STRING
        self.reinit_description: str = _DEFAULT_STRING
        self.change_lang_description: str = _DEFAULT_STRING
        self.clean_dirs_description: str = _DEFAULT_STRING

        self.not_latest: str = _DEFAULT_STRING
        self.collecting_inf: str = _DEFAULT_STRING
        self.about_sc: str = _DEFAULT_STRING
        self.skip_not_installed: str = _DEFAULT_STRING
        self.decompression_error: str = _DEFAULT_STRING
        self.detected_comp: str = _DEFAULT_STRING
        self.unknown_pixel_type: str = _DEFAULT_STRING
        self.crt_pic: str = _DEFAULT_STRING
        self.join_pic: str = _DEFAULT_STRING
        self.png_save: str = _DEFAULT_STRING
        self.saved: str = _DEFAULT_STRING
        self.illegal_size: str = _DEFAULT_STRING
        self.resize_qu: str = _DEFAULT_STRING
        self.resizing: str = _DEFAULT_STRING
        self.split_pic: str = _DEFAULT_STRING
        self.writing_pic: str = _DEFAULT_STRING
        self.compressing_with: str = _DEFAULT_STRING
        self.compression_error: str = _DEFAULT_STRING
        self.compression_done: str = _DEFAULT_STRING
        self.dir_empty: str = _DEFAULT_STRING
        self.texture_not_found: str = _DEFAULT_STRING
        self.file_not_found: str = _DEFAULT_STRING
        self.cut_sprites_process: str = _DEFAULT_STRING
        self.place_sprites_process: str = _DEFAULT_STRING
        self.not_implemented: str = _DEFAULT_STRING
        self.error: str = _DEFAULT_STRING

        self.e1sc1: str = _DEFAULT_STRING
        self.cgl: str = _DEFAULT_STRING
        self.upd_av: str = _DEFAULT_STRING
        self.upd_qu: str = _DEFAULT_STRING
        self.upd: str = _DEFAULT_STRING
        self.upd_ck: str = _DEFAULT_STRING
        self.bkp: str = _DEFAULT_STRING
        self.stp: str = _DEFAULT_STRING

        self.enabled: str = _DEFAULT_STRING
        self.disabled: str = _DEFAULT_STRING

        self.install_to_unlock: str = _DEFAULT_STRING

    def load(self, language: str):
        language_filepath = _LOCALES_DIRECTORY / (language + ".json")
        default_locale_filepath = _LOCALES_DIRECTORY / (
            config.DEFAULT_LANGUAGE + ".json"
        )

        loaded_locale = {}
        if os.path.exists(language_filepath):
            loaded_locale = json.load(open(language_filepath, encoding="utf-8"))  # Any
        english_locale = json.load(open(default_locale_filepath))  # English

        for key in self.__dict__:
            if key in loaded_locale:
                setattr(self, key, loaded_locale[key])
                continue
            setattr(self, key, english_locale[key])

    def change(self):
        language_files = os.listdir(_LOCALES_DIRECTORY)

        for file_index, language_file in enumerate(language_files):
            language_path = _LOCALES_DIRECTORY / language_file
            language_name = json.load(open(language_path, encoding="utf-8"))["name"]

            print(f"{file_index + 1} - {language_name}")

        language_index = input("\n>>> ")
        try:
            language_index = int(language_index) - 1
            if language_index >= 0:
                if language_index < len(language_files):
                    language = ".".join(language_files[language_index].split(".")[:-1])
                    self.load(language)

                    return language
        except ValueError:
            pass

        return self.change()


locale = Locale()
locale.load(config.language)
