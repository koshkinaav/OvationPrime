import numpy as np


def fill_zeros(coordinates: 'list[dict]') -> 'list[dict]':
    lats = [c['mlat'] for c in coordinates]
    lons = [c['mlt'] for c in coordinates]

    lats = list(sorted(set(lats)))
    lons = list(sorted(set(lons)))

    lat_diff = lats[1] - lats[0]

    begin = lats[len(lats) // 2 - 1] + lat_diff
    end = lats[len(lats) // 2]

    for lat in np.arange(begin, end, lat_diff):
        for lon in lons:
            fix = {
                'mlat': lat,
                'mlt': lon,
                'value': 0,

            }
            coordinates.append(fix)

    return coordinates