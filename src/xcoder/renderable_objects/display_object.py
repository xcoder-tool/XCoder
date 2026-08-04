from __future__ import annotations

from abc import ABC, abstractmethod

from PIL import Image
from sc.math.rect import Rect
from sc.matrices import ColorTransform, Matrix2x3


class DisplayObject(ABC):
    def __init__(self) -> None:
        self._matrix: Matrix2x3 = Matrix2x3()
        self._color_transform: ColorTransform = ColorTransform()
        self._blend_mode: int = 0
        self._is_visible: bool = True

    @abstractmethod
    def calculate_bounds(self, matrix: Matrix2x3) -> Rect: ...

    @abstractmethod
    def render(self, matrix: Matrix2x3) -> Image.Image: ...

    def set_matrix(self, matrix: Matrix2x3) -> None:
        self._matrix = matrix

    def set_color_transform(self, color_transform: ColorTransform) -> None:
        self._color_transform = color_transform

    # TODO: BlendMode enum
    # TODO: implement blend mode rendering
    def set_blend_mode(self, blend_mode: int) -> None:
        self._blend_mode = blend_mode

    def set_visible(self, is_visible: bool) -> None:
        self._is_visible = is_visible
