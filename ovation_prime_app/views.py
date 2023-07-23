import pandas as pd
from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
import cProfile
import datetime
# import the logging library
import logging
import pytz
# Get an instance of a logger
import math
import os
import json
import numpy as np
from django.views.decorators.csrf import csrf_exempt
from matplotlib import pyplot as plt

from ovation_prime_app.forms import OvationPrimeConductanceForm, WeightedFluxForm, SeasonalFluxForm
from ovation_prime_app.my_types import CoordinatesValue
from ovation_prime_app.utils.fill_zeros import fill_zeros
from ovation_prime_app.utils.grids_to_dicts import grids_to_dicts
from ovation_prime_app.utils.mag_to_geo import mag_to_geo
from ovation_prime_app.utils.round_coordinates import round_coordinates
from ovation_prime_app.utils.sort_coordinates import sort_coordinates
# from ovation_prime_app.utils.test_plot import plot
from ovation_prime_app.utils.dicts_to_tuples import parse
from ovation_prime_app.utils.geo_to_mag import geo_2_mag_fixed

logger = logging.getLogger(__name__)

from django.http import JsonResponse, HttpResponseBadRequest
from django.conf import settings
# Create your views here.

import aacgmv2
import nasaomnireader
from ovationpyme import ovation_prime


def get_north_mlat_grid():
    return settings.NORTH_MLAT_GRID


def get_north_mlt_grid():
    return settings.NORTH_MLT_GRID


def get_south_mlat_grid():
    return settings.SOUTH_MLAT_GRID


def get_south_mlt_grid():
    return settings.SOUTH_MLT_GRID


def create_mag_grids(dt: datetime.datetime, geo_lons: 'list[float]', geo_lats: 'list[float]'):
    geo_lats_table = np.meshgrid(geo_lats, geo_lons)
    mag_lats, mlts = np.meshgrid(geo_lats, geo_lons)
    n, m = geo_lats_table[0].shape
    for i in range(n):
        for j in range(m):
            geo_lat = geo_lats[j]
            geo_lon = geo_lons[i]

            geo_lat_rads = math.radians(geo_lat)
            geo_lon_rads = math.radians(geo_lon)

            alt = 0

            latMAG_degrees, longMAG_degrees = geo_2_mag_fixed(geo_lat_rads, geo_lon_rads, alt, dt)

            mlt = aacgmv2.convert_mlt(longMAG_degrees, dt, False)[0]

            mag_lats[i][j] = latMAG_degrees
            mlts[i][j] = mlt

            # back_mlt = mlts[i][j]
            # back_mlat = mag_lats[i][j]

            # back_mlon_degrees = aacgmv2.convert_mlt(back_mlt, dt, True)
            # back_lat_geo_rads, back_long_geo_rads, back_h = mag_to_geo(back_mlat, back_mlon_degrees, dt)

            # back_lat_geo_rads = back_lat_geo_rads
            # back_long_geo_rads = back_long_geo_rads

            # assert abs(back_mlon_degrees - longMAG_degrees) < 1e-4 or abs( back_mlon_degrees - longMAG_degrees -
            # 360) < 1e-4 or abs( back_mlon_degrees - longMAG_degrees + 360) < 1e-4, f'{back_mlon_degrees=},
            # {longMAG_degrees=}, {mlt=}, {i=}, {j=}'
            #
            # assert abs( back_lat_geo_rads - geo_lat_rads) < 1e-4, f'{back_lat_geo_rads=}, {geo_lat_rads=},
            # {back_long_geo_rads=}, {geo_lon_rads=} {i=}, {j=}, {longMAG_degrees=}, {back_mlon_degrees=},
            # {mlt=}' assert abs(back_long_geo_rads - geo_lon_rads) < 1e-4 or abs( back_long_geo_rads - geo_lon_rads
            # + 2 * math.pi) < 1e-4 or abs( back_long_geo_rads - geo_lon_rads - 2 * math.pi) < 1e-4, f'{geo_lat=},
            # {geo_lon=}, {back_lat_geo_rads=}, {geo_lat_rads=}, {back_long_geo_rads=}, {geo_lon_rads=}, {i=}, {j=},
            # {longMAG_degrees=}, {latMAG_degrees=},{back_mlon_degrees=}, {mlt=}'

    return mag_lats, mlts


def create_north_grids(dt: datetime.datetime):
    lons = settings.LONGITUDES
    lats = settings.N_LATITUDES

    return create_mag_grids(dt, lons, lats)


def create_south_grids(dt: datetime.datetime):
    lons = settings.LONGITUDES
    lats = settings.S_LATITUDES

    return create_mag_grids(dt, lons, lats)


