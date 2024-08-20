import os
import shutil
from pathlib import Path

from loguru import logger
from sc_compression import Signatures

from system.bytestream import Writer
from system.lib.features.cut_sprites import render_objects
from system.lib.swf import SupercellSWF
from system.localization import locale

IN_COMPRESSED_PATH = Path("./SC/In-Compressed")
OUT_DECOMPRESSED = Path("./SC/Out-Decompressed")
OUT_SPRITES_PATH = Path("./SC/Out-Sprites")


def decode_textures_only():
    input_folder = IN_COMPRESSED_PATH
    output_folder = OUT_DECOMPRESSED

    files = os.listdir(input_folder)
    for file in files:
        if not file.endswith("_tex.sc"):
            continue

        swf = SupercellSWF()
        base_name = os.path.basename(file).rsplit(".", 1)[0]
        try:
            texture_loaded, signature = swf.load(f"{input_folder / file}")
            if not texture_loaded:
                logger.error(locale.not_found % f"{base_name}_tex.sc")
                continue

            base_name = get_file_basename(swf)

            objects_output_folder = _create_objects_output_folder(
                output_folder, base_name
            )

            _save_meta_file(
                swf, objects_output_folder, base_name.rsplit("_", 1)[0], signature
            )
            _save_textures(swf, objects_output_folder, base_name)
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


def decode_and_render_objects():
    input_folder = IN_COMPRESSED_PATH
    output_folder = OUT_SPRITES_PATH
    files = os.listdir(input_folder)

    for file in files:
        if file.endswith("_tex.sc") or not file.endswith(".sc"):
            continue

        try:
            base_name = os.path.basename(file).rsplit(".", 1)[0]

            swf = SupercellSWF()
            texture_loaded, signature = swf.load(input_folder / file)
            if not texture_loaded:
                logger.error(locale.not_found % f"{base_name}_tex.sc")
                continue

            base_name = get_file_basename(swf)

            objects_output_folder = _create_objects_output_folder(
                output_folder, base_name
            )

            _save_textures(swf, objects_output_folder / "textures", base_name)
            render_objects(swf, objects_output_folder)
            _save_meta_file(swf, objects_output_folder, base_name, signature)
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


def get_file_basename(swf: SupercellSWF):
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
    swf: SupercellSWF,
    objects_output_folder: Path,
    base_name: str,
    signature: Signatures,
) -> None:
    writer = Writer()
    writer.write(b"XCOD")
    writer.write_string(signature.name)
    writer.write_ubyte(len(swf.textures))
    writer.write(swf.xcod_writer.getvalue())

    with open(objects_output_folder / f"{base_name}.xcod", "wb") as file:
        file.write(writer.getvalue())
