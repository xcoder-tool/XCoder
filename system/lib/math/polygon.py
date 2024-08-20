from enum import IntEnum
from math import atan2, degrees
from typing import TypeAlias

from system.lib.math.point import Point
from system.lib.math.rect import Rect
from system.lib.matrices import Matrix2x3

Polygon: TypeAlias = list[Point]


class PointOrder(IntEnum):
    CLOCKWISE = 0
    COUNTER_CLOCKWISE = 1


def get_polygon_sum_of_edges(polygon: Polygon) -> float:
    """
     Mostly like signed area, but two times bigger and more accurate with signs.

    https://stackoverflow.com/questions/1165647/how-to-determine-if-a-list-of-polygon-points-are-in-clockwise-order/1165943#1165943

    :param polygon:
    :return:
    """
    points_sum = 0
    for i in range(len(polygon)):
        p1 = polygon[i]
        p2 = polygon[(i + 1) % len(polygon)]

        points_sum += (p2.x - p1.x) * (p1.y + p2.y)
    return points_sum


def get_polygon_point_order(polygon: Polygon) -> PointOrder | None:
    sum_of_edges = get_polygon_sum_of_edges(polygon)
    if sum_of_edges > 0:
        return PointOrder.CLOCKWISE
    elif sum_of_edges < 0:
        return PointOrder.COUNTER_CLOCKWISE

    return None


def compare_polygons(
    polygon1: Polygon,
    polygon2: Polygon,
) -> tuple[float, bool]:
    """Calculates rotation and if polygon is mirrored.

    :param polygon1: shape polygon
    :param polygon2: sheet polygon
    :return: rotation degrees, is polygon mirrored
    """

    polygon1_order = get_polygon_point_order(polygon1)
    polygon2_order = get_polygon_point_order(polygon2)

    mirroring = polygon1_order != polygon2_order

    dx = (polygon1[1].x - polygon1[0].x) * (-1 if mirroring else 1)
    dy = polygon1[1].y - polygon1[0].y
    du = polygon2[1].x - polygon2[0].x
    dv = polygon2[1].y - polygon2[0].y

    # Solution from https://stackoverflow.com/a/21484228/14915825
    angle_radians = atan2(dy, dx) - atan2(dv, du)
    angle = degrees(angle_radians)

    return angle, mirroring


def get_rect(polygon: list[Point]) -> Rect:
    """Calculates polygon bounds and returns rect.

    :param polygon: polygon points
    :return: Rect object
    """

    rect = Rect(left=100000, top=100000, right=-100000, bottom=-100000)

    for point in polygon:
        rect.add_point(point.x, point.y)

    return rect


def apply_matrix(polygon: Polygon, matrix: Matrix2x3 | None = None) -> Polygon:
    """Applies affine matrix to the given polygon. If matrix is none, returns points.

    :param polygon: polygon points
    :param matrix: Affine matrix
    """

    if matrix is None:
        return polygon

    return [
        Point(
            matrix.apply_x(point.x, point.y),
            matrix.apply_y(point.x, point.y),
        )
        for point in polygon
    ]
