from __future__ import annotations

from typing import TYPE_CHECKING

from PIL import Image

from system.bytestream import Reader
from system.lib.matrices import Matrix2x3

if TYPE_CHECKING:
    from system.lib.swf import SupercellSWF


CACHE = {}


class MovieClipFrame:
    def __init__(self):
        self._elements_count: int = 0
        self._label: str | None = None

        self._elements: list[tuple[int, int, int]] = []

    def load(self, reader: Reader) -> None:
        self._elements_count = reader.read_short()
        self._label = reader.read_string()

    def get_elements_count(self) -> int:
        return self._elements_count

    def set_elements(self, elements: list[tuple[int, int, int]]) -> None:
        self._elements = elements

    def get_elements(self) -> list[tuple[int, int, int]]:
        return self._elements

    def get_element(self, index: int) -> tuple[int, int, int]:
        return self._elements[index]


class MovieClip:
    def __init__(self):
        super().__init__()

        self.id = -1
        self.export_name: str | None = None
        self.fps: int = 30
        self.frames_count: int = 0
        self.frames: list[MovieClipFrame] = []
        self.frame_elements: list[tuple[int, int, int]] = []
        self.blends: list[int] = []
        self.binds: list[int] = []
        self.matrix_bank_index: int = 0

    def load(self, swf: SupercellSWF, tag: int):
        self.id = swf.reader.read_ushort()

        self.fps = swf.reader.read_char()
        self.frames_count = swf.reader.read_ushort()

        if tag in (3, 14):
            pass
        else:
            if tag == 49:
                swf.reader.read_char()  # unknown

            transforms_count = swf.reader.read_uint()

            for i in range(transforms_count):
                child_index = swf.reader.read_ushort()
                matrix_index = swf.reader.read_ushort()
                color_transform_index = swf.reader.read_ushort()

                self.frame_elements.append(
                    (child_index, matrix_index, color_transform_index)
                )

        binds_count = swf.reader.read_ushort()

        for i in range(binds_count):
            bind_id = swf.reader.read_ushort()  # bind_id
            self.binds.append(bind_id)

        if tag in (12, 35, 49):
            for i in range(binds_count):
                blend = swf.reader.read_char()  # blend
                self.blends.append(blend)

        for i in range(binds_count):
            swf.reader.read_string()  # bind_name

        elements_used = 0

        while True:
            frame_tag = swf.reader.read_uchar()
            frame_length = swf.reader.read_int()

            if frame_tag == 0:
                break

            if frame_tag == 11:
                frame = MovieClipFrame()
                frame.load(swf.reader)
                frame.set_elements(
                    self.frame_elements[
                        elements_used : elements_used + frame.get_elements_count()
                    ]
                )
                self.frames.append(frame)

                elements_used += frame.get_elements_count()
            elif frame_tag == 41:
                self.matrix_bank_index = swf.reader.read_uchar()
            else:
                swf.reader.read(frame_length)

    def render(self, swf: SupercellSWF, matrix: Matrix2x3 | None = None) -> Image.Image:
        raise Exception("Not implemented yet")
