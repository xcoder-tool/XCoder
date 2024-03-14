from __future__ import annotations

import os
from typing import TYPE_CHECKING

import zstandard
from PIL import Image

from system.lib.images import (
    get_format_by_pixel_type,
    join_image,
    load_image_from_buffer,
    load_texture,
)
from system.lib.pvr_tex_tool import get_image_from_ktx_data

if TYPE_CHECKING:
    from system.lib.swf import SupercellSWF


class SWFTexture:
    def __init__(self):
        self.width = 0
        self.height = 0

        self.pixel_type = -1
        self.khronos_texture_filename: str | None = None

        self.image: Image.Image | None = None

    def load(self, swf: SupercellSWF, tag: int, has_texture: bool):
        if tag == 45:
            khronos_texture_length = swf.reader.read_int()
        elif tag == 47:
            self.khronos_texture_filename = swf.reader.read_string()

        self.pixel_type = swf.reader.read_char()
        self.width, self.height = (swf.reader.read_ushort(), swf.reader.read_ushort())

        if not has_texture:
            return

        if tag == 45:
            # noinspection PyUnboundLocalVariable
            khronos_texture_data = swf.reader.read(khronos_texture_length)
            self.image = get_image_from_ktx_data(khronos_texture_data)
            return
        elif tag == 47:
            with open(
                swf.filepath.parent / self.khronos_texture_filename, "rb"
            ) as file:
                decompressor = zstandard.ZstdDecompressor()
                decompressed = decompressor.decompress(file.read())
                self.image = get_image_from_ktx_data(decompressed)
            return

        img = Image.new(
            get_format_by_pixel_type(self.pixel_type), (self.width, self.height)
        )

        load_texture(swf.reader, self.pixel_type, img)

        if tag in (27, 28, 29):
            join_image(img)
        else:
            load_image_from_buffer(img)

        os.remove("pixel_buffer")

        self.image = img
