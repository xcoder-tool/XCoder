import os
import time

from loguru import logger

from xcoder.config import config
from xcoder.localization import locale


def download_update(zip_url: str) -> None:
    if not os.path.exists("updates"):
        os.mkdir("updates")

    try:
        import urllib.request

        with open("updates/update.zip", "wb") as f:
            f.write(urllib.request.urlopen(zip_url).read())

        import zipfile

        with zipfile.ZipFile("updates/update.zip") as zf:
            zf.extractall("updates/")
            zf.close()

            folder_name = f' "{zf.namelist()[0]}"'
            logger.opt(colors=True).info(
                f"<green>{locale.update_done % folder_name}</green>"
            )
            config.has_update = True
            config.last_update = int(time.time())
            config.dump()
            input(locale.to_continue)
            exit()
    except ImportError as exception:
        logger.exception(exception)
