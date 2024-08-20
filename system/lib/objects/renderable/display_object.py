from __future__ import annotations

from abc import ABC, abstractmethod

from PIL import Image

from system.lib.math.rect import Rect
from system.lib.matrices import ColorTransform, Matrix2x3


class DisplayObject(ABC):
    def __init__(self):
        self._matrix = Matrix2x3()
        self._color_transform = ColorTransform()

    @abstractmethod
    def calculate_bounds(self, matrix: Matrix2x3) -> Rect:
        ...

    @abstractmethod
    def render(self, matrix: Matrix2x3) -> Image.Image:
        ...

    def set_matrix(self, matrix: Matrix2x3):
        self._matrix = matrix

    def set_color_transform(self, color_transform: ColorTransform):
        self._color_transform = color_transform
