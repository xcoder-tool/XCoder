import math
from typing import TYPE_CHECKING

from PIL import Image, ImageDraw

if TYPE_CHECKING:
    from PIL._imaging import PixelAccess  # type: ignore[reportPrivateImportUsage]

from .bytestream import Reader, Writer
from .console import Console
from .localization import locale
from .math.point import Point
from .matrices import Matrix2x3
from .pixel_utils import get_pixel_encode_function, get_raw_mode

CHUNK_SIZE = 32


def load_image_from_buffer(
    pixel_type: int, width: int, height: int, pixel_buffer: Reader
) -> Image.Image:
    raw_mode = get_raw_mode(pixel_type)
    bytes_per_pixel = get_byte_count_by_pixel_type(pixel_type)

    return Image.frombuffer(
        get_format_by_pixel_type(pixel_type),
        (width, height),
        pixel_buffer.read(width * height * bytes_per_pixel),
        "raw",
        raw_mode,
        0,
        1,
    )


def join_image(
    pixel_type: int, width: int, height: int, pixel_buffer: Reader
) -> Image.Image:
    mode = get_format_by_pixel_type(pixel_type)
    bytes_per_pixel = get_byte_count_by_pixel_type(pixel_type)
    image = Image.new(mode, (width, height))

    chunk_count_x = math.ceil(width / CHUNK_SIZE)
    chunk_count_y = math.ceil(height / CHUNK_SIZE)
    chunk_count = chunk_count_x * chunk_count_y

    raw_mode = get_raw_mode(pixel_type)

    for chunk_index in range(chunk_count):
        chunk_x = chunk_index % chunk_count_x
        chunk_y = chunk_index // chunk_count_x

        chunk_width = min(width - chunk_x * CHUNK_SIZE, CHUNK_SIZE)
        chunk_height = min(height - chunk_y * CHUNK_SIZE, CHUNK_SIZE)

        sub_image = Image.frombuffer(
            mode,
            (chunk_width, chunk_height),
            pixel_buffer.read(bytes_per_pixel * chunk_width * chunk_height),
            "raw",
            raw_mode,
            0,
            1,
        )

        image.paste(sub_image, (chunk_x * CHUNK_SIZE, chunk_y * CHUNK_SIZE))

        Console.progress_bar(locale.join_pic, chunk_index, chunk_count)

    return image


def _add_pixel(
    image: "PixelAccess", pixel_index: int, width: int, color: tuple
) -> None:
    image[pixel_index % width, int(pixel_index / width)] = color


def split_image(img: Image.Image) -> None:
    width, height = img.size

    loaded_image = img.load()
    if loaded_image is None:
        raise Exception("loaded_image is None")

    loaded_clone = img.copy().load()
    if loaded_clone is None:
        raise Exception("loaded_clone is None")

    x_chunks_count = width // CHUNK_SIZE
    y_chunks_count = height // CHUNK_SIZE

    pixel_index = 0

    for y_chunk in range(y_chunks_count + 1):
        for x_chunk in range(x_chunks_count + 1):
            for y in range(CHUNK_SIZE):
                pixel_y = (y_chunk * CHUNK_SIZE) + y
                if pixel_y >= height:
                    break

                for x in range(CHUNK_SIZE):
                    pixel_x = (x_chunk * CHUNK_SIZE) + x
                    if pixel_x >= width:
                        break

                    _add_pixel(
                        loaded_image, pixel_index, width, loaded_clone[pixel_x, pixel_y]
                    )
                    pixel_index += 1

        Console.progress_bar(locale.split_pic, y_chunk, y_chunks_count + 1)


def get_byte_count_by_pixel_type(pixel_type: int) -> int:
    if pixel_type in (0, 1):
        return 4
    elif pixel_type in (2, 3, 4, 6):
        return 2
    elif pixel_type == 10:
        return 1
    raise Exception(locale.unknown_pixel_type % pixel_type)


