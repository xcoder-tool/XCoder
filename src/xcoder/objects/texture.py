from __future__ import annotations

from typing import TYPE_CHECKING, TypeAlias

from PIL import Image
import zstandard

from ktx import get_image_from_ktx_data
from xcoder.bytestream import Reader, Writer
from xcoder.console import Console
from xcoder.images import join_image, load_image_from_buffer, split_image
from xcoder.localization import locale
from xcoder.pixel_utils import get_pixel_encode_function, get_raw_mode

if TYPE_CHECKING:
    from xcoder.swf import SupercellSWF


PixelType: TypeAlias = int

_interleaved_tags = (27, 28, 29)


class SWFTexture:
    def __init__(
        self, *, width: int = 0, height: int = 0, pixel_type: PixelType = -1
    ) -> None:
        self.width: int = width
        self.height: int = height

        self.pixel_type: PixelType = pixel_type

        self.image: Image.Image | None = None

    def load(self, swf: SupercellSWF, tag: int, has_texture: bool) -> None:
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

    def save(self, writer: Writer, tag: int, has_texture: bool) -> None:
        writer.write_ubyte(self.pixel_type)
        writer.write_uint16(self.width)
        writer.write_uint16(self.height)

        if not has_texture:
            return

        assert self.image is not None
        image = self.image

        if tag in _interleaved_tags:
            image = split_image(self.image)

        raw_mode = get_raw_mode(self.pixel_type)
        encode_pixel = get_pixel_encode_function(self.pixel_type)

        width, height = image.size

        pixels = image.getdata()

        # Note: Some packers for raw_encoder are absent
        # https://github.com/python-pillow/Pillow/blob/58e48745cc7b6c6f7dd26a50fe68d1a82ea51562/src/encode.c#L337
        # https://github.com/python-pillow/Pillow/blob/main/src/libImaging/Pack.c#L668
        if raw_mode != image.mode and encode_pixel is not None:
            for y in range(height):
                for x in range(width):
                    writer.write(encode_pixel(pixels[y * width + x]))  # type: ignore

                Console.progress_bar(locale.writing_pic, y, height)

            return

        writer.write(image.tobytes("raw", raw_mode, 0, 1))
        Console.progress_bar(locale.writing_pic, height - 1, height)

    def _load_texture(self, reader: Reader, tag: int) -> Image.Image:
        if tag in _interleaved_tags:
            return join_image(self.pixel_type, self.width, self.height, reader)

        return load_image_from_buffer(self.pixel_type, self.width, self.height, reader)
