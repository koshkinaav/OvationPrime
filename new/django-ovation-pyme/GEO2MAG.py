import math
# from pylab import *  # Подключение пакетов "matplotlib" (matlab-подобный набор команд для построения графиков) и "numpy"
import numpy as np

from igrfcoord import convert


# GEO->MAG (2015-2020)

# latGEO = 1 * (math.pi / 180)  #
# longGEO = 1 * (math.pi / 180)  # координаты в географической системе (GEO), переведенные в радианы
# altGEO = 0.18


def geo_2_mag__initial(latGEO: float, longGEO: float, altGEO: float) -> [float, float]:
    h11 = 4797.1  #
    g11 = -1501  # Сферические гармонические коэффициенты для эпохи 2015-2020
    g10 = -29442  #

    a = 6378.245  # Большая и малая полуось земного ээлипсоида
    b = 6356.863019  # по Красовскому

    #

    rE = math.sqrt(math.pow(altGEO, 2) + 2 * altGEO * math.sqrt(
        math.pow(a, 2) * math.pow(math.cos(latGEO), 2) + math.pow(b, 2) * math.pow(math.sin(latGEO), 2)) + (
                           math.pow(a, 4) * math.pow(math.cos(latGEO), 2) + math.pow(b, 4) * math.pow(
                       math.sin(latGEO), 2)) / (
                           math.pow(a, 2) * math.pow(math.cos(latGEO), 2) + math.pow(b, 2) * math.pow(
                       math.sin(latGEO), 2)))
    # print("***")
    # print(rE)

    # расчет углов поворота
    lamda = math.atan(h11 / g11)  # угол поворотота вокруг оси Y
    fi = ((math.pi / 2) - math.asin((g11 * math.cos(lamda) + h11 * math.sin(lamda)) / (g10))) - math.pi / 2
    # print("***")
    # print(lamda)
    # print(fi)

    # перевод в геоцентрическую систему

    xGEO = rE * math.cos(latGEO) * math.cos(longGEO)
    yGEO = rE * math.cos(latGEO) * math.sin(longGEO)
    zGEO = rE * math.sin(latGEO)

    # матрица координат GEO
    GEO = list(range(3))
    GEO[0] = xGEO
    GEO[1] = yGEO
    GEO[2] = zGEO
    # print("***")
    # print(GEO)

    # Поворотные матрицы 3x3
    t5Y = list(range(3))
    for i in range(3):
        t5Y[i] = list(range(3))

    t5Y[0][0] = math.cos(fi)
    t5Y[0][1] = 0
    t5Y[0][2] = math.sin(fi)
    t5Y[1][0] = 0
    t5Y[1][1] = 1
    t5Y[1][2] = 0
    t5Y[2][0] = -math.sin(fi)
    t5Y[2][1] = 0
    t5Y[2][2] = math.cos(fi)
    # print("***")
    # print(t5Y)

    t5Z = list(range(3))
    for i in range(3):
        t5Z[i] = list(range(3))

    t5Z[0][0] = math.cos(lamda)
    t5Z[0][1] = math.sin(lamda)
    t5Z[0][2] = 0
    t5Z[1][0] = -math.sin(lamda)
    t5Z[1][1] = math.cos(lamda)
    t5Z[1][2] = 0
    t5Z[2][0] = 0
    t5Z[2][1] = 0
    t5Z[2][2] = 1
    # print("***")
    # print(t5Z)

    # Умножение матриц: t5 = t5Y*t5Z
    t5 = list(range(3))
    for i in range(3):
        t5[i] = list(range(3))
    t5[0][0] = (t5Y[0][0] * t5Z[0][0]) + (t5Y[0][1] * t5Z[1][0]) + (t5Y[0][2] * t5Z[2][0])
    t5[0][1] = (t5Y[0][0] * t5Z[0][1]) + (t5Y[0][1] * t5Z[1][1]) + (t5Y[0][2] * t5Z[2][1])
    t5[0][2] = (t5Y[0][0] * t5Z[0][2]) + (t5Y[0][1] * t5Z[1][2]) + (t5Y[0][2] * t5Z[2][2])

    t5[1][0] = (t5Y[1][0] * t5Z[0][0]) + (t5Y[1][1] * t5Z[1][0]) + (t5Y[1][2] * t5Z[2][0])
    t5[1][1] = (t5Y[1][0] * t5Z[0][1]) + (t5Y[1][1] * t5Z[1][1]) + (t5Y[1][2] * t5Z[2][1])
    t5[1][2] = (t5Y[1][0] * t5Z[0][2]) + (t5Y[1][1] * t5Z[1][2]) + (t5Y[1][2] * t5Z[2][2])

    t5[2][0] = (t5Y[2][0] * t5Z[0][0]) + (t5Y[2][1] * t5Z[1][0]) + (t5Y[2][2] * t5Z[2][0])
    t5[2][1] = (t5Y[2][0] * t5Z[0][1]) + (t5Y[2][1] * t5Z[1][1]) + (t5Y[2][2] * t5Z[2][1])
    t5[2][2] = (t5Y[2][0] * t5Z[0][2]) + (t5Y[2][1] * t5Z[1][2]) + (t5Y[2][2] * t5Z[2][2])
    # print("***")
    # print(t5)

    # Умножение матриц: MAG = t5*tGEO
    MAG = list(range(3))
    MAG[0] = (t5[0][0] * GEO[0]) + (t5[0][1] * GEO[1]) + (t5[0][2] * GEO[2])
    MAG[1] = (t5[1][0] * GEO[0]) + (t5[1][1] * GEO[1]) + (t5[1][2] * GEO[2])
    MAG[2] = (t5[2][0] * GEO[0]) + (t5[2][1] * GEO[1]) + (t5[2][2] * GEO[2])
    # print("***")
    # print(MAG)

    # пересчет в  град
    latMAG = math.atan((MAG[2]) / (math.sqrt(pow(MAG[0], 2) + pow(MAG[1], 2)))) * (180 / math.pi)
    if MAG[1] > 0:
        longMAG = math.acos((MAG[0]) / (math.sqrt(pow(MAG[0], 2) + pow(MAG[1], 2)))) * (180 / math.pi)
    else:
        longMAG = 360 - (math.acos((MAG[0]) / (math.sqrt(pow(MAG[0], 2) + pow(MAG[1], 2)))) * (180 / math.pi))
    # print("***")
    # print(latMAG)
    # print(longMAG)

    return latMAG, longMAG


