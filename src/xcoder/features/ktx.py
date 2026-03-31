import os
from pathlib import Path

from loguru import logger

from ktx import KtxTool
from xcoder.localization import locale

IN_PNG_PATH = Path("./TEX/In-PNG")
IN_KTX_PATH = Path("./TEX/In-KTX")
OUT_PNG_PATH = Path("./TEX/Out-PNG")
OUT_KTX_PATH = Path("./TEX/Out-KTX")


def convert_png_textures_to_ktx():
    assert KtxTool.is_available()

    input_folder = IN_PNG_PATH
    output_folder = OUT_KTX_PATH

    for file in os.listdir(input_folder):
        if not file.endswith(".png"):
            continue

        png_filepath = input_folder / file
        if not os.path.isfile(png_filepath):
            continue

        logger.info(locale.collecting_inf % file)
        KtxTool.convert_png_to_ktx(png_filepath, output_folder=output_folder)


def convert_ktx_textures_to_png():
    assert KtxTool.is_available()

    input_folder = IN_KTX_PATH
    output_folder = OUT_PNG_PATH

    for file in os.listdir(input_folder):
        if not file.endswith(".ktx"):
            continue

        ktx_filepath = input_folder / file
        if not os.path.isfile(ktx_filepath):
            continue

        logger.info(locale.collecting_inf % file)
        KtxTool.convert_ktx_to_png(ktx_filepath, output_folder=output_folder)
