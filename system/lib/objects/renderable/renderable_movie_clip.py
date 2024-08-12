from __future__ import annotations

from typing import TYPE_CHECKING

from PIL import Image

from system.lib.math.rect import Rect
from system.lib.matrices import Matrix2x3, MatrixBank
from system.lib.objects.movie_clip.movie_clip import MovieClip
from system.lib.objects.movie_clip.movie_clip_frame import MovieClipFrame
from system.lib.objects.renderable.display_object import DisplayObject

if TYPE_CHECKING:
    from system.lib.swf import SupercellSWF


class RenderableMovieClip(DisplayObject):
    def __init__(self):
        super().__init__()

        self._id = -1
        self._export_name: str | None = None
        self._fps: int = 30
        self._frame_count: int = 0
        self._frames: list[MovieClipFrame] = []
        self._frame_elements: list[tuple[int, int, int]] = []
        self._blends: list[int] = []
        self._binds: list[int] = []
        self._matrix_bank: MatrixBank | None = None

        self._children: list[DisplayObject] = []
        self._frame_children: list[DisplayObject] = []

    @staticmethod
    def create_from_plain(
        swf: SupercellSWF, movie_clip: MovieClip, children: list[DisplayObject]
    ) -> RenderableMovieClip:
        clip = RenderableMovieClip()

        clip._id = movie_clip.id
        clip._matrix_bank = swf.get_matrix_bank(movie_clip.matrix_bank_index)

        clip._export_name = movie_clip.export_name
        clip._fps = movie_clip.fps
        clip._frame_count = movie_clip.frame_count
        clip._frames = movie_clip.frames
        clip._frame_elements = movie_clip.frame_elements
        clip._blends = movie_clip.blends
        clip._binds = movie_clip.binds
        clip._children = children

        clip.set_frame(0)

        return clip

    def render(self, matrix: Matrix2x3) -> Image.Image:
        matrix_multiplied = Matrix2x3(self._matrix)
        matrix_multiplied.multiply(matrix)

        bounds = self.calculate_bounds(matrix_multiplied)

        image = Image.new("RGBA", (int(bounds.width), int(bounds.height)))

        for child in self._frame_children:
            rendered_region = child.render(matrix_multiplied)
            region_bounds = child.calculate_bounds(matrix_multiplied)

            x = int(region_bounds.left - bounds.left)
            y = int(region_bounds.top - bounds.top)

            image.paste(rendered_region, (x, y), rendered_region)

        return image

    def calculate_bounds(self, matrix: Matrix2x3 | None = None) -> Rect:
        rect = Rect()

        for child in self._frame_children:
            rect.merge_bounds(child.calculate_bounds(matrix))

        return rect

    def set_frame(self, frame_index: int):
        self._frame_children = []

        frame = self._frames[frame_index]
        for child_index, matrix_index, color_transform_index in frame.get_elements():
            matrix = None
            if matrix_index != 0xFFFF:
                matrix = self._matrix_bank.get_matrix(matrix_index)

            color_transform = None
            if color_transform_index != 0xFFFF:
                color_transform = self._matrix_bank.get_color_transform(
                    color_transform_index
                )

            child = self._children[child_index]
            if child is None:
                continue

            child.set_matrix(matrix)
            child.set_color_transform(color_transform)

            self._frame_children.append(child)
