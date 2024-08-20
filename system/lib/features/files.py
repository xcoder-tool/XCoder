import os

from loguru import logger
from sc_compression import compress, decompress
from sc_compression.signatures import Signatures

from system.localization import locale


def write_sc(
    output_filename: str | os.PathLike,
    buffer: bytes,
    signature: Signatures,
    version: int | None = None,
):
    with open(output_filename, "wb") as file_out:
        file_out.write(compress(buffer, signature, version))


def open_sc(input_filename: str) -> tuple[bytes, Signatures]:
    with open(input_filename, "rb") as f:
        file_data = f.read()

    try:
        if b"START" in file_data:
            file_data = file_data[: file_data.index(b"START")]
        return decompress(file_data)
    except TypeError:
        logger.info(locale.decompression_error)
        exit(1)
