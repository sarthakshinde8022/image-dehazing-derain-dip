# Progress Log

Weekly write-ups for teacher check-ins. Each entry covers what was built, the
core idea behind it, the result, and what's next.

---

## Week 1 — Classical Dehazing Baseline

**Objective:** Establish a working classical dehazing pipeline as the
foundation for the project.

**What was built:**
- Implemented the Dark Channel Prior (He, Sun, Tang, 2009) in
  `dehazing/dark_channel_prior.py`
- Pipeline: dark channel computation → atmospheric light estimation →
  transmission map estimation → guided filter refinement → scene radiance
  recovery
- Deployed as a live, interactive multi-page Streamlit app (Home, How to
  Use, Try the Demo) with adjustable parameters (patch size, omega, min
  transmission, guided filter radius)

**The core idea:**
The atmospheric scattering model describes a hazy image as:
I(x) = J(x)·t(x) + A·(1 − t(x))
where `I` is what the camera sees, `J` is the true clean scene, `A` is
atmospheric light, and `t` is the transmission — how much of the original
light survives the haze. Dehazing means estimating `A` and `t`, then
solving for `J`. The Dark Channel Prior estimates `t` from the observation
that haze-free outdoor patches almost always have at least one very dark
color channel somewhere — so wherever the image isn't "dark enough," that's
a sign of haze.

**Result:** Working end-to-end demo — upload a hazy photo, see it dehazed
in real time, download the result.

**Next (Week 2):** Quantitative evaluation — run this pipeline across the
full SOTS benchmark and report PSNR/SSIM, indoor vs. outdoor.

## Week 2 — Dehazing Evaluation

**Objective:** Quantitatively evaluate the DCP baseline on the SOTS benchmark.

**What was done:**
- Ran `evaluation/evaluate_sots.py` on all SOTS indoor and outdoor pairs
- Metrics: PSNR and SSIM against ground truth

**Results:**

| Subset | Images | Mean PSNR (dB) | Mean SSIM |
|--------|--------|----------------|-----------|
| Indoor | [n] | [x.xx] | [0.xxxx] |
| Outdoor | [n] | [x.xx] | [0.xxxx] |

**Observations:** [Which subset performed better and why. One failure case and its cause.]

**Next (Week 3):** Classical rain streak removal (guided-filter frequency decomposition).
## Week 3 — Classical Rain Streak Removal

**Objective:** Implement a classical rain streak removal method and
integrate it into the live demo.

**What was built:**
- Frequency decomposition: Gaussian blur separates the image into a
  low-frequency base layer and a high-frequency detail layer
- Streak isolation: a directional morphological white top-hat (erosion
  with a short, wide horizontal kernel) removes anything narrower than
  a chosen pixel width, isolating thin near-vertical rain streaks from
  genuine scene detail
- Wired into the "Rain Streak Removal" tab of the live demo, with the
  same upload → adjust → compare → download flow as dehazing

**A design correction worth noting:** the original plan used a
self-guided filter for frequency decomposition (matching the dehazing
module's style). Testing on a synthetic rain image showed this actively
hurt results — a guided filter preserves sharp edges by design, so it
treated rain streaks as "real" structure and leaked them into the base
layer instead of isolating them. Switching to a plain Gaussian blur
(which doesn't try to preserve any edges) fixed this immediately.

**Validation:** Tested on a synthetic image with known clean ground
truth (smooth gradient background + synthetic vertical streaks).
PSNR improved from 21.74 dB (rainy) to 40.15 dB (derained); SSIM from
0.694 to 0.969.

**Next (Week 4):** Quantitative evaluation on the Rain100L/Rain100H
benchmark, and wiring a results CSV + sample comparisons the same way
Week 2 did for dehazing.
