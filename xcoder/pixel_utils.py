import struct
from typing import Callable, TypeAlias

from xcoder.bytestream import Reader

PixelChannels: TypeAlias = tuple[int, ...]
EncodeFunction: TypeAlias = Callable[[PixelChannels], bytes]
DecodeFunction: TypeAlias = Callable[[Reader], PixelChannels]


def get_read_function(pixel_type: int) -> DecodeFunction | None:
    return _decode_functions.get(pixel_type, None)


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


def _read_rgba8(reader: Reader) -> PixelChannels:
    return tuple(reader.read(4))


def _read_rgba4(reader: Reader) -> PixelChannels:
    p = reader.read_ushort()
    return (
        (p >> 12 & 15) << 4,
        (p >> 8 & 15) << 4,
        (p >> 4 & 15) << 4,
        (p >> 0 & 15) << 4,
    )


def _read_rgb5a1(reader: Reader) -> PixelChannels:
    p = reader.read_ushort()
    return (
        (p >> 11 & 31) << 3,
        (p >> 6 & 31) << 3,
        (p >> 1 & 31) << 3,
        (p & 255) << 7,
    )


def _read_rgb565(reader: Reader) -> PixelChannels:
    p = reader.read_ushort()
    return (p >> 11 & 31) << 3, (p >> 5 & 63) << 2, (p & 31) << 3


def _read_luminance8_alpha8(reader: Reader) -> PixelChannels:
    return tuple(reader.read(2))[::-1]


def _read_luminance8(reader: Reader) -> PixelChannels:
    return tuple(reader.read(1))


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


def _write_luminance8_alpha8(pixel: PixelChannels) -> bytes:
    return struct.pack("2B", *pixel[::-1])


def _write_luminance8(pixel: PixelChannels) -> bytes:
    return struct.pack("B", pixel)


_encode_functions: dict[int, EncodeFunction] = {
    0: _write_rgba8,
    1: _write_rgba8,
    2: _write_rgba4,
    3: _write_rgb5a1,
    4: _write_rgb565,
    6: _write_luminance8_alpha8,
    10: _write_luminance8,
}

_decode_functions: dict[int, DecodeFunction] = {
    0: _read_rgba8,
    1: _read_rgba8,
    2: _read_rgba4,
    3: _read_rgb5a1,
    4: _read_rgb565,
    6: _read_luminance8_alpha8,
    10: _read_luminance8,
}
