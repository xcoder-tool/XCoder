import os

from PIL import Image

from system.lib.images import (
    get_format_by_pixel_type,
    join_image,
    load_image_from_buffer,
    load_texture,
)
from system.lib.pvr_tex_tool import get_image_from_ktx_data


class SWFTexture:
    def __init__(self):
        self.width = 0
        self.height = 0

        self.pixel_type = -1

        self.image: Image.Image

    def load(self, swf, tag: int, has_texture: bool):
        if tag == 45:
            khronos_texture_length = swf.reader.read_int()

        self.pixel_type = swf.reader.read_char()
        self.width, self.height = (swf.reader.read_ushort(), swf.reader.read_ushort())

        if not has_texture:
            return

        if tag == 45:
            # noinspection PyUnboundLocalVariable
            khronos_texture_data = swf.reader.read(khronos_texture_length)
            self.image = get_image_from_ktx_data(khronos_texture_data)
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