def geo_2_mag_fixed(latGEO_radians: float, longGEO_radians: float, altGEO: float) -> [float, float]:
    """
    :param: latGEO_radians Географическая ... радианы
    :param longGEO_radians: радианы

    :return : latMAG_degrees, longMAG_degrees, tan, cos, MAG, GEO
    """
    h11 = 4797.1  #
    g11 = -1501  # Сферические гармонические коэффициенты для эпохи 2015-2020
    g10 = -29442  #

    rE = 1

    # расчет углов поворота
    lambda_radians = math.atan(h11 / g11)  # угол поворота вокруг оси Y
    fi_radians = - math.asin((g11 * math.cos(lambda_radians) + h11 * math.sin(lambda_radians)) / (g10))
    # print("***")
    # print(lamda)
    # print(fi)

    # перевод в геоцентрическую систему

    xGEO = rE * math.cos(latGEO_radians) * math.cos(longGEO_radians)
    yGEO = rE * math.cos(latGEO_radians) * math.sin(longGEO_radians)
    zGEO = rE * math.sin(latGEO_radians)

    # print(f'{rE=}')
    # print(f'{math.sin(latGEO)=}')

    GEO = [xGEO, yGEO, zGEO]

    geo_len = GEO[0] * GEO[0] + GEO[1] * GEO[1] + GEO[2] * GEO[2]

    assert abs(geo_len - rE * rE) < 1e-6, f'GEO!=rE, {GEO=}, {geo_len=}, {rE*rE=}'

    t5Y = [
        [math.cos(fi_radians), 0, math.sin(fi_radians)],
        [0, 1, 0],
        [-math.sin(fi_radians), 0, math.cos(fi_radians)]
    ]

    t5Z = [
        [math.cos(lambda_radians), math.sin(lambda_radians), 0],
        [-math.sin(lambda_radians), math.cos(lambda_radians), 0],
        [0, 0, 1]
    ]

    t5 = np.dot(t5Y, t5Z)

    MAG = np.dot(t5, GEO)

    # MAG[0] /= 2
    # MAG[1] /= 2
    # MAG[2] /= 2
    mag_len = math.sqrt(MAG[0] * MAG[0] + MAG[1] * MAG[1] + MAG[2] * MAG[2])
    assert abs(mag_len - 1) < 1e-6
    # print(f'{mag_len=}')
    tan = (MAG[2]) / (math.sqrt(pow(MAG[0], 2) + pow(MAG[1], 2)))
    cos = (MAG[0]) / (math.sqrt(pow(MAG[0], 2) + pow(MAG[1], 2)))

    DEBUG= True
    if DEBUG:

        # print(f'{cos=}, {tan=}')
        # print(f'geo_2_mag {MAG=}')

        cos = np.longdouble(cos)
        tan = np.longdouble(tan)

        cos2 = cos * cos
        tan2 = tan * tan
        _MAG = [0, 0, 0]

        _MAG[0] = cos2 * (1 - tan2 / (1 + tan2))
        _MAG[1] = _MAG[0] * (1 / cos2 - 1)
        _MAG[2] = tan2 / (1 + tan2)

        _MAG[0] = math.sqrt(_MAG[0])
        _MAG[1] = math.sqrt(_MAG[1])
        _MAG[2] = math.sqrt(_MAG[2])

        if MAG[1] < 0:
            _MAG[1] *= -1
        if tan < 0:
            _MAG[2] *= -1
        if cos < 0:
            _MAG[0] *= -1

        for i in range(3):
            assert abs(MAG[i] - _MAG[i]) < 1e-6

        # print(f'geo_2_mag {_MAG=}')

        t5_inv = np.linalg.inv(t5)

        _GEO1 = np.dot(t5_inv, MAG)
        _GEO2 = np.dot(t5_inv, _MAG)

        for i in range(3):
            assert abs(GEO[i] - _GEO2[i]) < 1e-6

        _x = _GEO2[0] / rE  # math.cos(latGEO) * math.cos(longGEO)
        _y = _GEO2[1] / rE  # math.cos(latGEO) * math.sin(longGEO)
        _z = _GEO2[2] / rE  # math.sin(latGEO)

        assert abs(_x - math.cos(latGEO_radians) * math.cos(longGEO_radians)) < 1e-6
        assert abs(_y - math.cos(latGEO_radians) * math.sin(longGEO_radians)) < 1e-6
        assert abs(_z - math.sin(latGEO_radians)) < 1e-6

        _latGEO1 = math.asin(_z)
        if abs(_latGEO1 - math.pi / 2) < math.radians(0.0625):
            _latGEO1 += math.radians(0.125)
        if abs(_latGEO1 + math.pi / 2) < math.radians(0.0625):
            _latGEO1 += math.radians(0.125)

        if _latGEO1 > 0:
            _latGEO2 = math.pi - _latGEO1
        else:
            _latGEO2 = -math.pi - _latGEO1

        cos_lat1 = math.cos(_latGEO1)
        cos_lat2 = math.cos(_latGEO2)

        if abs(cos_lat1) < 1e-8:
            long_sin1 = 1
            long_sin2 = -1
        else:
            long_sin1 = _y / cos_lat1
            if long_sin1 > 1:
                long_sin1 = 1
            if long_sin1 < -1:
                long_sin1 = -1
            long_sin2 = _y / cos_lat2
            if long_sin2 > 1:
                long_sin2 = 1
            if long_sin2 < -1:
                long_sin2 = -1

        _longGEO1 = math.asin(long_sin1)
        if _longGEO1 > 0:
            _longGEO2 = math.pi - _longGEO1
        else:
            _longGEO2 = -math.pi - _longGEO1

        _longGEO3 = math.asin(long_sin2)
        if _longGEO3 > 0:
            _longGEO4 = math.pi - _longGEO3
        else:
            _longGEO4 = -math.pi - _longGEO3

        # assert any([abs(latGEO-_latGEO)<1e-3 for _latGEO in [_latGEO1, _latGEO2]])
        # assert any([abs(longGEO - _longGEO) < 1e-3 for _longGEO in [_longGEO1, _longGEO2, _longGEO3, _longGEO4]])

        _x1 = math.cos(_latGEO1) * math.cos(_longGEO1)

        _x2 = math.cos(_latGEO1) * math.cos(_longGEO2)

        _x3 = math.cos(_latGEO2) * math.cos(_longGEO3)

        _x4 = math.cos(_latGEO2) * math.cos(_longGEO4)

        eps = 1e-6
        # if abs(_x - _x1) < eps and abs(_x - _x4) < eps:
        #     if abs(_latGEO1-latGEO)<1e-6:
        #         print('x1')
        #     if abs(_latGEO2-latGEO)<1e-6:
        #         print('x4')
        #     print(f'{latGEO=}, {longGEO=}, {_MAG=}, {_x1=}, {_latGEO1=}, {_longGEO1=}, {_latGEO2=}, {_longGEO4=}')
        # elif abs(_x - _x2) < eps and abs(_x - _x3) < eps:
        #     if abs(_latGEO1-latGEO)<1e-6:
        #         print('x2')
        #     if abs(_latGEO2-latGEO)<1e-6:
        #         print('x3')
        #     print(f'{latGEO=}, {longGEO=}, {_MAG=}, {_x2=}, {_latGEO1=}, {_longGEO2=}, {_latGEO2=}, {_longGEO3=}')
        # else:
        #     raise ValueError()

        # assert abs(_latGEO - latGEO) < 1e-6
        # assert abs(_longGEO - longGEO) < 1e-6

        # print(_GEO1)

        # 1) MAG0^2 + MAG1^2 + MAG2^2 = rE^2
        # 2) MAG0^2 + MAG1^2 = MAG2^2 / tan^2
        # 3) MAG0^2 + MAG1^2 = MAG0^2 / cos^2

        # MAG0^2 = MAG1^2/(1/cos^2-1) = MAG1^2*(cos^2)/(1-cos^2) (3)
        # MAG1^2*(cos^2)/(1-cos^2) + MAG1^2 + MAG2^2 = rE^2 (1)
        # MAG1^2 / (1-cos^2) + MAG2^2 = re^2 (1)
        # MAG1^2*(cos^2)/(1-cos^2)  + MAG1^2 = MAG2^2 / tan^2 (2)

        # MAG2^2 / tan^2 + MAG2^2 - re^2
        # MAG2^2 * (1+1/tan^2) = re^2
        # MAG2^2 * ((tan^2+1)(tan^2)) = re^2
        # MAG2^2 = (tan^2)/(1+tan^2)
        # MAG0^2/cos2 = rE^2 - MAG2^2
        # MAG0^2 = cos^2 * (1 - MAG2^2)

        # MAG1^2 = MAG0^2(1/cos^2-1) (3)

        # MAG0^2 + MAG0^2(1/cos^2-1) + MAG2^2 = 1 (1)
        # MAG0^2 * (1/cos^2) + MAG2^2 = 1
        # MAG2^2 = 1 - MAG0^2 * (1/cos^2) (1)

        # MAG0^2 + MAG0^2(1/cos^2-1) = (1/tan^2)*(1-MAG0^2*1/cos^2) (2)
        # MAG0^2 * (1+1/cos^2) = 1/tan^2-MAG0^2*1/tan^2*1/cos^2
        # MAG0^2 * (1+1/cos^2 + 1/(cos^2 * tan^2)) = 1/tan^2
        # MAG0^2 * (cos^2*tan^2+(tan^2 + 1)/(cos^2*tan^2)) = 1/tan^2
        # MAG0^2 = (cos^2 * tan^2) / (tan^2*(tan^2*cos^2 + tan^2+1))

    # пересчет в  град

    latMAG_degrees = math.degrees(math.atan(tan))
    longMAG_degrees = math.degrees(math.acos(cos))
    if MAG[1] <= 0:
        longMAG_degrees = 360 - longMAG_degrees
    # print("***")
    # print(latMAG)
    # print(longMAG)

    return latMAG_degrees, longMAG_degrees, tan, cos, MAG, GEO


