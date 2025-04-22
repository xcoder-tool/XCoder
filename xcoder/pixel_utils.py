import struct
from typing import Callable, Literal, TypeAlias

from xcoder.localization import locale

PixelChannels: TypeAlias = tuple[int, ...]
EncodeFunction: TypeAlias = Callable[[PixelChannels], bytes]
RawMode: TypeAlias = Literal["RGBA", "RGBA;4B", "RGBA;15", "BGR;16", "LA", "L"]


def get_raw_mode(pixel_type: int) -> RawMode:
    if pixel_type in _raw_modes:
        return _raw_modes[pixel_type]

    raise Exception(locale.unknown_pixel_type % pixel_type)


def get_pixel_encode_function(pixel_type: int) -> EncodeFunction | None:
    return _encode_functions.get(pixel_type, None)


def get_channel_count_by_pixel_type(pixel_type: int) -> int:
    if pixel_type == 4:
        return 3
    elif pixel_type == 6:
        return 2
    elif pixel_type == 10:
        return 1
    return 4


def _write_rgba8(pixel: PixelChannels) -> bytes:
    return struct.pack("4B", *pixel)


def _write_rgba4(pixel: PixelChannels) -> bytes:
    r, g, b, a = pixel
    return struct.pack("<H", a >> 4 | b >> 4 << 4 | g >> 4 << 8 | r >> 4 << 12)


def _write_rgb5a1(pixel: PixelChannels) -> bytes:
    r, g, b, a = pixel
    return struct.pack("<H", a >> 7 | b >> 3 << 1 | g >> 3 << 6 | r >> 3 << 11)


# TODO: rewrite with numpy https://qna.habr.com/q/298153
# rgb888 = numpy.asarray(Image.open(filename))
# # check that image have 3 color components, each of 8 bits
# assert rgb888.shape[-1] == 3 and rgb888.dtype == numpy.uint8
# r5 = (rgb888[..., 0] >> 3 & 0x1f).astype(numpy.uint16)
# g6 = (rgb888[..., 1] >> 2 & 0x3f).astype(numpy.uint16)
# b5 = (rgb888[..., 2] >> 3 & 0x1f).astype(numpy.uint16)
# rgb565 = r5 << 11 | g6 << 5 | b5
# return rgb565.tobytes()
def _write_rgb565(pixel: PixelChannels) -> bytes:
    r, g, b = pixel
    return struct.pack("<H", b >> 3 | g >> 2 << 5 | r >> 3 << 11)


_encode_functions: dict[int, EncodeFunction] = {
    2: _write_rgba4,
    3: _write_rgb5a1,
    4: _write_rgb565,
}

# here is a problem with these names https://github.com/python-pillow/Pillow/pull/8158
_raw_modes: dict[int, RawMode] = {
    0: "RGBA",
    1: "RGBA",
    2: "RGBA;4B",  # ABGR;4
    3: "RGBA;15",  # ABGR;1555
    4: "BGR;16",  # RGB;565
    6: "LA",
    10: "L",
}
