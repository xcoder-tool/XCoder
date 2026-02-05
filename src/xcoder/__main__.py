import time

from loguru import logger

from xcoder import clear
from xcoder.config import config
from xcoder.features.initialization import initialize
from xcoder.localization import locale
from xcoder.main_menu import check_auto_update, check_files_updated, menu, refill_menu


def main():
    if not config.initialized:
        config.change_language(locale.change())

    if not config.initialized:
        initialize(True)
        exit()

    check_auto_update()
    check_files_updated()

    refill_menu()

    interrupted = False
    while not interrupted:
        try:
            handler = menu.choice()
            if handler is None:
                continue

            start_time = time.time()
            with logger.catch():
                handler()
            logger.opt(colors=True).info(
                f"<green>{locale.done % (time.time() - start_time)}</green>"
            )
            input(locale.to_continue)
        except KeyboardInterrupt:
            interrupted = True
        finally:
            clear()

    logger.info("Exit.")


if __name__ == "__main__":
    main()
