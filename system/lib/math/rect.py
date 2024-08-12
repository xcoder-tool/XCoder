from typing import Self


class Rect:
    def __init__(
        self, *, left: float = 0, top: float = 0, right: float = 0, bottom: float = 0
    ):
        self.left: float = left
        self.top: float = top
        self.right: float = right
        self.bottom: float = bottom

    @property
    def width(self) -> float:
        return self.right - self.left

    @property
    def height(self) -> float:
        return self.bottom - self.top

    def as_tuple(self) -> tuple[float, float, float, float]:
        return self.left, self.top, self.right, self.bottom

    def add_point(self, x: float, y: float):
        if x < self.left:
            self.left = x
        if x > self.right:
            self.right = x
        if y < self.top:
            self.top = y
        if y > self.bottom:
            self.bottom = y

    def merge_bounds(self, other: Self):
        if other.left < self.left:
            self.left = other.left
        if other.right > self.right:
            self.right = other.right
        if other.top < self.top:
            self.top = other.top
        if other.bottom > self.bottom:
            self.bottom = other.bottom

    def __str__(self):
        return f"Rect{self.left, self.top, self.right, self.bottom}"
