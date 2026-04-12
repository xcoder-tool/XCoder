from pathlib import Path

from ._common import bin_dir, get_executable_path, run
from .exceptions import ToolNotFoundException

_toktx_cli_name = "toktx"
_toktx_cli_path = get_executable_path(bin_dir / _toktx_cli_name, _toktx_cli_name)

_ktx_cli_name = "ktx"
_ktx_cli_path = get_executable_path(bin_dir / _ktx_cli_name, _ktx_cli_name)

_ktx2ktx2_cli_name = "ktx2ktx2"
_ktx2ktx2_cli_path = get_executable_path(
    bin_dir / _ktx2ktx2_cli_name, _ktx2ktx2_cli_name
)


class KhronosKtxTool:
    @classmethod
    def is_available(cls) -> bool:
        return (
            _ktx_cli_path is not None
            and _ktx2ktx2_cli_path is not None
            and _toktx_cli_path is not None
        )

    @classmethod
    def convert_ktx_to_png(
        cls, filepath: Path, output_folder: Path | None = None
    ) -> Path:
        cls._ensure_tool_installed()

        ktx2_filepath = filepath.with_suffix(".ktx2")
        output_filepath = filepath.with_suffix(".png")
        if output_folder is not None:
            output_filepath = output_folder / output_filepath.name

        run(f"{_ktx2ktx2_cli_path} {filepath!s}")
        run(f"{_ktx_cli_path} extract {ktx2_filepath!s} {output_filepath!s}")

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
            f"{_toktx_cli_path} --encode etc1s --genmipmap {output_filepath!s} {filepath!s}"
        )

        return output_filepath

    @classmethod
    def _ensure_tool_installed(cls):
        if cls.is_available():
            return

        raise ToolNotFoundException("ktx-tool not found.")
