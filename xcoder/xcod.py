from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from loguru import logger
from sc_compression import Signatures

from xcoder.bytestream import Reader
from xcoder.localization import locale
from xcoder.math.point import Point


@dataclass
class SheetInfo:
    file_type: int
    pixel_type: int
    size: tuple[int, int]

    @property
    def width(self) -> int:
        return self.size[0]

    @property
    def height(self) -> int:
        return self.size[1]


@dataclass
class RegionInfo:
    texture_id: int
    points: list[Point]


@dataclass
class ShapeInfo:
    id: int
    regions: list[RegionInfo]


@dataclass
class FileInfo:
    name: str
    signature: Signatures
    signature_version: int | None
    sheets: list[SheetInfo]
    shapes: list[ShapeInfo]


def parse_info(metadata_file_path: Path, has_detailed_info: bool) -> FileInfo:
    logger.info(locale.collecting_inf % metadata_file_path.name)
    print()

    with open(metadata_file_path, "rb") as file:
        reader = Reader(file.read(), "big")

    ensure_magic_known(reader)

    file_info = FileInfo(
        os.path.splitext(metadata_file_path.name)[0], Signatures.NONE, None, [], []
    )
    parse_base_info(file_info, reader)

    if has_detailed_info:
        parse_detailed_info(file_info, reader)

    return file_info


def parse_base_info(file_info: FileInfo, reader: Reader) -> None:
    file_info.signature = Signatures.SC
    file_info.signature_version = 1 if reader.read_string() == "LZMA" else 3

    sheets_count = reader.read_uchar()
    for i in range(sheets_count):
        file_type = reader.read_uchar()
        pixel_type = reader.read_uchar()
        width = reader.read_ushort()
        height = reader.read_ushort()

        file_info.sheets.append(SheetInfo(file_type, pixel_type, (width, height)))


def parse_detailed_info(file_info: FileInfo, reader: Reader) -> None:
    shapes_count = reader.read_ushort()
    for shape_index in range(shapes_count):
        shape_id = reader.read_ushort()

        regions = []

        regions_count = reader.read_ushort()
        for region_index in range(regions_count):
            texture_id, points_count = reader.read_uchar(), reader.read_uchar()

            points = [
                Point(reader.read_ushort(), reader.read_ushort())
                for _ in range(points_count)
            ]

            regions.append(RegionInfo(texture_id, points))

        file_info.shapes.append(ShapeInfo(shape_id, regions))


def ensure_magic_known(reader: Reader) -> None:
    magic = reader.read(4)
    if magic != b"XCOD":
        raise IOError("Unknown file MAGIC: " + magic.hex())
