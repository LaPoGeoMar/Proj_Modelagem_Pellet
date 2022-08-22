from pathlib import Path

import humanize
import xarray as xr

# The commented out variables at not saved!
variables = [
    # "grid_longitude",
    # "grid_latitude",
    #     "k",
    #     "grid_depth",
    # "depth",
    #     "zactive",
    #     "area",
    "waterlevel",
    "velocity_x",
    "velocity_y",
    #     "velocity_omega",
    #     "velocity_z",
    #     "tau_x",
    #     "tau_y",
    #     "density",
    #     "salinity",
    #     "temperature",
    #     "tke",
    #     "eps",
    #     "viscosity_z",
    #     "diffusivity_z",
    #     "Ri",
]


def subset_ds(fname):
    ds = xr.open_dataset(fname, drop_variables="time_bounds")
    # We will store only the surface and trim a bit on the western boundary.
    subset = (
        ds[variables]
        .sel(m=slice(-49, -47.5))  # Cut some of the western part of the domain
        .isel({"Layer": 0})  # just the surface
    )
    print(f"\nSubsetting {fname.name}")
    print(f"Original size: {humanize.naturalsize(ds.nbytes)}")
    print(f"Subset: {humanize.naturalsize(subset.nbytes)}")
    subset.to_netcdf(f"subset-{fname.name}", format="NETCDF4", engine="netcdf4")
    ds.close()
    subset.close()


path = Path(".").absolute()
for fname in path.glob("*.nc4"):
    subset_ds(fname)
