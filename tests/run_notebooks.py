"""Run the example notebooks end to end and check key results.

    python tests/run_notebooks.py            # run all notebooks, check, keep the files unchanged
    python tests/run_notebooks.py --save     # also write the outputs back into the notebooks
    python tests/run_notebooks.py 02         # run only the notebooks whose name contains "02"

Each notebook runs in a fresh kernel from its own folder. A notebook fails
when a cell raises an error or when one of the expected lines below is
missing from its printed output. The data are read over HTTPS from
data.grid4earth.eu, so the run needs network access (a few minutes).
The exit code is the number of failed notebooks.
"""
import re
import sys
import time
from pathlib import Path

import nbformat
from nbclient import NotebookClient
from nbclient.exceptions import CellExecutionError

ROOT = Path(__file__).resolve().parent.parent
NOTEBOOKS = sorted((ROOT / "notebooks").glob("[0-9]*.ipynb"))
TIMEOUT = 1800  # seconds per cell

# Expected results: regular expressions that must match the text printed by the notebook.
# Numbers are checked to the precision given (the data are version 0 and may be replaced).
EXPECT = {
    "02-mixing-products-on-one-grid": [
        r"Sentinel-2: 65,536 cells, OLCI: 65,536 cells, SLSTR: 65,536 cells, elevation: 65,536 cells",
        r"ERA5: level 7, nested, WGS84, 24 times",
        r"b8a -> oa17: n = 65,\d{3}, r = 0\.9[34]\d",  # Sentinel-2 against OLCI at 865 nm
        r"oa17 -> sl3 : n = 65,\d{3}, r = 0\.9[34]\d",  # OLCI against SLSTR
        r"\n\s+11\s+256\s+0\.99\d",  # aggregated to level 11, S2 against OLCI r >= 0.99
        r"NDMI median: .*correlation r = 0\.[78]\d",
        r"reprocessed-synergy_20260915T101708_psf_level15: 38,763,176 cells",
        r"25 Sentinel-2 stores \(level-7 cells\) in this pass",
        r"NDVI change from the mosaic equals the one from the STAC items: True",
        r"49,605 cells valid in both, r = 0\.8\d",
    ],
}


def printed_text(nb):
    """All text a notebook printed (stream and plain-text results)."""
    out = []
    for cell in nb.cells:
        for o in cell.get("outputs", []):
            if o.get("output_type") == "stream":
                out.append(o.get("text", ""))
            elif "text/plain" in o.get("data", {}):
                out.append(o["data"]["text/plain"])
    return "\n".join(out)


def run(path, save):
    nb = nbformat.read(path, as_version=4)
    client = NotebookClient(nb, timeout=TIMEOUT, kernel_name="python3",
                            resources={"metadata": {"path": str(path.parent)}})
    t = time.perf_counter()
    try:
        client.execute()
    except CellExecutionError as e:
        print(f"FAIL {path.name}: a cell raised an error\n{str(e)[-2000:]}")
        return False
    text = printed_text(nb)
    missing = [p for p in EXPECT.get(path.stem, []) if not re.search(p, text)]
    for p in missing:
        print(f"FAIL {path.name}: expected output not found: {p}")
    if save and not missing:
        nbformat.write(nb, path)
    print(f"{'ok  ' if not missing else 'FAIL'} {path.name} ({time.perf_counter() - t:.0f} s, "
          f"{len(EXPECT.get(path.stem, [])) - len(missing)}/{len(EXPECT.get(path.stem, []))} checks)")
    return not missing


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    todo = [p for p in NOTEBOOKS if not args or any(a in p.name for a in args)]
    failed = sum(not run(p, "--save" in sys.argv) for p in todo)
    sys.exit(failed)
