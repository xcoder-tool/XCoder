from __future__ import annotations

from dataclasses import dataclass
import os
from pathlib import Path

from bytestream import BinaryReader
from loguru import logger
from sc.math.point import Point
from sc_compression import Signatures

from .localization import locale


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
    sheets: list[SheetInfo]
    shapes: list[ShapeInfo]


def parse_info(metadata_file_path: Path) -> FileInfo:
    logger.info(locale.collecting_inf % metadata_file_path.name)
    print()

    with open(metadata_file_path, "rb") as file:
        reader = BinaryReader(file.read(), "little")

    ensure_magic_known(reader)

    file_info = FileInfo(
        os.path.splitext(metadata_file_path.name)[0], Signatures.NONE, [], []
    )
    parse_base_info(file_info, reader)

    shape_count = reader.read_ushort()
    for _shape_index in range(shape_count):
        shape_id = reader.read_ushort()

        regions: list[RegionInfo] = []

        command_count = reader.read_ushort()
        for _region_index in range(command_count):
            texture_id, point_count = reader.read_uchar(), reader.read_uchar()

            points = [
                Point(reader.read_ushort(), reader.read_ushort())
                for _ in range(point_count)
            ]

            regions.append(RegionInfo(texture_id, points))

        file_info.shapes.append(ShapeInfo(shape_id, regions))

    return file_info


def parse_base_info(file_info: FileInfo, reader: BinaryReader) -> None:
    file_info.signature = Signatures.SC

    sheet_count = reader.read_uchar()
    for _i in range(sheet_count):
        file_type = reader.read_uchar()
        pixel_type = reader.read_uchar()
        width = reader.read_ushort()
        height = reader.read_ushort()

        file_info.sheets.append(SheetInfo(file_type, pixel_type, (width, height)))


def ensure_magic_known(reader: BinaryReader) -> None:
    magic = reader.read(4)
    if magic != b"XCOD":
        raise IOError("Unknown file MAGIC: " + magic.hex())
