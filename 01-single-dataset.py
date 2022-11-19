from pathlib import Path

import humanize
import xarray as xr

path = Path("model_tides_and_wind").absolute()
datasets = [
    # (time: 745, m: 138, n: 218)
    xr.open_dataset(fname)
    for fname in sorted(path.glob("*.nc4"))
]
ds = xr.concat(datasets, dim="time")

print(humanize.naturalsize(ds.nbytes))

ds.to_netcdf("model_tides_and_wind.nc4", format="NETCDF4", engine="netcdf4", compute=True)
