"""
How to Use page.
"""

import streamlit as st

from theme import inject_custom_css

st.set_page_config(page_title="How to Use — Clarity", page_icon="📖", layout="wide")
inject_custom_css()

st.page_link("app.py", label="← Home", icon="🏠")

st.markdown('<div class="eyebrow">GUIDE</div>', unsafe_allow_html=True)
st.markdown("# How to Use")
st.markdown(
    '<p style="color:#93A5B1; max-width:640px;">Everything you need to get '
    'a clean result out of the demo, plus what each parameter actually does.</p>',
    unsafe_allow_html=True,
)

st.markdown('<hr class="clarity-divider">', unsafe_allow_html=True)

steps = [
    ("01", "Upload a hazy image",
     "JPG or PNG. Outdoor scenes with visible depth (a road, a skyline, "
     "trees at different distances) show the clearest before/after "
     "difference — the Dark Channel Prior relies on depth variation to "
     "work well."),
    ("02", "Adjust the parameters (optional)",
     "Defaults work for most images. Nudge them if the result looks off "
     "— see the parameter guide below."),
    ("03", "Compare the result",
     "The hazy and dehazed versions appear side by side. Upload a "
     "matching ground-truth image too, and you'll get PSNR/SSIM scores."),
    ("04", "Download",
     "Save the dehazed output directly from the demo page."),
]

for num, title, desc in steps:
    st.markdown(
        f"""
        <div class="stage-card" style="margin-bottom:0.9rem;">
        <div class="stage-number">{num}</div>
        <div style="font-weight:600; margin:0.4rem 0;">{title}</div>
        <div style="color:#93A5B1; font-size:0.92rem;">{desc}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown('<hr class="clarity-divider">', unsafe_allow_html=True)

st.markdown("### Parameter guide")
param_col1, param_col2 = st.columns(2)
with param_col1:
    st.markdown("**Patch size**")
    st.caption(
        "Size of the local window used to estimate haze density. Larger "
        "values smooth results but blur fine detail; smaller values keep "
        "detail but can look patchy."
    )
    st.markdown("**Omega (haze retention)**")
    st.caption(
        "How aggressively haze is removed. Near 1.0 removes almost all "
        "haze but can look unnatural; lower values keep a touch of realism."
    )
with param_col2:
    st.markdown("**Min transmission (t0)**")
    st.caption(
        "A floor on how much the algorithm trusts heavily-hazed regions. "
        "Lower values recover more detail there but risk amplifying noise."
    )
    st.markdown("**Guided filter radius**")
    st.caption(
        "Controls how far the refinement step looks around each pixel "
        "when smoothing the transmission map to match real edges."
    )

st.markdown('<hr class="clarity-divider">', unsafe_allow_html=True)

st.markdown("### Common issues")
with st.expander("The sky looks too dark or has a color cast"):
    st.write(
        "This is a known limitation of the Dark Channel Prior — the "
        "assumption it relies on breaks down in large, uniformly bright "
        "regions like open sky. Worth including as a discussed "
        "limitation in your project report rather than something to "
        "fully eliminate."
    )
with st.expander("I see halo-like edges around objects"):
    st.write(
        "Usually means the guided filter radius is too small for the "
        "image's resolution. Try increasing it."
    )
with st.expander("The result barely changed from the original"):
    st.write(
        "Try increasing omega, or check that the image is actually "
        "hazy — the algorithm has little to correct in an already-clear "
        "photo."
    )

st.markdown('<hr class="clarity-divider">', unsafe_allow_html=True)
st.page_link("pages/2_Try_the_Demo.py", label="Ready — try the demo →", icon="🌫️")
