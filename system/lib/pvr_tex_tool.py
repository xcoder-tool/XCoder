import os
import tempfile
from pathlib import Path

from PIL import Image

from system import run
from system.exceptions.tool_not_found import ToolNotFoundException

_main_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
_color_space = "sRGB"
_format = "ETC1,UBN,lRGB"
_quality = "etcfast"


# Note: a solution from
# https://stackoverflow.com/questions/11210104/check-if-a-program-exists-from-a-python-script
def _get_executable_path(*paths: str) -> str | None:
    from shutil import which

    for path in paths:
        executable_path = which(path)
        if executable_path is not None:
            return path

    return None


_cli_name = "PVRTexToolCLI"
_cli_path = _get_executable_path(f"{_main_dir}/system/bin/{_cli_name}", _cli_name)


def can_use_pvr_tex_tool() -> bool:
    return _cli_path is not None


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
    _ensure_tool_installed()

    output_filepath = filepath.with_suffix(".png")
    if output_folder is not None:
        output_filepath = output_folder / output_filepath.name

    run(
        f"{_cli_path} -noout -ics {_color_space} -i {filepath!s} -d {output_filepath!s}"
    )

    return output_filepath


def convert_png_to_ktx(filepath: Path, output_folder: Path | None = None) -> Path:
    _ensure_tool_installed()

    output_filepath = filepath.with_suffix(".ktx")
    if output_folder is not None:
        output_filepath = output_folder / output_filepath.name

    run(
        f"{_cli_path} -f {_format} -q {_quality} -i {filepath!s} -o {output_filepath!s}"
    )

    return output_filepath


def _ensure_tool_installed():
    if can_use_pvr_tex_tool():
        return

    raise ToolNotFoundException("PVRTexTool not found.")
