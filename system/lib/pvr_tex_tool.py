import os
import tempfile
from pathlib import Path

from PIL import Image

from system import run

TOOL_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
COLOR_SPACE = "sRGB"
KTX_FORMAT = "ETC1,UBN,lRGB"
QUALITY = "etcfast"
CLI_PATH = f"{TOOL_DIR}/system/bin/PVRTexToolCLI"


def get_image_from_ktx_data(data: bytes) -> Image.Image:
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".ktx")
    try:
        tmp.write(data)
    finally:
        tmp.close()

    image = get_image_from_ktx(Path(tmp.name))
    os.remove(tmp.name)

    return image


def get_image_from_ktx(filepath: Path) -> Image.Image:
    png_filepath = convert_ktx_to_png(filepath)
    image_open = Image.open(png_filepath)
    image = image_open.copy()
    image_open.close()
    os.remove(png_filepath)
    return image


def convert_ktx_to_png(filepath: Path, output_folder: Path | None = None) -> Path:
    output_filepath = filepath.with_suffix(".png")
    if output_folder is not None:
        output_filepath = output_folder / output_filepath.name

    run(f"{CLI_PATH} -noout -ics {COLOR_SPACE} -i {filepath!s} -d {output_filepath!s}")

    return output_filepath


def convert_png_to_ktx(filepath: Path, output_folder: Path | None = None) -> Path:
    output_filepath = filepath.with_suffix(".ktx")
    if output_folder is not None:
        output_filepath = output_folder / output_filepath.name

    run(
        f"{CLI_PATH} -f {KTX_FORMAT} -q {QUALITY} "
        f"-i {filepath!s} -o {output_filepath!s}"
    )

    return output_filepath
