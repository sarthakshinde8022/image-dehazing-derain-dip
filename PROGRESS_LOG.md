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
