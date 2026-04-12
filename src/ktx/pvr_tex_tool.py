from pathlib import Path

from ._common import bin_dir, get_executable_path, run
from .exceptions import ToolNotFoundException

_color_space = "sRGB"
_format = "ETC1,UBN,lRGB"
_quality = "etcfast"

_cli_name = "PVRTexToolCLI"
_cli_path = get_executable_path(bin_dir / _cli_name, _cli_name)


class PvrTexTool:
    @classmethod
    def is_available(cls) -> bool:
        return _cli_path is not None

    @classmethod
    def convert_ktx_to_png(
        cls, filepath: Path, output_folder: Path | None = None
    ) -> Path:
        cls._ensure_tool_installed()

        output_filepath = filepath.with_suffix(".png")
        if output_folder is not None:
            output_filepath = output_folder / output_filepath.name

        run(
            f"{_cli_path} -noout -ics {_color_space} -i {filepath!s} -d {output_filepath!s}"
        )

        return output_filepath

    @classmethod
    def convert_png_to_ktx(
        cls, filepath: Path, output_folder: Path | None = None
    ) -> Path:
        cls._ensure_tool_installed()

        output_filepath = filepath.with_suffix(".ktx")
        if output_folder is not None:
            output_filepath = output_folder / output_filepath.name

        run(
            f"{_cli_path} -f {_format} -q {_quality} -i {filepath!s} -o {output_filepath!s}"
        )

        return output_filepath

    @classmethod
    def _ensure_tool_installed(cls):
        if cls.is_available():
            return

        raise ToolNotFoundException("PVRTexTool not found.")
