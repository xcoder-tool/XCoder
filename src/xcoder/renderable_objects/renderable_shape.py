from __future__ import annotations

from math import inf
from typing import override

from PIL import Image
from sc.math.rect import Rect
from sc.matrices import Matrix2x3
from sc.shape import Shape

from .display_object import DisplayObject
from .renderable_draw_command import DrawCommand


class RenderableShape(DisplayObject):
    def __init__(self, shape: Shape) -> None:
        super().__init__()

        self._id: int = shape.id
        self._commands: list[DrawCommand] = list(map(DrawCommand, shape.commands))

    @override
    def render(self, matrix: Matrix2x3) -> Image.Image:
        matrix_multiplied = Matrix2x3(self._matrix)
        matrix_multiplied.multiply(matrix)

        bounds = self.calculate_bounds(matrix)

        image = Image.new("RGBA", (int(bounds.width), int(bounds.height)))

        for command in self._commands:
            rendered_region = command.render(matrix_multiplied)
            region_bounds = command.calculate_bounds(matrix_multiplied)

            x = int(region_bounds.left - bounds.left)
            y = int(region_bounds.top - bounds.top)

            image.paste(rendered_region, (x, y), rendered_region)

        return image

    @override
    def calculate_bounds(self, matrix: Matrix2x3) -> Rect:
        matrix_multiplied = Matrix2x3(self._matrix)
        matrix_multiplied.multiply(matrix)

        rect = Rect(left=+inf, top=+inf, right=-inf, bottom=-inf)

        for region in self._commands:
            rect.merge_bounds(region.calculate_bounds(matrix_multiplied))

        rect = Rect(
            left=round(rect.left),
            top=round(rect.top),
            right=round(rect.right),
            bottom=round(rect.bottom),
        )

        return rect
