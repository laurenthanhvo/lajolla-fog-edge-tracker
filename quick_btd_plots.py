# file: quick_btd_plots.py
import os, re
import xarray as xr
import matplotlib.pyplot as plt
from glob import glob

# --- Find your four files in Downloads ---
files = sorted(glob(os.path.expanduser("~/Downloads/OR_ABI-L2-CMIPC-*.nc")))
assert len(files) >= 4, f"Expected 4 .nc files, found {len(files)}"

# Group by band & time token (the 'sYYYYDDDHHMM...' token)
pat = re.compile(r".*_(C\d{2})_G18_(_?s\d+)_")
by_key = {}
for f in files:
    m = pat.match(f.replace("M6","")) or pat.match(f)  # be flexible
    assert m, f"Could not parse {f}"
    band, s = m.group(1), m.group(2)
    by_key.setdefault(s, {})[band] = f

# Pick the two times that have both C07 and C13
pairs = [(s, d["C07"], d["C13"]) for s, d in by_key.items() if "C07" in d and "C13" in d]
pairs = sorted(pairs)  # chronological
assert len(pairs) >= 2, f"Need at least two matched times, found {len(pairs)}"
(t1, c07_t1, c13_t1), (t2, c07_t2, c13_t2) = pairs[:2]
print("Using:", t1, "and", t2)

def open_cmi(fn):
    ds = xr.open_dataset(fn)
    # CMIPC emissive bands store brightness temperature (K) in CMI
    da = ds["CMI"].load()
    return da

# Load both bands at t1 and t2
BT07_t1 = open_cmi(c07_t1)
BT13_t1 = open_cmi(c13_t1)
BT07_t2 = open_cmi(c07_t2)
BT13_t2 = open_cmi(c13_t2)

# Compute BTD = BT(10.3 µm) - BT(3.9 µm)
BTD_t1 = (BT13_t1 - BT07_t1).assign_attrs(long_name="BTD 10.3-3.9 µm", units="K")
BTD_t2 = (BT13_t2 - BT07_t2).assign_attrs(long_name="BTD 10.3-3.9 µm", units="K")

print("BTD t1 (min/max):", float(BTD_t1.min()), float(BTD_t1.max()))
print("BTD t2 (min/max):", float(BTD_t2.min()), float(BTD_t2.max()))

# Quicklook images (no reprojection yet)
for name, arr in [("BTD_t1", BTD_t1), ("BTD_t2", BTD_t2)]:
    plt.figure(figsize=(7,6))
    # Reasonable stretch for fog highlighting; tweak vmin/vmax by printouts above
    im = plt.imshow(arr, origin="lower", vmin=-5, vmax=10)  # K
    plt.title(f"{arr.attrs.get('long_name','BTD')} ({name})")
    cbar = plt.colorbar(im)
    cbar.set_label("K")
    out = os.path.expanduser(f"~/Downloads/{name}.png")
    plt.tight_layout()
    plt.savefig(out, dpi=180)
    plt.close()
    print("wrote", out)

# Also save the arrays if you want to quickly diff later
BTD_t1.to_netcdf(os.path.expanduser("~/Downloads/BTD_t1.nc"))
BTD_t2.to_netcdf(os.path.expanduser("~/Downloads/BTD_t2.nc"))
print("Saved BTD_t1.nc and BTD_t2.nc in Downloads.")
