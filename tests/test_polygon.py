from unittest import TestCase

from system.lib.math.point import Point
from system.lib.math.polygon import PointOrder, Polygon, get_polygon_point_order


def create_polygon_from_tuple(*polygon: tuple[float, float]) -> Polygon:
    return [Point(x, y) for x, y in polygon]


class PolygonTestCase(TestCase):
    def test_clockwise_square(self):
        polygon = create_polygon_from_tuple(
            (0.0, 0.0), (0.0, 1.0), (1.0, 1.0), (1.0, 0.0)
        )

        self.assertEqual(PointOrder.CLOCKWISE, get_polygon_point_order(polygon))

    def test_clockwise_real1(self):
        polygon = create_polygon_from_tuple(
            (4.0, 4.0), (5.0, -2.0), (-1.0, -4.0), (-6.0, 0.0), (-2.0, 5.0), (0.0, 1.0)
        )

        self.assertEqual(PointOrder.CLOCKWISE, get_polygon_point_order(polygon))

    def test_clockwise_real2(self):
        polygon = create_polygon_from_tuple(
            (160.0, -73.0),
            (89.0, -73.0),
            (89.0, -10.0),
            (143.0, 10.0),
            (156.0, 10.0),
            (160.0, -46.0),
        )

        self.assertEqual(PointOrder.CLOCKWISE, get_polygon_point_order(polygon))

    def test_counter_clockwise_real1(self):
        polygon = create_polygon_from_tuple(
            (5.0, 0.0), (6.0, 4.0), (4.0, 5.0), (1.0, 5.0), (1.0, 0.0)
        )

        self.assertEqual(PointOrder.COUNTER_CLOCKWISE, get_polygon_point_order(polygon))

    def test_counter_clockwise_real2(self):
        polygon = create_polygon_from_tuple(
            (0.0, 0.0), (11.0, 0.0), (0.0, 10.0), (10.0, 10.0)
        )

        self.assertEqual(PointOrder.COUNTER_CLOCKWISE, get_polygon_point_order(polygon))

    def test_counter_clockwise_real3(self):
        polygon = create_polygon_from_tuple(
            (20.0, -73.0),
            (91.0, -73.0),
            (91.0, -10.0),
            (37.0, 10.0),
            (24.0, 10.0),
            (20.0, -46.0),
        )

        self.assertEqual(PointOrder.COUNTER_CLOCKWISE, get_polygon_point_order(polygon))
