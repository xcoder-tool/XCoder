import time

from loguru import logger

from xcoder import clear
from xcoder.config import config
from xcoder.console import Console
from xcoder.features.directories import clear_directories
from xcoder.features.initialization import initialize
from xcoder.features.update.check import check_update, get_tags
from xcoder.localization import locale
from xcoder.menu import Menu

menu = Menu()


def check_auto_update():
    if config.auto_update and time.time() - config.last_update > 60 * 60 * 24 * 7:
        check_update()
        config.last_update = int(time.time())
        config.dump()


def check_files_updated():
    if config.has_update:
        logger.opt(colors=True).info(f"<green>{locale.update_done % ''}</green>")
        if Console.question(locale.done_qu):
            latest_tag = get_tags(config.repo_owner, config.repo_name)[0]
            latest_tag_name = latest_tag["name"][1:]

            config.has_update = False
            config.version = latest_tag_name
            config.last_update = int(time.time())
            config.dump()
        else:
            exit()


# noinspection PyUnresolvedReferences
@logger.catch()
def refill_menu():
    menu.categories.clear()

    sc_category = Menu.Category(0, locale.sc_label)
    ktx_category = Menu.Category(1, locale.ktx_label)
    csv_category = Menu.Category(2, locale.csv_label)
    other = Menu.Category(10, locale.other_features_label)

    menu.add_category(sc_category)
    menu.add_category(ktx_category)
    menu.add_category(csv_category)
    menu.add_category(other)

    try:
        import sc_compression

        del sc_compression
    except ImportError:
        logger.warning(locale.install_to_unlock % "sc-compression")
    else:
        from xcoder.features.csv.compress import compress_csv
        from xcoder.features.csv.decompress import decompress_csv

        try:
            import PIL

            del PIL
        except ImportError:
            logger.warning(locale.install_to_unlock % "PILLOW")
        else:
            from xcoder.features.sc.decode import (
                decode_and_render_objects,
                decode_textures_only,
            )
            from xcoder.features.sc.encode import (
                collect_objects_and_encode,
                encode_textures_only,
            )

            sc_category.add(
                Menu.Item(
                    name=locale.decode_sc,
                    description=locale.decode_sc_description,
                    handler=decode_textures_only,
                )
            )
            sc_category.add(
                Menu.Item(
                    name=locale.encode_sc,
                    description=locale.encode_sc_description,
                    handler=encode_textures_only,
                )
            )
            sc_category.add(
                Menu.Item(
                    name=locale.decode_by_parts,
                    description=locale.decode_by_parts_description,
                    handler=decode_and_render_objects,
                )
            )
            sc_category.add(
                Menu.Item(
                    name=locale.encode_by_parts,
                    description=locale.encode_by_parts_description,
                    handler=collect_objects_and_encode,
                )
            )
            sc_category.add(
                Menu.Item(
                    name=locale.overwrite_by_parts,
                    description=locale.overwrite_by_parts_description,
                    handler=lambda: collect_objects_and_encode(True),
                )
            )

            from xcoder.features.ktx import (
                convert_ktx_textures_to_png,
                convert_png_textures_to_ktx,
            )
            from xcoder.pvr_tex_tool import can_use_pvr_tex_tool

            if can_use_pvr_tex_tool():
                ktx_category.add(
                    Menu.Item(
                        name=locale.png_from_ktx_label,
                        description=locale.png_from_ktx_description,
                        handler=convert_ktx_textures_to_png,
                    )
                )
                ktx_category.add(
                    Menu.Item(
                        name=locale.ktx_from_png_label,
                        description=locale.ktx_from_png_description,
                        handler=convert_png_textures_to_ktx,
                    )
                )

        csv_category.add(
            Menu.Item(
                name=locale.decompress_csv,
                description=locale.decompress_csv_description,
                handler=decompress_csv,
            )
        )
        csv_category.add(
            Menu.Item(
                name=locale.compress_csv,
                description=locale.compress_csv_description,
                handler=compress_csv,
            )
        )

    other.add(
        Menu.Item(
            name=locale.check_update,
            description=locale.version % config.version,
            handler=check_update,
        )
    )
    other.add(
        Menu.Item(
            name=locale.reinit,
            description=locale.reinit_description,
            handler=lambda: (initialize(), refill_menu()),
        )
    )
    other.add(
        Menu.Item(
            name=locale.change_language,
            description=locale.change_lang_description % config.language,
            handler=lambda: (config.change_language(locale.change()), refill_menu()),
        )
    )
    other.add(
        Menu.Item(
            name=locale.clear_directories,
            description=locale.clean_dirs_description,
            handler=lambda: (
                clear_directories() if Console.question(locale.clear_qu) else -1
            ),
        )
    )
    other.add(
        Menu.Item(
            name=locale.toggle_update_auto_checking,
            description=locale.enabled if config.auto_update else locale.disabled,
            handler=lambda: (config.toggle_auto_update(), refill_menu()),
        )
    )
    other.add(Menu.Item(name=locale.exit, handler=lambda: (clear(), exit())))
