#!/usr/bin/env bash
set -euo pipefail

# Example: downloads four files into current directory.
aws s3 cp --no-sign-request   s3://noaa-goes18/ABI-L2-CMIPC/2025/303/23/ .   --recursive --exclude "*"   --include "*M6C07_G18_s20253032336175_*.nc"   --include "*M6C13_G18_s20253032336175_*.nc"

aws s3 cp --no-sign-request   s3://noaa-goes18/ABI-L2-CMIPC/2025/304/00/ .   --recursive --exclude "*"   --include "*M6C07_G18_s20253040006175_*.nc"   --include "*M6C13_G18_s20253040006175_*.nc"
