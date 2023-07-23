from typing import List

# from ovation_prime_app.types import OvationPrimeData


def grids_to_dicts(mlat_grid, mlt_grid, value_grid) -> 'list[OvationPrimeData]':
    (n, m) = mlat_grid.shape

    result = []
    for i in range(n):
        for j in range(m):
            item = {
                'mlat': mlat_grid[i, j],
                'mlt': mlt_grid[i, j],
                'value': value_grid[i, j],
            }
            result.append(item)
    return result