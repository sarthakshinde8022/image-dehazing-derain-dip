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
