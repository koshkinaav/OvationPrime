from functools import cmp_to_key

from ovation_prime_app.my_types import CoordinatesValue


def sort_coordinates(coords: 'list[CoordinatesValue]') -> 'list[CoordinatesValue]':
    def comparator(a: CoordinatesValue, b: CoordinatesValue) -> int:
        for i in range(2):
            if a[i] > b[i]:
                return 1
            if a[i] < b[i]:
                return -1
        return 0

    return list(sorted(coords, key=cmp_to_key(comparator)))
