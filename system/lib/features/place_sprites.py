import os
from pathlib import Path

from PIL import Image

from system.lib import Console
from system.lib.images import create_filled_polygon_image, get_format_by_pixel_type
from system.lib.math.polygon import get_rect
from system.lib.xcod import FileInfo
from system.localization import locale

MASK_COLOR = 255


def place_sprites(
    file_info: FileInfo, folder: Path, overwrite: bool = False
) -> list[Image.Image]:
    files_to_overwrite = os.listdir(folder / ("overwrite" if overwrite else ""))
    texture_files = os.listdir(folder / "textures")

    sheets = []
    for i in range(len(file_info.sheets)):
        sheet_info = file_info.sheets[i]

        sheets.append(
            Image.open(f"{folder}/textures/{texture_files[i]}")
            if overwrite
            else Image.new(
                get_format_by_pixel_type(sheet_info.pixel_type), sheet_info.size
            )
        )

    shapes_count = len(file_info.shapes)
    for shape_index, shape_info in enumerate(file_info.shapes):
        Console.progress_bar(
            locale.place_sprites_process % (shape_index + 1, shapes_count),
            shape_index,
            shapes_count,
        )

        for region_index, region_info in enumerate(shape_info.regions):
            texture_width = sheets[region_info.texture_id].width
            texture_height = sheets[region_info.texture_id].height

            filename = f"shape_{shape_info.id}_{region_index}.png"
            if filename not in files_to_overwrite:
                continue

            rect = get_rect(region_info.points)

            img_mask = create_filled_polygon_image(
                "L", texture_width, texture_height, region_info.points, MASK_COLOR
            )

            if rect.width == 0 or rect.height == 0:
                if rect.height != 0:
                    for _y in range(int(rect.height)):
                        img_mask.putpixel(
                            (int(rect.right - 1), int(rect.top + _y - 1)), MASK_COLOR
                        )
                    rect.right += 1
                elif rect.width != 0:
                    for _x in range(int(rect.width)):
                        img_mask.putpixel(
                            (int(rect.left + _x - 1), int(rect.bottom - 1)), MASK_COLOR
                        )
                    rect.bottom += 1
                else:
                    img_mask.putpixel(
                        (int(rect.right - 1), int(rect.bottom - 1)), MASK_COLOR
                    )
                    rect.right += 1
                    rect.bottom += 1

            x = int(rect.left)
            y = int(rect.top)
            width = int(rect.width)
            height = int(rect.height)
            bbox = int(rect.left), int(rect.top), int(rect.right), int(rect.bottom)

            region_image = Image.open(
                f'{folder}{"/overwrite" if overwrite else ""}/{filename}'
            ).convert("RGBA")

            sheets[region_info.texture_id].paste(
                Image.new("RGBA", (width, height)), (x, y), img_mask.crop(bbox)
            )
            sheets[region_info.texture_id].paste(region_image, (x, y), region_image)
    print()

    return sheets
