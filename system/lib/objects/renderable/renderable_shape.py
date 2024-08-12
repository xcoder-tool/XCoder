from __future__ import annotations

from PIL import Image

from system.lib.math.rect import Rect
from system.lib.matrices import Matrix2x3
from system.lib.objects import Shape
from system.lib.objects.renderable.display_object import DisplayObject


class RenderableShape(DisplayObject):
    def __init__(self, shape: Shape):
        super().__init__()

        self._id = shape.id
        self._regions = shape.regions

    def render(self, matrix: Matrix2x3) -> Image.Image:
        matrix_multiplied = Matrix2x3(self._matrix)
        matrix_multiplied.multiply(matrix)

        bounds = self.calculate_bounds(matrix_multiplied)

        image = Image.new("RGBA", (int(bounds.width), int(bounds.height)))

        for region in self._regions:
            rendered_region = region.render(matrix_multiplied)
            region_bounds = region.calculate_bounds(matrix_multiplied)

            x = int(region_bounds.left - bounds.left)
            y = int(region_bounds.top - bounds.top)

            image.paste(rendered_region, (x, y), rendered_region)

        return image

    def calculate_bounds(self, matrix: Matrix2x3 | None = None) -> Rect:
        rect = Rect()

        for region in self._regions:
            rect.merge_bounds(region.calculate_bounds(matrix))

        return rect