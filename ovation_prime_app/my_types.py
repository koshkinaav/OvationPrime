from typing import TypedDict, NamedTuple


class OvationPrimeData(TypedDict):
    value: float
    mlt: float
    mlat: float


class CoordinatesValue(NamedTuple):
    latitude: float
    longitude: float
    value: float