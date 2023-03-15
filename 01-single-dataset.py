from pathlib import Path

import humanize
import xarray as xr

path = Path(".").absolute()
datasets = [
    # (time: 721, m: 138, n: 218)
    xr.open_dataset(fname)
    for fname in sorted(path.glob("subset-*.nc"))
]
ds = xr.concat(datasets, dim="time")

print(humanize.naturalsize(ds.nbytes))

ds.to_netcdf("model_tides_only.nc", format="NETCDF4", engine="netcdf4", compute=True)
