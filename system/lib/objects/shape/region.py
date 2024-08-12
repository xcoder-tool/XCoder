from __future__ import annotations

from typing import TYPE_CHECKING

from PIL import Image

from system.lib.images import create_filled_polygon_image
from system.lib.math.point import Point
from system.lib.math.polygon import compare_polygons, get_rect
from system.lib.math.rect import Rect
from system.lib.matrices import Matrix2x3

if TYPE_CHECKING:
    from system.lib.objects import SWFTexture
    from system.lib.swf import SupercellSWF


class Region:
    def __init__(self):
        self.texture_index = 0
        self.rotation = 0
        self.is_mirrored = False

        self._point_count = 0
        self._xy_points: list[Point] = []
        self._uv_points: list[Point] = []
        self._transformed_points: list[Point] = []

        self.texture: SWFTexture | None = None

    def load(self, swf: SupercellSWF, tag: int):
        self.texture_index = swf.reader.read_uchar()

        self.texture = swf.textures[self.texture_index]

        self._point_count = 4
        if tag != 4:
            self._point_count = swf.reader.read_uchar()

        self._xy_points: list[Point] = [Point() for _ in range(self._point_count)]
        self._uv_points: list[Point] = [Point() for _ in range(self._point_count)]

        for i in range(self._point_count):
            x = swf.reader.read_int() / 20
            y = swf.reader.read_int() / 20

            self._xy_points[i] = Point(x, y)

        for i in range(self._point_count):
            u = swf.reader.read_ushort() * self.texture.width / 0xFFFF
            v = swf.reader.read_ushort() * self.texture.height / 0xFFFF

            self._uv_points[i] = Point(u, v)

    def render(
        self, matrix: Matrix2x3 | None = None, use_original_size: bool = False
    ) -> Image.Image:
        transformed_points = self.apply_matrix(matrix)

        rect = get_rect(transformed_points)
        width, height = max(int(rect.width), 1), max(int(rect.height), 1)

        self.rotation, self.is_mirrored = compare_polygons(
            transformed_points, self._uv_points, True
        )

        rendered_region = self.get_image()
        if rendered_region.width + rendered_region.height <= 2:
            fill_color: int = rendered_region.getpixel((0, 0))  # type: ignore

            return create_filled_polygon_image(
                rendered_region.mode, width, height, transformed_points, fill_color
            )

        rendered_region = rendered_region.rotate(-self.rotation, expand=True)
        if self.is_mirrored:
            rendered_region = rendered_region.transpose(Image.Transpose.FLIP_LEFT_RIGHT)

        if use_original_size:
            return rendered_region

        return rendered_region.resize((width, height), Image.Resampling.LANCZOS)

    def get_image(self) -> Image.Image:
        rect = get_rect(self._uv_points)

        width = max(int(rect.width), 1)
        height = max(int(rect.height), 1)
        if width + height <= 2:  # The same speed as without this return
            return Image.new(
                "RGBA",
                (1, 1),
                color=self.texture.image.getpixel((int(rect.left), int(rect.top))),
            )

        mask_image = create_filled_polygon_image(
            "L", self.texture.width, self.texture.height, self._uv_points, 0xFF
        )

        rendered_region = Image.new("RGBA", (width, height))
        rendered_region.paste(
            self.texture.image.crop(rect.as_tuple()),
            (0, 0),
            mask_image.crop(rect.as_tuple()),
        )

        return rendered_region

    def get_point_count(self):
        return self._point_count

    def get_uv(self, index: int):
        return self._uv_points[index]

    def get_u(self, index: int):
        return self._uv_points[index].x

    def get_v(self, index: int):
        return self._uv_points[index].y

    def get_xy(self, index: int):
        return self._xy_points[index]

    def get_x(self, index: int):
        return self._xy_points[index].x

    def get_y(self, index: int):
        return self._xy_points[index].y

    def apply_matrix(self, matrix: Matrix2x3 | None = None) -> list[Point]:
        """Applies affine matrix to shape (xy) points.
        If matrix is none, copies the points.

        :param matrix: Affine matrix
        """

        if matrix is None:
            return self._xy_points

        return [
            Point(
                matrix.apply_x(point.x, point.y),
                matrix.apply_y(point.x, point.y),
            )
            for point in self._xy_points
        ]

    def calculate_bounds(self, matrix: Matrix2x3 | None = None) -> Rect:
        return get_rect(self.apply_matrix(matrix))
