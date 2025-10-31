// docs/app.js
console.log("La Jolla Fog Edge Tracker: scaffold ready.");

const IMG = document.getElementById("ab-image");
const statusEl = document.getElementById("status");

// paths relative to /docs
const SRC_T1   = "assets/BTD_t1.png";
const SRC_T2   = "assets/BTD_t2.png";
const SRC_DIFF = "assets/BTD_diff_t2_minus_t1.png"; // optional

function show(src, label) {
  statusEl.textContent = "Loading…";
  IMG.onerror = () => {
    statusEl.textContent = "Image not found: " + src;
  };
  IMG.onload = () => {
    statusEl.textContent = label;
  };
  IMG.src = src;
}

document.getElementById("btnA").onclick = () => show(SRC_T1,  "Showing t₁ (BTD)");
document.getElementById("btnB").onclick = () => show(SRC_T2,  "Showing t₂ (BTD)");

const diffBtn = document.getElementById("btnD");
if (diffBtn) diffBtn.onclick = () => show(SRC_DIFF, "Showing ΔBTD (t₂–t₁)");
