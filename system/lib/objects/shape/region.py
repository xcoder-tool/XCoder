from __future__ import annotations

from typing import TYPE_CHECKING

from PIL import Image

from system.lib.images import create_filled_polygon_image
from system.lib.math.point import Point
from system.lib.math.polygon import apply_matrix, compare_polygons, get_rect
from system.lib.math.rect import Rect
from system.lib.matrices import Matrix2x3

if TYPE_CHECKING:
    from system.lib.objects import SWFTexture
    from system.lib.swf import SupercellSWF


class Region:
    def __init__(self):
        self.texture_index: int = 0

        self._texture: SWFTexture | None = None
        self._point_count = 0
        self._xy_points: list[Point] = []
        self._uv_points: list[Point] = []

        self._cache_image: Image.Image | None = None

    def load(self, swf: SupercellSWF, tag: int):
        assert swf.reader is not None

        self.texture_index = swf.reader.read_uchar()

        self._texture = swf.textures[self.texture_index]

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
            if tag == 4:
                u = swf.reader.read_ushort() * 0xFFFF / self._texture.width
                v = swf.reader.read_ushort() * 0xFFFF / self._texture.height
            else:
                u = swf.reader.read_ushort() * self._texture.width / 0xFFFF
                v = swf.reader.read_ushort() * self._texture.height / 0xFFFF

            self._uv_points[i] = Point(u, v) * (0.5 if swf.use_lowres_texture else 1)

    def render(self, matrix: Matrix2x3) -> Image.Image:
        transformed_points = apply_matrix(self._xy_points, matrix)

        rect = get_rect(transformed_points)
        width, height = max(int(rect.width), 1), max(int(rect.height), 1)

        rendered_region = self.get_image()
        if rendered_region.width + rendered_region.height <= 2:
            fill_color: int = rendered_region.getpixel((0, 0))  # type: ignore

            return create_filled_polygon_image(
                rendered_region.mode, width, height, transformed_points, fill_color
            )

        self.rotation, self.is_mirrored = compare_polygons(
            transformed_points, self._uv_points
        )

        rendered_region = rendered_region.rotate(-self.rotation, expand=True)
        if self.is_mirrored:
            rendered_region = rendered_region.transpose(Image.Transpose.FLIP_LEFT_RIGHT)

        return rendered_region.resize((width, height), Image.Resampling.BILINEAR)

    def get_image(self) -> Image.Image:
        # Note: it's 100% safe and very helpful for rendering movie clips
        if self._cache_image is not None:
            return self._cache_image

        assert self._texture is not None and self._texture.image is not None

        rect = get_rect(self._uv_points)

        width = max(int(rect.width), 1)
        height = max(int(rect.height), 1)
        if width + height <= 2:  # The same speed as without this return
            return Image.new(
                "RGBA",
                (1, 1),
                color=self._texture.image.getpixel((int(rect.left), int(rect.top))),
            )

        mask_image = create_filled_polygon_image(
            "L", self._texture.width, self._texture.height, self._uv_points, 0xFF
        )

        rendered_region = Image.new("RGBA", (width, height))
        rendered_region.paste(
            self._texture.image.crop(rect.as_tuple()),
            (0, 0),
            mask_image.crop(rect.as_tuple()),
        )

        self._cache_image = rendered_region

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

    def calculate_bounds(self, matrix: Matrix2x3 | None = None) -> Rect:
        return get_rect(apply_matrix(self._xy_points, matrix))
