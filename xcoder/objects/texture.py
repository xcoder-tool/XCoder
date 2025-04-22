from __future__ import annotations

from typing import TYPE_CHECKING

import zstandard
from PIL import Image

from xcoder.bytestream import Reader
from xcoder.images import join_image, load_image_from_buffer
from xcoder.pvr_tex_tool import get_image_from_ktx_data

if TYPE_CHECKING:
    from xcoder.swf import SupercellSWF


class SWFTexture:
    def __init__(self):
        self.width = 0
        self.height = 0

        self.pixel_type = -1

        self.image: Image.Image | None = None

    def load(self, swf: SupercellSWF, tag: int, has_texture: bool):
        assert swf.reader is not None

        khronos_texture_length = 0
        khronos_texture_filename = None
        if tag == 45:
            khronos_texture_length = swf.reader.read_int()
        elif tag == 47:
            khronos_texture_filename = swf.reader.read_string()

        self.pixel_type = swf.reader.read_char()
        self.width, self.height = (swf.reader.read_ushort(), swf.reader.read_ushort())

        if not has_texture:
            return

        khronos_texture_data = None
        if tag == 45:
            # noinspection PyUnboundLocalVariable
            khronos_texture_data = swf.reader.read(khronos_texture_length)
        elif tag == 47:
            assert khronos_texture_filename is not None
            with open(swf.filepath.parent / khronos_texture_filename, "rb") as file:
                decompressor = zstandard.ZstdDecompressor()
                khronos_texture_data = decompressor.decompress(file.read())

        if khronos_texture_data is not None:
            self.image = get_image_from_ktx_data(khronos_texture_data).resize(
                (self.width, self.height), Image.Resampling.LANCZOS
            )
            return

        self.image = self._load_texture(swf.reader, tag)

    def _load_texture(self, reader: Reader, tag: int) -> Image.Image:
        if tag in (27, 28, 29):
            return join_image(self.pixel_type, self.width, self.height, reader)

        return load_image_from_buffer(self.pixel_type, self.width, self.height, reader)