def check_duplicates(data: 'list[CoordinatesValue]') -> 'list[CoordinatesValue]':
    used_coordinates = set()
    used_180_values = {}
    used_0_values = {}
    result = []

    for coord in data:
        corrds = (coord.longitude, coord.latitude)
        if corrds in used_coordinates:
            logger.warning(f'duplicate {corrds}')
            continue
        used_coordinates.add(corrds)
        if abs(coord.latitude) == 180:
            used_180_values[coord.longitude] = coord.value
            continue
        if abs(coord.latitude) == 0 or abs(coord.latitude) == 360:
            used_0_values[coord.longitude] = coord.value
            continue
        result.append(coord)

    for longitude, value in used_180_values.items():
        result.append(CoordinatesValue(180, longitude, value))
    for longitude, value in used_0_values.items():
        result.append(CoordinatesValue(0, longitude, value))
        # result.append(CoordinatesValue(-180, longitude, value))

    return result


@csrf_exempt
def get_ovation_prime_conductance_interpolated(request):
    """
    Формат ввода: словарь {'dt': 'yyyy-mm-ddTHH:MM:SS', 'type': 'pedgrid' или 'hallgrid'}
    :param request:
    :return: файл из NASA
    """

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            dt = pd.to_datetime(data['dt'])
            _type = data['_type']
        except:
            form = OvationPrimeConductanceForm(request.POST)
            is_valid = form.is_valid()
            if not is_valid:
                return HttpResponseBadRequest(form.errors.as_json())
            dt = form.cleaned_data['dt']
            dt = datetime.datetime(dt.year, dt.month, dt.day)
            _type = form.cleaned_data['_type']
        new_north_mlat_grid, new_north_mlt_grid = create_north_grids(dt)
        new_south_mlat_grid, new_south_mlt_grid = create_south_grids(dt)
        estimator = ovation_prime.ConductanceEstimator(fluxtypes=['diff', 'mono'])
        north_mlatgrid, north_mltgrid, north_pedgrid, north_hallgrid = estimator.get_conductance(dt, hemi='N',
                                                                                                 auroral=True,
                                                                                                 solar=True)
        south_mlatgrid, south_mltgrid, south_pedgrid, south_hallgrid = estimator.get_conductance(dt, hemi='S',
                                                                                                 auroral=True,
                                                                                                 solar=True)
        if _type == 'pedgrid':
            north_interpolator = ovation_prime.LatLocaltimeInterpolator(north_mlatgrid, north_mltgrid, north_pedgrid)
            north_new_values = north_interpolator.interpolate(new_north_mlat_grid, new_north_mlt_grid)

            south_interpolator = ovation_prime.LatLocaltimeInterpolator(south_mlatgrid, south_mltgrid, south_pedgrid)
            south_new_values = south_interpolator.interpolate(new_south_mlat_grid, new_south_mlt_grid)

        else:
            north_interpolator = ovation_prime.LatLocaltimeInterpolator(north_mlatgrid, north_mltgrid, north_hallgrid)
            north_new_values = north_interpolator.interpolate(new_north_mlat_grid, new_north_mlt_grid)

            south_interpolator = ovation_prime.LatLocaltimeInterpolator(south_mlatgrid, south_mltgrid, south_hallgrid)
            south_new_values = south_interpolator.interpolate(new_south_mlat_grid, new_south_mlt_grid)
        from ovation_prime_app.utils.test_plot import plot
        # plot(new_north_mlat_grid, new_north_mlt_grid, north_new_values, 'N', dt, "conductance_interpolated")
        # plot(new_south_mlat_grid, new_south_mlt_grid, south_new_values, 'S', dt, "conductance_interpolated")
        _data = [
            *grids_to_dicts(new_north_mlat_grid, new_north_mlt_grid, north_new_values),
            *grids_to_dicts(new_south_mlat_grid, new_south_mlt_grid, south_new_values),
        ]

        now = datetime.datetime.now()
        now_str = now.strftime('%Y_%m_%d_%H_%M_%S_%f')

        parsed_data = [parse(val, dt) for val in _data]

        parsed_data_rounded = round_coordinates(parsed_data)
        parsed_data_rounded = check_duplicates(parsed_data_rounded)
        parsed_data_sorted = sort_coordinates(parsed_data_rounded)

        result = {
            "Forecast Time": str(dt),
            "Data Format": f"[Longitude, Latitude, {_type}]",
            "coordinates": parsed_data_sorted,
            "type": "MultiPoint",
        }

        return JsonResponse(result, safe=False)

    if request.method == 'GET':
        form = OvationPrimeConductanceForm()
        return render(request, 'ovation_prime_app/OvationPrimeConductanceForm.html', {'form': form})


def get_ovation_prime_conductance(request):
    pass


def get_weighted_flux(request):
    pass


def get_weighted_flux_interpolated(request):
    pass


def get_seasonal_flux(request):
    pass
