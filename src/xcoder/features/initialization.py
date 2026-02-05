import platform

from loguru import logger

from xcoder import clear
from xcoder.config import config
from xcoder.features.directories import create_directories
from xcoder.features.update.check import get_tags
from xcoder.localization import locale


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
    config.version = get_tags(config.repo_owner, config.repo_name)[0]["name"][1:]
    config.dump()

    if first_init:
        input(locale.to_continue)
