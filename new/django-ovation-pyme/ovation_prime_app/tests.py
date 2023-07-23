import math

import datetime

from django.test import TestCase

from ovation_prime_app.utils.mag_to_geo import mag_to_geo
from ovation_prime_app.utils.geo_to_mag import geo_2_mag_fixed


# Create your tests here.

class TestCoordinatesConversion(TestCase):
    eps = 1e-4

    def testSimpleConvertation(self):
        geo_lats = range(-88, 88, 2)
        geo_lons = range(-188, 188, 4)

        dates = []

        dt = datetime.datetime(2005, 1, 1)
        dt_end = datetime.datetime(2022, 11, 19)
        while dt <= dt_end:
            dates.append(dt)
            dt += datetime.timedelta(weeks=4 * 8)

        for geo_lat in geo_lats:
            for geo_lon in geo_lons:
                for dt in dates:
                    with self.subTest(geo_lat=geo_lat, geo_lon=geo_lon, dt=dt):
                        self.processSubTestGeoToMag(geo_lat, geo_lon, dt)

    def processSubTestGeoToMag(self, geo_lat: float, geo_lon: float, dt: datetime.datetime):
        geo_alt = 0

        geo_lat_rads = math.radians(geo_lat)
        geo_lon_rads = math.radians(geo_lon)

        mag_lat_degrees, mag_lon_degrees = geo_2_mag_fixed(geo_lat_rads, geo_lon_rads, geo_alt, dt)

        back_geo_lat_radians, back_geo_lon_radians, back_heo_alt = mag_to_geo(mag_lat_degrees, mag_lon_degrees, dt)

        self.assertCoordinatesEqual(back_geo_lat_radians, geo_lat_rads, self.eps)
        self.assertCoordinatesEqual(back_geo_lon_radians, geo_lon_rads, self.eps)

        back_geo_lat_degrees = math.degrees(back_geo_lat_radians)
        back_geo_lon_degrees = math.degrees(back_geo_lon_radians)

        self.assertLessEqual(back_geo_lat_degrees, 90)
        self.assertGreaterEqual(back_geo_lat_degrees, -90)

        self.assertLessEqual(back_geo_lon_degrees, 180)
        self.assertGreaterEqual(back_geo_lon_degrees, -180)

    def assertCoordinatesEqual(self, a, b, eps):
        a = self.normalizeCoord(a)
        b = self.normalizeCoord(b)
        is_equal = abs(a - b) < eps or abs(a - b - 2 * math.pi) < eps or abs(a - b + 2 * math.pi) < eps
        self.assertTrue(is_equal)

    def normalizeCoord(self, a):
        while a < 0:
            a += 2 * math.pi
        while a >= 2 * math.pi:
            a -= 2 * math.pi
        return a
