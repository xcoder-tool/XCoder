import platform

from loguru import logger

from system import clear
from system.lib.config import config
from system.lib.features.directories import create_directories
from system.lib.features.update.check import get_tags
from system.localization import locale


@logger.catch()
def initialize(first_init=False):
    if first_init:
        clear()

    logger.info(locale.detected_os % platform.system())
    logger.info(locale.installing)

    logger.info(locale.crt_workspace)
    create_directories()
    logger.info(locale.verifying)

    config.initialized = True
    config.version = get_tags("vorono4ka", "xcoder")[0]["name"][1:]
    config.dump()

    if first_init:
        input(locale.to_continue)