def mag_to_geo(latMAG_degrees: float, longMAG_degrees: float, expMAG, expGEO) -> tuple[float, float, float]:
    """
    :param latMAG_degrees: градусы
    :param longMAG_degrees: градусы
    :return: _latGEO1, _longGEO1, 0 - радианы
    """
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

    for i in range(3):
        assert abs(MAG[i]-expMAG[i]) < 1e-6

    h11 = 4797.1  #
    g11 = -1501  # Сферические гармонические коэффициенты для эпохи 2015-2020
    g10 = -29442  #
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

    for i in range(3):
        assert abs(GEO[i]-expGEO[i]) < 1e-6

    rE = math.sqrt(GEO[0] * GEO[0] + GEO[1] * GEO[1] + GEO[2] * GEO[2])

    x = GEO[0] / rE  # math.cos(latGEO) * math.cos(longGEO)
    y = GEO[1] / rE  # math.cos(latGEO) * math.sin(longGEO)
    z = GEO[2] / rE  # math.sin(latGEO)

    back_latGEO_radians = math.asin(z)
    if abs(back_latGEO_radians) > math.pi/2:
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


def main():
    print()
    eps = 1e-5
    year = 2020

    for latGEO_degrees in range(45, 46, 2): #N
        for longGEO_degrees in range(120, 121, 3): #E
            for altGEO_meters in range(0, 5_000, 500):
                altGEO_meters = 0
                # print(f'{latGEO_degrees=}, {longGEO_degrees=}')

                latGEO_radians = math.radians(latGEO_degrees)
                longGEO_radians = math.radians(longGEO_degrees)
                altGEO_km = altGEO_meters / 1000

                mag1 = geo_2_mag__initial(latGEO_radians, longGEO_radians, altGEO_km)
                mag2 = geo_2_mag_fixed(latGEO_radians, longGEO_radians, altGEO_km)

                if abs(mag1[0] - mag2[0]) > eps or abs(mag1[1] - mag2[1]) > eps:
                    print("mag1-mag2", latGEO_radians, longGEO_radians, altGEO_km, mag1, mag2)

                mag_lat_degrees = mag2[0]
                mag_lon_degrees = mag2[1]

                # print(f'{mag_lat_degrees=}, {mag_lon_degrees=}')

                back_latGEO_radians, back_longGEO2_radians, _altGEO2 = mag_to_geo(mag_lat_degrees,mag_lon_degrees, expMAG=mag2[4], expGEO=mag2[5])

                # print(f'{back_latGEO_radians=}, {back_longGEO2_radians=}')
                # print(f'{math.degrees(back_latGEO_radians)=}, {math.degrees(back_longGEO2_radians)=}')

                is_ok = abs(back_latGEO_radians - latGEO_radians) < eps and abs(back_longGEO2_radians - longGEO_radians) < eps
                print(f'{is_ok=}')

                assert abs(back_latGEO_radians - latGEO_radians) < eps, f'{back_latGEO_radians=}, {latGEO_radians=}'
                assert abs(back_longGEO2_radians - longGEO_radians) < eps, f'{back_longGEO2_radians=}, {longGEO_radians=}'

                assert abs(math.degrees(back_latGEO_radians) - latGEO_degrees) < eps
                assert abs(math.degrees(back_longGEO2_radians) - longGEO_degrees) < eps

                # print(f'{_latGEO2=}, {_latGEO=}, {_longGEO2=}, {_longGEO=}, {_altGEO2=}, {_altGEO=}, {_latGEO+_latGEO2}, {_longGEO+_longGEO2}')
                # print()
                # print()
                # print()

if __name__ =='__main__':
    main()
    print("end")
