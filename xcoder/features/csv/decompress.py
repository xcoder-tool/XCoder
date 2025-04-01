import os

from loguru import logger
from sc_compression import decompress

from xcoder.localization import locale


def decompress_csv():
    folder = "./CSV/In-Compressed"
    folder_export = "./CSV/Out-Decompressed"

    for file in os.listdir(folder):
        if file.endswith(".csv"):
            try:
                with open(f"{folder}/{file}", "rb") as f:
                    file_data = f.read()

                with open(f"{folder_export}/{file}", "wb") as f:
                    f.write(decompress(file_data)[0])
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
