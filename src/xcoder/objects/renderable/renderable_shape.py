from __future__ import annotations

from PIL import Image

from xcoder.math.rect import Rect
from xcoder.matrices import Matrix2x3
from xcoder.objects import Shape
from xcoder.objects.renderable.display_object import DisplayObject


class RenderableShape(DisplayObject):
    def __init__(self, shape: Shape):
        super().__init__()

        self._id = shape.id
        self._regions = shape.regions

    def render(self, matrix: Matrix2x3) -> Image.Image:
        matrix_multiplied = Matrix2x3(self._matrix)
        matrix_multiplied.multiply(matrix)

        bounds = self.calculate_bounds(matrix)

        image = Image.new("RGBA", (int(bounds.width), int(bounds.height)))

        for region in self._regions:
            rendered_region = region.render(matrix_multiplied)
            region_bounds = region.calculate_bounds(matrix_multiplied)

            x = int(region_bounds.left - bounds.left)
            y = int(region_bounds.top - bounds.top)

            image.paste(rendered_region, (x, y), rendered_region)

        return image

    def calculate_bounds(self, matrix: Matrix2x3) -> Rect:
        matrix_multiplied = Matrix2x3(self._matrix)
        matrix_multiplied.multiply(matrix)

        rect = Rect()

        for region in self._regions:
            rect.merge_bounds(region.calculate_bounds(matrix_multiplied))

        rect = Rect(
            left=round(rect.left),
            top=round(rect.top),
            right=round(rect.right),
            bottom=round(rect.bottom),
        )

        return rect
