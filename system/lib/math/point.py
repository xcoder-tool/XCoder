class Point:
    def __init__(self, x: float = 0, y: float = 0):
        self.x: float = x
        self.y: float = y

    def __eq__(self, other):
        if isinstance(other, Point):
            return self.x == other.x and self.y == other.y
        return False

    def __mul__(self, other):
        if isinstance(other, int):
            self.x *= other
            self.y *= other
        if isinstance(other, float):
            self.x *= other
            self.y *= other

        return self

    def __add__(self, other):
        if isinstance(other, Point):
            self.x += other.x
            self.y += other.y
        return self

    def __sub__(self, other):
        return self + -other

    def __neg__(self):
        self.x *= -1
        self.y *= -1
        return self

    def __repr__(self):
        return str(self.as_tuple())

    def as_tuple(self) -> tuple[float, float]:
        return self.x, self.y
