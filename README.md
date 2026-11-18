# GRID4EARTH examples

Worked, runnable examples on the data GRID4EARTH publishes on the HEALPix grid of the WGS84 ellipsoid. Every notebook reads the public object store over HTTPS: no account, no download beforehand.

| Notebook | What it shows |
|---|---|
| [01 – Sentinel-2: find, open, extract and plot at several resolutions](notebooks/01-sentinel-2-find-open-plot.ipynb) | Find the store of a place in the STAC catalogue or from its coordinates alone, open it with Xarray and xdggs, read a point and a region, plot the same area at levels 14, 17 and 20. A second route to the same cells: the Icechunk mosaic, a pass stack with a time axis. All addresses and identifiers sit in one configuration cell. |
| [02 – Mixing products on one grid: Sentinel-2, Sentinel-3 OLCI and SLSTR, Copernicus DEM and ERA5](notebooks/02-mixing-products-on-one-grid.ipynb) | Read the same cells from stores with different layouts (per parent cell, per overpass, global, mosaic) and resolutions, put them in one dataset without regridding, turn Sentinel-3 radiance into reflectance, mask clouds of both satellites, compare Sentinel-2 with Sentinel-3 and OLCI with SLSTR cell for cell and at coarser levels, build one spectrum from OLCI, SLSTR and Sentinel-2, compute a moisture index that needs both Sentinel-3 instruments, open a Sentinel-3 Synergy store, bring a whole Sentinel-2 pass up to the 50 km cells of the reanalysis, subset by region (a range of cell ids, or a longitude/latitude box with xdggs read through the Sentinel-2 mosaic) and by time (a STAC search by date, or the time axis of the Icechunk mosaic), and zoom in to a finer level. ERA5 stands in for DestinE ClimateDT, which cannot be published openly; with a ClimateDT store converted by [healpix-convert](https://github.com/GRID4EARTH/healpix-convert), the notebook runs on it instead. All addresses, identifiers and dates sit in one configuration cell. |

## Run them

```bash
python -m venv .venv
.venv/bin/pip install -r requirements.txt jupyterlab
.venv/bin/jupyter lab notebooks/
```

The notebooks were run with Python 3.13. Notebook 02 takes a few minutes, most of it reading over HTTPS.

`requirements.txt` gives minimum versions. `requirements-lock.txt` pins the exact environment the notebooks were last run with (Python 3.13); install it instead to reproduce a run:

```bash
python3.13 -m venv .venv
.venv/bin/pip install -r requirements-lock.txt
```

## Test them

```bash
.venv/bin/python tests/run_notebooks.py
```

runs every notebook in a fresh kernel and checks key results (cell counts, the agreement between Sentinel-2, OLCI and SLSTR, the mosaic against the STAC items, ...). It fails when a cell raises an error or a result is not the expected one; `--save` also writes the outputs back into the notebooks, and a name filter (`tests/run_notebooks.py 02`) runs one notebook only.

The Sentinel-2 stores use the `hcc-sentinel2-pyramid` codec of [healpix-compress](https://github.com/GRID4EARTH/healpix-compress); zarr finds it once the package is installed.

## Data

The data are described in the [STAC catalogue](https://stac-browser.grid4earth.eu) and served from `https://data.grid4earth.eu/`. The data are version 0 test data: the layout and the metadata may still change, and in the Sentinel-2 stores the no-data part outside the swath is 0.0 instead of NaN (a known issue of this version, GRID4EARTH/healpix-resample#119), visible as a staircase along swath edges. A later version replaces the data.

## Licence

The code in these notebooks is released under the [Apache License 2.0](LICENSE). The data keep their own licences:

- Contains modified Copernicus Sentinel data (2026), processed by GRID4EARTH.
- Copernicus DEM GLO-30: © DLR e.V. 2010-2014 and © Airbus Defence and Space GmbH 2014-2018, provided under COPERNICUS by the European Union and ESA.
- Contains modified Copernicus Climate Change Service information (2026) (ERA5). Neither the European Commission nor ECMWF is responsible for any use of this information.
