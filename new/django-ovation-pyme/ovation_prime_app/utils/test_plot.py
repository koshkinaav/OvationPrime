import matplotlib.pyplot as pp
from geospacepy import satplottools


def plot(new_mlat_grid, new_mlt_grid, vals, hemi, dt, view_name: str):
    f = pp.figure(figsize=(11, 5))
    aH = f.add_subplot(111)
    # aP = f.add_subplot(122)

    X, Y = satplottools.latlt2cart(new_mlat_grid.flatten(), new_mlt_grid.flatten(), hemi)
    X = X.reshape(new_mlat_grid.shape)
    Y = Y.reshape(new_mlt_grid.shape)

    satplottools.draw_dialplot(aH)
    # satplottools.draw_dialplot(aP)

    # mappableH = aH.pcolormesh(X, Y, new_hallgrid, vmin=0., vmax=20.)
    # mappableP = aP.pcolormesh(X, Y, new_pedgrid, vmin=0., vmax=15.)

    mappableH = aH.pcolormesh(X, Y, vals, vmin=0., vmax=20.)

    aH.set_title("Hall Conductance")
    # aP.set_title("Pedersen Conductance")

    f.colorbar(mappableH, ax=aH)
    # f.colorbar(mappableP, ax=aP)

    f.suptitle("{2} {0} Hemisphere at {1}".format(hemi, dt.strftime('%c'), view_name),
               fontweight='bold')
    f.savefig('{2}_{1}_{0}.png'.format(dt.strftime('%Y%m%d_%H%M%S'), hemi, view_name))

    # return f
