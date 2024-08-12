from system.lib.matrices.color_transform import ColorTransform
from system.lib.matrices.matrix2x3 import Matrix2x3


class MatrixBank:
    def __init__(self):
        self._matrices: list[Matrix2x3] = []
        self._color_transforms: list[ColorTransform] = []

    def init(self, matrix_count: int, color_transform_count: int):
        self._matrices = []
        for i in range(matrix_count):
            self._matrices.append(Matrix2x3())

        self._color_transforms = []
        for i in range(color_transform_count):
            self._color_transforms.append(ColorTransform())

    def get_matrix(self, index: int) -> Matrix2x3:
        return self._matrices[index]

    def get_color_transform(self, index: int) -> ColorTransform:
        return self._color_transforms[index]
