from math import atan2, degrees
from typing import TypeAlias

from system.lib.math.point import Point
from system.lib.math.rect import Rect

Polygon: TypeAlias = list[Point]


def is_clockwise(polygon: Polygon) -> bool:
    """Returns true if polygon points order is clockwise, otherwise false.

    :param polygon:
    :return:
    """
    points_sum = 0
    for i in range(len(polygon)):
        p1 = polygon[i]
        p2 = polygon[(i + 1) % len(polygon)]

        points_sum += (p2.x - p1.x) * (p1.y + p2.y)
    return points_sum > 0


def compare_polygons(
    polygon1: Polygon,
    polygon2: Polygon,
    round_to_nearest: bool = False,
) -> tuple[int, bool]:
    """Calculates rotation and if polygon is mirrored.

    :param polygon1: shape polygon
    :param polygon2: sheet polygon
    :param round_to_nearest: should round to a multiple of 90
    :return: rotation degrees, is polygon mirrored
    """

    is_uv_clockwise = is_clockwise(polygon2)
    is_xy_clockwise = is_clockwise(polygon1)

    mirroring = not (is_uv_clockwise == is_xy_clockwise)

    dx = polygon1[1].x - polygon1[0].x
    dy = polygon1[1].y - polygon1[0].y
    du = polygon2[1].x - polygon2[0].x
    dv = polygon2[1].y - polygon2[0].y

    angle_xy = degrees(atan2(dy, dx)) % 360
    angle_uv = degrees(atan2(dv, du)) % 360

    angle = angle_xy - angle_uv

    if mirroring:
        angle -= 180

    angle = (angle + 360) % 360

    if round_to_nearest:
        angle = round(angle / 90) * 90

    return int(angle), mirroring


def get_rect(polygon: list[Point]) -> Rect:
    """Calculates polygon bounds and returns rect.

    :param polygon: polygon points
    :return: Rect object
    """

    rect = Rect(left=100000, top=100000, right=-100000, bottom=-100000)

    for point in polygon:
        rect.add_point(point.x, point.y)

    return rect
