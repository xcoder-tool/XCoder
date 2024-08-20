from system.lib.math.point import Point
from system.lib.math.polygon import PointOrder, Polygon, get_polygon_point_order


def create_polygon_from_tuple(*polygon: tuple[float, float]) -> Polygon:
    return [Point(x, y) for x, y in polygon]


def assert_equals(expected, existing) -> None:
    assert expected == existing, f"Got {existing}, while {expected=}"


def test1():
    polygon = create_polygon_from_tuple(
        (4.0, 4.0), (5.0, -2.0), (-1.0, -4.0), (-6.0, 0.0), (-2.0, 5.0), (0.0, 1.0)
    )

    assert_equals(PointOrder.CLOCKWISE, get_polygon_point_order(polygon))
    polygon = create_polygon_from_tuple((0.0, 0.0), (0.0, 1.0), (1.0, 1.0), (1.0, 0.0))

    assert_equals(PointOrder.CLOCKWISE, get_polygon_point_order(polygon))

    polygon = create_polygon_from_tuple(
        (160.0, -73.0),
        (89.0, -73.0),
        (89.0, -10.0),
        (143.0, 10.0),
        (156.0, 10.0),
        (160.0, -46.0),
    )

    assert_equals(PointOrder.CLOCKWISE, get_polygon_point_order(polygon))

    polygon = create_polygon_from_tuple(
        (5.0, 0.0), (6.0, 4.0), (4.0, 5.0), (1.0, 5.0), (1.0, 0.0)
    )

    assert_equals(PointOrder.COUNTER_CLOCKWISE, get_polygon_point_order(polygon))

    polygon = create_polygon_from_tuple(
        (0.0, 0.0), (11.0, 0.0), (0.0, 10.0), (10.0, 10.0)
    )

    assert_equals(PointOrder.COUNTER_CLOCKWISE, get_polygon_point_order(polygon))

    polygon = create_polygon_from_tuple(
        (20.0, -73.0),
        (91.0, -73.0),
        (91.0, -10.0),
        (37.0, 10.0),
        (24.0, 10.0),
        (20.0, -46.0),
    )

    assert_equals(PointOrder.COUNTER_CLOCKWISE, get_polygon_point_order(polygon))


if __name__ == "__main__":
    test1()
