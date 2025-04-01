import time

from xcoder.config import config
from xcoder.localization import locale
from xcoder.main_menu import check_auto_update, check_files_updated, menu, refill_menu

try:
    from loguru import logger
except ImportError:
    raise RuntimeError("Please, install loguru using pip")

from xcoder import clear
from xcoder.features.initialization import initialize


def main():
    if not config.initialized:
        config.change_language(locale.change())

    if not config.initialized:
        initialize(True)
        exit()

    check_auto_update()
    check_files_updated()

    refill_menu()

    while True:
        handler = menu.choice()
        if handler is not None:
            start_time = time.time()
            with logger.catch():
                handler()
            logger.opt(colors=True).info(
                f"<green>{locale.done % (time.time() - start_time)}</green>"
            )
            input(locale.to_continue)
        clear()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Exit.")
