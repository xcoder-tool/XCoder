import os
from pathlib import Path
import tempfile
from typing import ClassVar

from PIL import Image

from ktx.exceptions import ToolNotFoundException

from .ktx_tool import KhronosKtxTool
from .pvr_tex_tool import PvrTexTool
from .tool_protocol import KtxToolProtocol


def get_image_from_ktx_data(data: bytes) -> Image.Image:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".ktx1") as tmp:
        tmp.write(data)

    try:
        image = get_image_from_ktx(Path(tmp.name))
    finally:
        os.remove(tmp.name)

    return image


def get_image_from_ktx(filepath: Path) -> Image.Image:
    png_filepath = KtxTool.convert_ktx_to_png(filepath)
    image_open = Image.open(png_filepath)

    try:
        return image_open.copy()
    finally:
        image_open.close()
        os.remove(png_filepath)


class KtxTool:
    TOOLS: ClassVar[tuple[KtxToolProtocol, ...]] = (
        KhronosKtxTool,
        PvrTexTool,
    )

    @classmethod
    def is_available(cls) -> bool:
        for tool in cls.TOOLS:
            if tool.is_available():
                return True

        return False

    @classmethod
    def convert_ktx_to_png(
        cls, filepath: Path, output_folder: Path | None = None
    ) -> Path:
        for tool in cls.TOOLS:
            if not tool.is_available():
                continue

            return tool.convert_ktx_to_png(filepath, output_folder)

        raise ToolNotFoundException("No tools available for ktx handling")

    @classmethod
    def convert_png_to_ktx(
        cls, filepath: Path, output_folder: Path | None = None
    ) -> Path:
        for tool in cls.TOOLS:
            if not tool.is_available():
                continue

            return tool.convert_png_to_ktx(filepath, output_folder)

        raise ToolNotFoundException("No tools available for ktx handling")
