from collections.abc import Sequence
from pathlib import Path

from PIL import Image
from loguru import logger

from xcoder.bytestream import Writer
from xcoder.console import Console
from xcoder.features.files import write_sc
from xcoder.localization import locale
from xcoder.objects import SWFTexture
from xcoder.xcod import FileInfo


def compile_sc(
    output_folder: Path,
    file_info: FileInfo,
    sheets: Sequence[Image.Image],
):
    writer = Writer()

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

        texture_writer = Writer()
        swf_texture.save(writer, tag, True)

        writer.write_tagged(tag, texture_writer.getvalue())

        print()

    writer.write_tagged(0, b"")  # EOF tag

    logger.info(locale.compressing_with % file_info.signature.name.upper())
    write_sc(
        output_folder / f"{file_info.name}.sc",
        writer.getvalue(),
        file_info.signature,
        file_info.signature_version,
    )
    logger.info(locale.compression_done)
    print()
