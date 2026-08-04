import os

from loguru import logger
from sc_compression import Compressor

from xcoder.localization import locale


def compress_csv():
    from sc_compression.signatures import Signatures

    folder = "./CSV/In-Decompressed"
    folder_export = "./CSV/Out-Compressed"

    for file in os.listdir(folder):
        if file.endswith(".csv"):
            try:
                with open(f"{folder}/{file}", "rb") as f:
                    file_data = f.read()

                with open(f"{folder_export}/{file}", "wb") as f:
                    f.write(Compressor.compress(file_data, Signatures.LZMA, 1))
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
