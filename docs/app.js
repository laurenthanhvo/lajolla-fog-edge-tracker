// Placeholder. You will implement:
// 1) Load two rasters (PNG or computed canvas from BTD arrays)
// 2) A/B toggle
// 3) Transect drawing with D3 drag/line and sampling
// 4) Speed computation (km/h) based on pixel displacement + GOES scale
console.log("Fog Edge Chaser: scaffold ready.");

// docs/app.js
const IMG = document.getElementById("ab-image");
const statusEl = document.getElementById("status");

// paths relative to /docs
const SRC_T1 = "assets/BTD_t1.png";
const SRC_T2 = "assets/BTD_t2.png";
const SRC_DIFF = "assets/BTD_diff_t2_minus_t1.png"; // optional

function show(src, label){
  IMG.src = src;
  statusEl.textContent = label;
}

document.getElementById("btnA").onclick = () => show(SRC_T1, "Showing t₁ (BTD)");
document.getElementById("btnB").onclick = () => show(SRC_T2, "Showing t₂ (BTD)");
document.getElementById("btnD").onclick = () => show(SRC_DIFF, "Showing ΔBTD (if present)");
