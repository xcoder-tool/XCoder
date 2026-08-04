from PIL import Image
from sc import Matrix2x3
from sc.images import create_filled_polygon_image
from sc.math.polygon import apply_matrix, compare_polygons
from sc.math.rect import Rect
from sc.shape import DrawCommand as DrawCommandOriginal


class DrawCommand:
    def __init__(self, original_command: DrawCommandOriginal) -> None:
        self._command: DrawCommandOriginal = original_command

        self.rotation: float
        self.is_mirrored: bool

    def render(self, matrix: Matrix2x3) -> Image.Image:
        transformed_points = apply_matrix(self._command._xy_points, matrix)

        rect = self._command.calculate_bounds(matrix)
        width, height = max(int(rect.width), 1), max(int(rect.height), 1)

        rendered_region = self._command.get_image()
        if rendered_region.width + rendered_region.height <= 2:
            fill_color: int = rendered_region.getpixel((0, 0))  # type: ignore

            return create_filled_polygon_image(
                rendered_region.mode, width, height, transformed_points, fill_color
            )

        self.rotation, self.is_mirrored = compare_polygons(
            transformed_points, self._command._uv_points
        )

        rendered_region = rendered_region.rotate(-self.rotation, expand=True)
        if self.is_mirrored:
            rendered_region = rendered_region.transpose(Image.Transpose.FLIP_LEFT_RIGHT)

        return rendered_region.resize((width, height), Image.Resampling.BILINEAR)

    def calculate_bounds(self, matrix: Matrix2x3 | None = None) -> Rect:
        return self._command.calculate_bounds(matrix)
