from __future__ import annotations

from typing import TYPE_CHECKING

from PIL import Image

from system.lib.math.rect import Rect
from system.lib.matrices import Matrix2x3
from system.lib.objects.shape import Region

if TYPE_CHECKING:
    from system.lib.swf import SupercellSWF


class Shape:
    def __init__(self):
        self.id = 0
        self.regions: list[Region] = []

    def load(self, swf: SupercellSWF, tag: int):
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

    def render(self, matrix: Matrix2x3 | None = None):
        rect = self.calculate_bounds(matrix)

        image = Image.new("RGBA", (int(rect.width), int(rect.height)))

        for region in self.regions:
            rendered_region = region.render(matrix)
            region_bounds = region.calculate_bounds(matrix)

            x = int(region_bounds.left - rect.left)
            y = int(region_bounds.top - rect.top)

            image.paste(rendered_region, (x, y), rendered_region)

        return image

    def calculate_bounds(self, matrix: Matrix2x3 | None = None) -> Rect:
        rect = Rect()

        for region in self.regions:
            rect.merge_bounds(region.calculate_bounds(matrix))

        return rect
