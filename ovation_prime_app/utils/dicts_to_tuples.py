# 2021.08.26 22:04
# Извлекает значения данных (value, mlat, mlt) из объекта OvationPrimeData. Выполняет преобразование
# магнитных долгот mlt в географические долготы mlon с использованием функции aacgmv2.convert_mlt. Если mlon
# отрицательное, добавляет 360, чтобы получить долготу в диапазоне от 0 до 360 градусов. Вызывает функцию mag_to_geo
# для преобразования магнитных координат (mlat, mlon) и даты (dt) в географические координаты. Выполняет некоторые
# преобразования для получения географической широты и долготы в градусах. Если географическая широта отрицательная,
# добавляет 360, чтобы получить широту в диапазоне от 0 до 360 градусов. Возвращает объект CoordinatesValue с
# полученными географическими координатами (latitude, longitude) и значением данных (value).
import datetime

# Get an instance of a logger
import math

# from ovation_prime_app.types import OvationPrimeData
from ovation_prime_app.my_types import CoordinatesValue, OvationPrimeData
from ovation_prime_app.utils.mag_to_geo import mag_to_geo

import aacgmv2


# import the logging library

def parse(data: 'OvationPrimeData', dt: datetime) -> 'CoordinatesValue':
    value = data['value']
    mlat = data['mlat']
    mlt = data['mlt']
    # latitude = mlat_to_lat(mlat)
    # longitude = mlt_to_lon(mlt)
    mlon = aacgmv2.convert_mlt(mlt, dt, True)
    if mlon < 0:
        mlon += 360
    # mlon2 = (mlt * 24 + 180) % 360

    # print(mlon, mlon2)

    # test = smToLatLon([mlat], [mlon], dt)
    test2 = mag_to_geo(mlat, mlon, dt)

    # print(test, [longitude, latitude])
    # longitude = test[1][0]
    # latitude = test[0][0]

    longitude = math.degrees(test2[0])
    latitude = math.degrees(test2[1])
    if latitude < 0:
        latitude += 360
    return CoordinatesValue(latitude, longitude, value)
