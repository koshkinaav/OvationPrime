import datetime
import math
import numpy as np

from ovation_prime_app.utils.date_to_year import date_to_year
from ovation_prime_app.utils.igrf import get_coeffs_cached


def mag_to_geo(latMAG_degrees: float, longMAG_degrees: float, dt: datetime.datetime) -> 'tuple[float, float, float]':
    mag1_sgn = 1

    if longMAG_degrees < 0:
        longMAG_degrees += 360

    if longMAG_degrees > 180:
        longMAG_degrees = 360 - longMAG_degrees
        mag1_sgn = -1

    MAG = [0, 0, 0]

    cos = math.cos(math.radians(longMAG_degrees))
    tan = math.tan(math.radians(latMAG_degrees))

    cos2 = cos * cos
    tan2 = tan * tan

    MAG[0] = cos2 * (1 - tan2 / (1 + tan2))
    MAG[1] = MAG[0] * (1 / cos2 - 1)
    MAG[2] = tan2 / (1 + tan2)

    MAG[0] = math.sqrt(MAG[0])
    MAG[1] = math.sqrt(MAG[1])
    MAG[2] = math.sqrt(MAG[2])
    if mag1_sgn == -1:
        MAG[1] *= -1
    if tan < 0:
        MAG[2] *= -1
    if cos < 0:
        MAG[0] *= -1

    _h11 = 4797.1  #
    _g11 = -1501  # Сферические гармонические коэффициенты для эпохи 2015-2020
    _g10 = -29442  #

    g, h = get_coeffs_cached(date_to_year(dt))

    h11 = h[1][1]
    g11 = g[1][1]
    g10 = g[1][0]

    # print(g10,_g10)
    # print(g11, _g11)
    # print(h11, _h11)

    lamda = math.atan(h11 / g11)  # угол поворотота вокруг оси Y
    fi = - math.asin((g11 * math.cos(lamda) + h11 * math.sin(lamda)) / (g10))

    t5Y = [
        [math.cos(fi), 0, math.sin(fi)],
        [0, 1, 0],
        [-math.sin(fi), 0, math.cos(fi)]
    ]

    # print(t5Y)

    t5Z = [
        [math.cos(lamda), math.sin(lamda), 0],
        [-math.sin(lamda), math.cos(lamda), 0],
        [0, 0, 1]
    ]

    # print(t5Z)

    t5 = np.dot(t5Y, t5Z)
    t5_inv = np.linalg.inv(t5)
    GEO = np.dot(t5_inv, MAG)

    rE = math.sqrt(GEO[0] * GEO[0] + GEO[1] * GEO[1] + GEO[2] * GEO[2])

    x = GEO[0] / rE  # math.cos(latGEO) * math.cos(longGEO)
    y = GEO[1] / rE  # math.cos(latGEO) * math.sin(longGEO)
    z = GEO[2] / rE  # math.sin(latGEO)

    back_latGEO_radians = math.asin(z)
    if abs(back_latGEO_radians) > math.pi / 2:
        if back_latGEO_radians > 0:
            back_latGEO_radians = math.pi - back_latGEO_radians
        else:
            back_latGEO_radians = -math.pi - back_latGEO_radians

    cos_lat = math.cos(back_latGEO_radians)

    long_sin = y / cos_lat
    if long_sin > 1:
        long_sin = 1
    if long_sin < -1:
        long_sin = -1

    back_longGEO_radians = math.asin(long_sin)
    # if abs(back_longGEO_radians) > math.pi/2:
    if back_longGEO_radians > 0:
        back_longGEO_radians2 = math.pi - back_longGEO_radians
    else:
        back_longGEO_radians2 = -math.pi - back_longGEO_radians

    _x1 = math.cos(back_latGEO_radians) * math.cos(back_longGEO_radians)
    _x2 = math.cos(back_latGEO_radians) * math.cos(back_longGEO_radians2)

    # print(f'{cos=}, {tan=}, {mag1_sgn=}, {latMAG_degrees+longMAG_degrees=}')
    eps = 1e-6

    if abs(x - _x1) < eps:
        return back_latGEO_radians, back_longGEO_radians, 0
    elif abs(x - _x2) < eps:
        return back_latGEO_radians, back_longGEO_radians2, 0
    else:
        raise ValueError()
