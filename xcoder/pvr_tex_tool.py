import os
import tempfile
from pathlib import Path

from PIL import Image

from xcoder import run
from xcoder.exceptions import ToolNotFoundException

_main_dir = Path(__file__).parent
_color_space = "sRGB"
_format = "ETC1,UBN,lRGB"
_quality = "etcfast"


# Note: a solution from
# https://stackoverflow.com/questions/11210104/check-if-a-program-exists-from-a-python-script
def _get_executable_path(
    *paths: os.PathLike[str] | str,
) -> os.PathLike[str] | str | None:
    from shutil import which

    for path in paths:
        # Fix of https://github.com/xcoder-tool/XCoder/issues/22
        executable_path = which(path)
        if executable_path is not None:
            return path

    return None


_cli_name = "PVRTexToolCLI"
_cli_path = _get_executable_path(_main_dir / f"bin/{_cli_name}", _cli_name)


def can_use_pvr_tex_tool() -> bool:
    return _cli_path is not None


# noinspection PyTypeChecker
def get_image_from_ktx_data(data: bytes) -> Image.Image:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".ktx") as tmp:
        tmp.write(data)

    try:
        image = get_image_from_ktx(Path(tmp.name))
    finally:
        os.remove(tmp.name)

    return image


# noinspection PyTypeChecker
def get_image_from_ktx(filepath: Path) -> Image.Image:
    png_filepath = convert_ktx_to_png(filepath)
    image_open = Image.open(png_filepath)

    try:
        return image_open.copy()
    finally:
        image_open.close()
        os.remove(png_filepath)


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
