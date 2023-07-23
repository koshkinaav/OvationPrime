from functools import lru_cache

from pyIGRF.loadCoeffs import get_coeffs

@lru_cache
def get_coeffs_cached(year: float):
    return get_coeffs(year)
