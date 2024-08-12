from system.bytestream import Reader

DEFAULT_MULTIPLIER = 1024
PRECISE_MULTIPLIER = 65535


class Matrix2x3:
    """
    This matrix looks like:
    [a c x]
    [b d y]
    """

    def __init__(self):
        self.a: float = 1
        self.b: float = 0
        self.c: float = 0
        self.d: float = 1
        self.x: float = 0
        self.y: float = 0

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
