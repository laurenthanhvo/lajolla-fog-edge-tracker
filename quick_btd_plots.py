# file: quick_btd_plots.py
import os, re
from os.path import basename, expanduser, join
from glob import glob

import numpy as np
import xarray as xr
import matplotlib.pyplot as plt

DL = expanduser("~/Downloads")

# --- Find your four files in Downloads ---
files = sorted(glob(join(DL, "OR_ABI-L2-CMIPC-*.nc")))
assert len(files) >= 4, f"Expected ≥4 .nc files in {DL}, found {len(files)}"

# Parse band (C07/C13) and scan time token (sYYYYDDDHHMM...) from name
# Examples:
#   OR_ABI-L2-CMIPC-M6C07_G18_s20253032336175_e...
#   OR_ABI-L2-CMIPC-M6C13_G18_s20253040006175_e...
# We normalize "M6C07" -> "C07" and then search for "(C##)_G18_(s\d+)" anywhere.
pat = re.compile(r"(C\d{2})_G18_(s\d+)")
by_key = {}  # s-token -> { "C07": path, "C13": path }

for f in files:
    name = basename(f).replace("M6", "")  # tolerate M6 prefix
    m = pat.search(name)                  # <- search (not match) for robustness
    assert m, f"Could not parse band/time from: {name}"
    band, s = m.group(1), m.group(2)
    by_key.setdefault(s, {})[band] = f

# Pick the first two times that have both bands
pairs = [(s, d["C07"], d["C13"]) for s, d in by_key.items() if "C07" in d and "C13" in d]
pairs = sorted(pairs)  # chronological by s-token
assert len(pairs) >= 2, f"Need at least two matched times with both bands; found {len(pairs)}"
(t1, c07_t1, c13_t1), (t2, c07_t2, c13_t2) = pairs[:2]

print("Matched times (s-token):")
for s, c07, c13 in pairs[:4]:
    print("  ", s, "->", basename(c07), "|", basename(c13))
print("Using:", t1, "and", t2)

def open_cmi(fn):
    """Open GOES CMIPC emissive-band CMI (brightness temperature, K)."""
    ds = xr.open_dataset(fn)
    try:
        da = ds["CMI"].load()
        return da
    finally:
        ds.close()

# Load both bands at t1 and t2
BT07_t1 = open_cmi(c07_t1)
BT13_t1 = open_cmi(c13_t1)
BT07_t2 = open_cmi(c07_t2)
BT13_t2 = open_cmi(c13_t2)

# Compute BTD = BT(10.3 µm) - BT(3.9 µm)
BTD_t1 = (BT13_t1 - BT07_t1).assign_attrs(long_name="BTD 10.3-3.9 µm", units="K")
BTD_t2 = (BT13_t2 - BT07_t2).assign_attrs(long_name="BTD 10.3-3.9 µm", units="K")
DBTD   = (BTD_t2 - BTD_t1).assign_attrs(long_name="ΔBTD (t2 − t1)", units="K")

print("BTD t1 (min/max):", float(np.nanmin(BTD_t1)), float(np.nanmax(BTD_t1)))
print("BTD t2 (min/max):", float(np.nanmin(BTD_t2)), float(np.nanmax(BTD_t2)))

def save_img(arr, name, vmin=None, vmax=None):
    plt.figure(figsize=(7,6))
    im = plt.imshow(arr, origin="lower", vmin=vmin, vmax=vmax)
    plt.title(name)
    cbar = plt.colorbar(im)
    cbar.set_label(arr.attrs.get("units",""))
    out = join(DL, f"{name.replace(' ','_').replace('(','').replace(')','')}.png")
    plt.tight_layout()
    plt.savefig(out, dpi=180)
    plt.close()
    print("wrote", out)

# Reasonable stretches (adjust if your printouts suggest otherwise)
save_img(BT13_t1, "C13_t1 (10.3 µm, K)", vmin=270, vmax=310)
save_img(BT07_t1, "C07_t1 (3.9 µm, K)",  vmin=260, vmax=310)
save_img(BTD_t1,  "BTD_t1 (10.3−3.9 µm, K)", vmin=-5, vmax=10)

save_img(BT13_t2, "C13_t2 (10.3 µm, K)", vmin=270, vmax=310)
save_img(BT07_t2, "C07_t2 (3.9 µm, K)",  vmin=260, vmax=310)
save_img(BTD_t2,  "BTD_t2 (10.3−3.9 µm, K)", vmin=-5, vmax=10)

# Optional difference image for motion cue
save_img(DBTD, "BTD_diff_t2_minus_t1 (K)", vmin=-5, vmax=5)

# Save small NetCDFs (optional)
BTD_t1.to_netcdf(join(DL, "BTD_t1.nc"))
BTD_t2.to_netcdf(join(DL, "BTD_t2.nc"))
print("Saved BTD_t1.nc and BTD_t2.nc in Downloads.")
