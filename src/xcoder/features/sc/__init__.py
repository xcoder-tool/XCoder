from collections.abc import Sequence
from pathlib import Path

from PIL import Image
from bytestream import BinaryWriter
from loguru import logger
from sc.texture import SWFTexture

from xcoder.console import Console
from xcoder.features.files import write_sc
from xcoder.localization import locale
from xcoder.xcod import FileInfo


def compile_sc(
    output_folder: Path,
    file_info: FileInfo,
    sheets: Sequence[Image.Image],
) -> None:
    writer = BinaryWriter("little")

    for i, image in enumerate(sheets):
        sheet_info = file_info.sheets[i]

        tag = sheet_info.file_type
        pixel_type = sheet_info.pixel_type

        if image.size != sheet_info.size:
            logger.info(
                locale.illegal_size
                % (sheet_info.width, sheet_info.height, image.width, image.height)
            )

            if Console.question(locale.resize_qu):
                logger.info(locale.resizing)
                image = image.resize(sheet_info.size, Image.Resampling.LANCZOS)

        width, height = image.size

        logger.info(
            locale.about_sc.format(
                filename=file_info.name,
                index=i,
                pixel_type=pixel_type,
                width=width,
                height=height,
            )
        )

        swf_texture = SWFTexture(width=width, height=height, pixel_type=pixel_type)
        swf_texture.image = image

        texture_writer = BinaryWriter("little")
        swf_texture.save(writer, tag, True)

        write_tagged(writer, tag, texture_writer.buffer)

        print()

    write_tagged(writer, 0, b"")  # EOF tag

    logger.info(locale.compressing_with % file_info.signature.name.upper())
    write_sc(
        output_folder / f"{file_info.name}.sc",
        writer.buffer,
        file_info.signature,
        1,
    )
    logger.info(locale.compression_done)
    print()


def write_tagged(writer: BinaryWriter, tag: int, data: bytes) -> None:
    writer.write_uchar(tag)
    writer.write_uint(len(data))
    writer.write(data)
