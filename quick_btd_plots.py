# file: quick_btd_plots.py
import os, re
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
from glob import glob

DL = os.path.expanduser("~/Downloads")

# --- Find your four files in Downloads ---
files = sorted(glob(os.path.join(DL, "OR_ABI-L2-CMIPC-*.nc")))
assert len(files) >= 4, f"Expected 4 .nc files in {DL}, found {len(files)}"

# Group by band & time token (the 'sYYYYDDDHHMM...' token)
pat = re.compile(r".*_(C\d{2})_G18_(_?s\d+)_")
by_key = {}
for f in files:
    m = pat.match(f.replace("M6","")) or pat.match(f)
    assert m, f"Could not parse {f}"
    band, s = m.group(1), m.group(2)
    by_key.setdefault(s, {})[band] = f

# Pick the two times that have both C07 and C13
pairs = [(s, d["C07"], d["C13"]) for s, d in by_key.items() if "C07" in d and "C13" in d]
pairs = sorted(pairs)  # chronological
assert len(pairs) >= 2, f"Need at least two matched times, found {len(pairs)}"
(t1, c07_t1, c13_t1), (t2, c07_t2, c13_t2) = pairs[:2]
print("Using times:", t1, "and", t2)

def open_cmi(fn):
    ds = xr.open_dataset(fn)
    da = ds["CMI"].load()  # emissive bands store brightness temperature (K)
    return da

# Load both bands at t1 and t2
BT07_t1 = open_cmi(c07_t1)
BT13_t1 = open_cmi(c13_t1)
BT07_t2 = open_cmi(c07_t2)
BT13_t2 = open_cmi(c13_t2)

# Compute BTD = BT(10.3 µm) - BT(3.9 µm)
BTD_t1 = (BT13_t1 - BT07_t1).assign_attrs(long_name="BTD 10.3-3.9 µm", units="K")
BTD_t2 = (BT13_t2 - BT07_t2).assign_attrs(long_name="BTD 10.3-3.9 µm", units="K")
DBTD   = (BTD_t2 - BTD_t1).assign_attrs(long_name="ΔBTD (t2 − t1)", units="K")

print("BTD t1 (min/max):", float(BTD_t1.min()), float(BTD_t1.max()))
print("BTD t2 (min/max):", float(BTD_t2.min()), float(BTD_t2.max()))

def save_img(arr, name, vmin=None, vmax=None):
    plt.figure(figsize=(7,6))
    im = plt.imshow(arr, origin="lower", vmin=vmin, vmax=vmax)
    plt.title(name)
    cbar = plt.colorbar(im)
    cbar.set_label(arr.attrs.get("units",""))
    out = os.path.join(DL, f"{name.replace(' ','_').replace('(','').replace(')','')}.png")
    plt.tight_layout()
    plt.savefig(out, dpi=180)
    plt.close()
    print("wrote", out)

# Reasonable stretches (tweak if needed)
save_img(BT13_t1, "C13_t1 (10.3 µm, K)", vmin=270, vmax=310)
save_img(BT07_t1, "C07_t1 (3.9 µm, K)",  vmin=260, vmax=310)
save_img(BTD_t1,  "BTD_t1 (10.3−3.9 µm, K)", vmin=-5, vmax=10)

save_img(BT13_t2, "C13_t2 (10.3 µm, K)", vmin=270, vmax=310)
save_img(BT07_t2, "C07_t2 (3.9 µm, K)",  vmin=260, vmax=310)
save_img(BTD_t2,  "BTD_t2 (10.3−3.9 µm, K)", vmin=-5, vmax=10)

# Optional difference image for motion cue
save_img(DBTD, "BTD_diff_t2_minus_t1 (K)", vmin=-5, vmax=5)

# Save small NetCDFs (optional)
BTD_t1.to_netcdf(os.path.join(DL, "BTD_t1.nc"))
BTD_t2.to_netcdf(os.path.join(DL, "BTD_t2.nc"))
print("Saved BTD_t1.nc and BTD_t2.nc in Downloads.")
