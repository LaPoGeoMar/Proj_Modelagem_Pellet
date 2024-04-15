import xarray as xr
import pooch
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
from cartopy.feature import NaturalEarthFeature
from cartopy.mpl.gridliner import LATITUDE_FORMATTER, LONGITUDE_FORMATTER

url = "https://github.com/LaPoGeoMar/Proj_Modelagem_Pellet/releases/download"
version = "v0.1.0"

fname = pooch.retrieve(
    url=f"{url}/{version}/bathymetry.nc4",
    known_hash="sha256:95e0a54db26373ab1a436eda1abf3a7bc24237e2424f0ab063a4f3a1bd2079ed",
)

bathy = xr.open_dataset(fname)

# Coastline
feature = NaturalEarthFeature(
    name="coastline",
    category="physical",
    scale="10m",
    edgecolor="#000000",
    facecolor="#AAAAAA",
)




def create_map(projection=ccrs.PlateCarree(), figsize=(9, 9), bbox=None):
    fig, ax = plt.subplots(
        figsize=figsize,
        subplot_kw={
            "projection": projection,
        },
    )
    gl = ax.gridlines(draw_labels=True)
    gl.top_labels = gl.right_labels = False
    gl.xformatter = LONGITUDE_FORMATTER
    gl.yformatter = LATITUDE_FORMATTER
    ax.coastlines(resolution="10m")

    ax.add_feature(feature, zorder=0)
    ax.set_extent(bbox)

    # Bathymetry
    levels = [-100, -25]

    def fmt(x):
        s = f"{x:.1f}"
        return rf"{s} m"

    labels =ax.contour(
        bathy["longitude"],
        bathy["latitude"],
        -bathy["depth"],
        levels=levels,
        colors="black",
        alpha=0.75,
        zorder=99,
        linestyles="-",
    )
    ax.clabel(labels, labels.levels, inline=True, fmt=fmt, fontsize=10)
    return fig, ax

