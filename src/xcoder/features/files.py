import os
from typing import Literal

from loguru import logger
from sc_compression import Compressor, Decompressor, Signatures

from xcoder.localization import locale


def write_sc(
    output_filename: os.PathLike[str] | str,
    buffer: bytes,
    signature: Signatures,
    version: Literal[1, 2, 3, 4, 5, 6],
):
    with open(output_filename, "wb") as file_out:
        file_out.write(Compressor.compress(buffer, signature, version))


def open_sc(input_filename: os.PathLike[str] | str) -> bytes:
    with open(input_filename, "rb") as f:
        file_data = f.read()

    try:
        if b"START" in file_data:
            file_data = file_data[: file_data.index(b"START")]

        return Decompressor.decompress(file_data)
    except TypeError:
        logger.info(locale.decompression_error)
        exit(1)
