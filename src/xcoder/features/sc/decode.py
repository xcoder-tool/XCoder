from collections.abc import Sequence
import os
from pathlib import Path
import shutil

from bytestream import BinaryWriter
from loguru import logger
from sc import Shape
from sc.swf import SupercellSWF
from sc.texture import SWFTexture

from xcoder.features.cut_sprites import render_objects
from xcoder.localization import locale

IN_COMPRESSED_PATH = Path("./SC/In-Compressed")
OUT_DECOMPRESSED = Path("./SC/Out-Decompressed")
OUT_SPRITES_PATH = Path("./SC/Out-Sprites")


def decode_textures_only() -> None:
    input_folder = IN_COMPRESSED_PATH
    output_folder = OUT_DECOMPRESSED

    files = os.listdir(input_folder)
    for file in files:
        # Note: otherwise both _tex.sc and .sc will be loaded, which is a bug
        if not file.endswith("_tex.sc"):
            continue

        try:
            swf = SupercellSWF()
            texture_loaded = swf.load(f"{input_folder / file}")
            if not texture_loaded:
                logger.error(locale.texture_not_found % file)
                continue

            base_name = get_file_basename(swf)

            objects_output_folder = _create_objects_output_folder(
                output_folder, base_name
            )

            _save_textures(swf, objects_output_folder, base_name)
            _save_meta_file(
                swf.textures,
                swf.shapes,
                objects_output_folder,
                base_name,
            )
        except Exception as exception:
            logger.exception(
                locale.error
                % (
                    exception.__class__.__module__,
                    exception.__class__.__name__,
                    exception,
                )
            )

        print()


def decode_and_render_objects() -> None:
    input_folder = IN_COMPRESSED_PATH
    output_folder = OUT_SPRITES_PATH
    files = os.listdir(input_folder)

    for file in files:
        if file.endswith("_tex.sc") or not file.endswith(".sc"):
            continue

        try:
            swf = SupercellSWF()
            texture_loaded = swf.load(input_folder / file)
            if not texture_loaded:
                logger.error(locale.texture_not_found % file)
                continue

            base_name = get_file_basename(swf)

            objects_output_folder = _create_objects_output_folder(
                output_folder, base_name
            )

            render_objects(swf, objects_output_folder)
            _save_textures(swf, objects_output_folder / "textures", base_name)
            _save_meta_file(
                swf.textures,
                swf.shapes,
                objects_output_folder,
                base_name,
            )
        except Exception as exception:
            logger.exception(
                locale.error
                % (
                    exception.__class__.__module__,
                    exception.__class__.__name__,
                    exception,
                )
            )

        print()


def get_file_basename(swf: SupercellSWF) -> str:
    assert swf.filename is not None
    return os.path.basename(swf.filename).rsplit(".", 1)[0]


def _create_objects_output_folder(output_folder: Path, base_name: str) -> Path:
    objects_output_folder = output_folder / base_name
    if objects_output_folder.exists():
        shutil.rmtree(objects_output_folder)
    objects_output_folder.mkdir(parents=True)
    return objects_output_folder


def _save_textures(swf: SupercellSWF, textures_output: Path, base_name: str) -> None:
    os.makedirs(textures_output, exist_ok=True)
    for texture_index, texture in enumerate(swf.textures):
        assert texture.image is not None
        texture.image.save(textures_output / f"{base_name}_{texture_index}.png")


def _save_meta_file(
    textures: Sequence[SWFTexture],
    shapes: Sequence[Shape],
    objects_output_folder: Path,
    base_name: str,
) -> None:
    writer = BinaryWriter("little")
    writer.write(b"XCOD")

    writer.write_uchar(len(textures))
    for texture in textures:
        writer.write_uchar(27)  # FIXME: hardcoded value
        writer.write_uchar(texture.pixel_type)
        writer.write_ushort(texture.width)
        writer.write_ushort(texture.height)

    writer.write_ushort(len(shapes))
    for shape in shapes:
        command_count = len(shape.commands)
        writer.write_ushort(shape.id)
        writer.write_ushort(command_count)
        for command in shape.commands:
            writer.write_uchar(command.texture_index)
            writer.write_uchar(command.get_point_count())

            for i in range(command.get_point_count()):
                writer.write_ushort(int(command.get_u(i)))
                writer.write_ushort(int(command.get_v(i)))

    with open(objects_output_folder / f"{base_name}.xcod", "wb") as file:
        file.write(writer.buffer)
