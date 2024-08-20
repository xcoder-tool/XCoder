import os

from loguru import logger
from sc_compression import compress, decompress
from sc_compression.signatures import Signatures

from system.localization import locale


def write_sc(
    output_filename: os.PathLike | str,
    buffer: bytes,
    signature: Signatures,
    version: int | None = None,
):
    with open(output_filename, "wb") as file_out:
        file_out.write(compress(buffer, signature, version))  # type: ignore


def open_sc(input_filename: os.PathLike | str) -> tuple[bytes, Signatures]:
    with open(input_filename, "rb") as f:
        file_data = f.read()

    try:
        if b"START" in file_data:
            file_data = file_data[: file_data.index(b"START")]
        return decompress(file_data)
    except TypeError:
        logger.info(locale.decompression_error)
        exit(1)
