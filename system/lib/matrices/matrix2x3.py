from typing import Self

from system.bytestream import Reader

DEFAULT_MULTIPLIER = 1024
PRECISE_MULTIPLIER = 65535


class Matrix2x3:
    """
    self matrix looks like:
    [a c x]
    [b d y]
    """

    def __init__(self, matrix: Self | None = None):
        self.a: float = 1
        self.b: float = 0
        self.c: float = 0
        self.d: float = 1
        self.x: float = 0
        self.y: float = 0

        if matrix is not None:
            self.a = matrix.a
            self.b = matrix.b
            self.c = matrix.c
            self.d = matrix.d
            self.x = matrix.x
            self.y = matrix.y

    def load(self, reader: Reader, tag: int):
        divider: int
        if tag == 8:
            divider = DEFAULT_MULTIPLIER
        elif tag == 36:
            divider = PRECISE_MULTIPLIER
        else:
            raise ValueError(f"Unsupported matrix tag: {tag}")

        self.a = reader.read_int() / divider
        self.b = reader.read_int() / divider
        self.c = reader.read_int() / divider
        self.d = reader.read_int() / divider
        self.x = reader.read_twip()
        self.y = reader.read_twip()

    def apply_x(self, x: float, y: float):
        return x * self.a + y * self.c + self.x

    def apply_y(self, x: float, y: float):
        return y * self.d + x * self.b + self.y

    def multiply(self, matrix: Self) -> Self:
        a = (self.a * matrix.a) + (self.b * matrix.c)
        b = (self.a * matrix.b) + (self.b * matrix.d)
        c = (self.d * matrix.d) + (self.c * matrix.b)
        d = (self.d * matrix.c) + (self.c * matrix.a)
        x = matrix.apply_x(self.x, self.y)
        y = matrix.apply_y(self.x, self.y)

        self.a = a
        self.b = b
        self.d = c
        self.c = d
        self.x = x
        self.y = y

        return self