def get_format_by_pixel_type(pixel_type: int) -> str:
    if pixel_type in (0, 1, 2, 3):
        return "RGBA"
    elif pixel_type == 4:
        return "RGB"
    elif pixel_type == 6:
        return "LA"
    elif pixel_type == 10:
        return "L"

    raise Exception(locale.unknown_pixel_type % pixel_type)


def save_texture(writer: Writer, image: Image.Image, pixel_type: int) -> None:
    raw_mode = get_raw_mode(pixel_type)
    encode_pixel = get_pixel_encode_function(pixel_type)

    width, height = image.size

    pixels = image.getdata()

    # Some packers for raw_encoder are absent
    # https://github.com/python-pillow/Pillow/blob/58e48745cc7b6c6f7dd26a50fe68d1a82ea51562/src/encode.c#L337
    # https://github.com/python-pillow/Pillow/blob/main/src/libImaging/Pack.c#L668
    if raw_mode != image.mode:
        for y in range(height):
            for x in range(width):
                # noinspection PyTypeChecker
                writer.write(encode_pixel(pixels[y * width + x]))

            Console.progress_bar(locale.writing_pic, y, height)

        return

    writer.write(image.tobytes("raw", raw_mode, 0, 1))
    Console.progress_bar(locale.writing_pic, height - 1, height)


def transform_image(
    image: Image.Image, scale_x: float, scale_y: float, angle: float, x: float, y: float
) -> Image.Image:
    im_orig = image
    image = Image.new("RGBA", im_orig.size, (255, 255, 255, 255))
    image.paste(im_orig)

    w, h = image.size
    angle = -angle

    cos_theta = math.cos(angle)
    sin_theta = math.sin(angle)

    scaled_w, scaled_h = w * scale_x, h * scale_y

    scaled_rotated_w = int(
        math.ceil(math.fabs(cos_theta * scaled_w) + math.fabs(sin_theta * scaled_h))
    )
    scaled_rotated_h = int(
        math.ceil(math.fabs(sin_theta * scaled_w) + math.fabs(cos_theta * scaled_h))
    )

    translated_w = int(math.ceil(scaled_rotated_w + math.fabs(x)))
    translated_h = int(math.ceil(scaled_rotated_h + math.fabs(y)))
    if x > 0:
        x = 0
    if y > 0:
        y = 0

    cx = w / 2.0
    cy = h / 2.0
    translate_x = scaled_rotated_w / 2.0 - x
    translate_y = scaled_rotated_h / 2.0 - y

    a = cos_theta / scale_x
    b = sin_theta / scale_x
    c = cx - translate_x * a - translate_y * b
    d = -sin_theta / scale_y
    e = cos_theta / scale_y
    f = cy - translate_x * d - translate_y * e

    return image.transform(
        (translated_w, translated_h),
        Image.Transform.AFFINE,
        (a, b, c, d, e, f),
        resample=Image.Resampling.BILINEAR,
    )


def translate_image(image, x: float, y: float) -> Image.Image:
    w, h = image.size

    translated_w = int(math.ceil(w + math.fabs(x)))
    translated_h = int(math.ceil(h + math.fabs(y)))
    if x > 0:
        x = 0
    if y > 0:
        y = 0

    return image.transform(
        (translated_w, translated_h),
        Image.Transform.AFFINE,
        (1, 0, -x, 0, 1, -y),
        resample=Image.Resampling.BILINEAR,
    )


def transform_image_by_matrix(image: Image.Image, matrix: Matrix2x3):
    new_width = abs(int(matrix.apply_x(image.width, image.height)))
    new_height = abs(int(matrix.apply_y(image.width, image.height)))

    return image.transform(
        (new_width, new_height),
        Image.Transform.AFFINE,
        (matrix.a, matrix.b, matrix.x, matrix.c, matrix.d, matrix.y),
        resample=Image.Resampling.BILINEAR,
    )


def create_filled_polygon_image(
    mode: str, width: int, height: int, polygon: list[Point], color: int
) -> Image.Image:
    mask_image = Image.new(mode, (width, height), 0)
    drawable_image = ImageDraw.Draw(mask_image)
    drawable_image.polygon([point.as_tuple() for point in polygon], fill=color)

    return mask_image
