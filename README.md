# Fog Edge Chaser (GOES CONUS BTD quicklook)

Interactive Visualization Project — UCSD (La Jolla focus)

This repo scaffolds your assignment and gives you a **Python quicklook** to generate 5–6 exploratory images from GOES-18 CONUS Cloud & Moisture Imagery (ABI-L2-CMIPC), using the **classic night fog Brightness-Temperature Difference**: **BT(10.3 µm) − BT(3.9 µm)**.

> You will later build the required **D3.js** interactive page (served from `/docs`) that implements your fog-edge transect and speed readout. No server is needed.

---

## 0) Prereqs

- **AWS CLI** (no account required): `aws --version`
- **Python 3.9+** with: `xarray`, `netCDF4`, `matplotlib`

Install the Python deps:
```bash
python3 -m pip install --upgrade xarray netCDF4 matplotlib
```

## 1) Download four GOES files (two times × two bands)

From your Mac terminal (example times — update if you chose different minutes):

```bash
# Optionally create a tidy subfolder
mkdir -p "$HOME/Downloads/goes_fog_2025-10-30"
cd "$HOME/Downloads/goes_fog_2025-10-30"

# t1 (UTC 2025-10-30 23:36) — both bands
aws s3 cp --no-sign-request   s3://noaa-goes18/ABI-L2-CMIPC/2025/303/23/ .   --recursive --exclude "*"   --include "*M6C07_G18_s20253032336175_*.nc"   --include "*M6C13_G18_s20253032336175_*.nc"

# t2 (UTC 2025-10-31 00:06) — both bands (~30 min later)
aws s3 cp --no-sign-request   s3://noaa-goes18/ABI-L2-CMIPC/2025/304/00/ .   --recursive --exclude "*"   --include "*M6C07_G18_s20253040006175_*.nc"   --include "*M6C13_G18_s20253040006175_*.nc"
```

You should see **four files** (two `C07`, two `C13`).

> If you use different minutes, keep the `sYYYYDDDHHMM` token identical between `C07` and `C13` for each time.

## 2) Make your exploratory images

From the repo root (or anywhere), run the quicklook script which reads from `~/Downloads` by default:

```bash
python3 quick_btd_plots.py
# This writes: ~/Downloads/BTD_t1.png, ~/Downloads/BTD_t2.png
```

Adjust the `vmin/vmax` stretch in the script if needed (e.g., `-5 .. 12 K`).

## 3) D3 app scaffolding (to be implemented by you)

- `/docs/index.html` includes a D3 v7 import and a simple layout.
- You will add:
  - File pickers for the two BTD images (or computed rasters)
  - A/B toggle between **t₁** and **t₂**
  - A **drawn transect** interaction that samples along the line and reports pixel offset and speed (km/h), using the known **5‑min** CONUS cadence and GOES geostationary projection scale (no server).
  - Tooltips/details-on-demand and annotation.

Serve via GitHub Pages from `/docs` (Settings → Pages → Deploy from branch).

## 4) GitHub setup

```bash
git init
git add .
git commit -m "Init: GOES BTD quicklook + D3 scaffolding"
# create an empty repo on GitHub named fog-edge-chaser
git remote add origin https://github.com/<YOUR_USER>/fog-edge-chaser.git
git branch -M main
git push -u origin main
```

## Notes

- Dataset: **GOES-18**, product **ABI-L2-CMIPC** (CONUS). Files are public on AWS S3 (`--no-sign-request`).
- Bands: **C07 = 3.9 µm**, **C13 = 10.3 µm**. **BTD = BT(13) − BT(07)**.
- Keep everything static (no server) to meet the assignment constraints.
