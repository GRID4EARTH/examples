# GRID4EARTH examples

Worked, runnable examples on the data GRID4EARTH publishes on the HEALPix grid of the WGS84 ellipsoid. Every notebook reads the public object store over HTTPS: no account, no download beforehand.

| Notebook | What it shows |
|---|---|
| [01 – Sentinel-2: find, open, extract and plot at several resolutions](notebooks/01-sentinel-2-find-open-plot.ipynb) | Find the store of a place in the STAC catalogue or from its coordinates alone, open it with Xarray and xdggs, read a point and a region, plot the same area at levels 14, 17 and 20. |
| 02 – Sentinel-2, Sentinel-3 and ERA5 on one grid (in preparation) | Combine products of the same day (2026-08-12) without regridding. |

## Run them

```bash
python -m venv .venv
.venv/bin/pip install -r requirements.txt jupyterlab
.venv/bin/jupyter lab notebooks/
```

The Sentinel-2 stores use the `hcc-sentinel2-pyramid` codec of [healpix-compress](https://github.com/GRID4EARTH/healpix-compress); zarr finds it once the package is installed.

## Data

The data are described in the [STAC catalogue](https://stac-browser.grid4earth.eu) and served from `https://data.grid4earth.eu/`. They are test data: the layout and the metadata may still change.

## Licence

The code in these notebooks is released under the [Apache License 2.0](LICENSE).
