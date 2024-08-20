from __future__ import annotations

from typing import TYPE_CHECKING

from system.lib.objects.plain_object import PlainObject
from system.lib.objects.shape import Region

if TYPE_CHECKING:
    from system.lib.swf import SupercellSWF


class Shape(PlainObject):
    def __init__(self):
        super().__init__()

        self.id = 0
        self.regions: list[Region] = []

    def load(self, swf: SupercellSWF, tag: int):
        assert swf.reader is not None

        self.id = swf.reader.read_ushort()

        swf.reader.read_ushort()  # regions_count
        if tag == 18:
            swf.reader.read_ushort()  # point_count

        while True:
            region_tag = swf.reader.read_char()
            region_length = swf.reader.read_uint()

            if region_tag == 0:
                return
            elif region_tag in (4, 17, 22):
                region = Region()
                region.load(swf, region_tag)
                self.regions.append(region)
            else:
                swf.reader.read(region_length)
