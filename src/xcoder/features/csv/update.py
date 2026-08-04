import os

from loguru import logger
from sc_compression import Compressor

from xcoder.localization import locale


def update_csv():
    from sc_compression.signatures import Signatures

    input_folder = "./CSV/In-Old"
    export_folder = "./CSV/Out-Updated"

    for file in os.listdir(input_folder):
        if file.endswith(".csv"):
            try:
                with open(f"{input_folder}/{file}", "rb") as f:
                    file_data = f.read()

                with open(f"{export_folder}/{file}", "wb") as f:
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
