"""
Home page — Image Dehazing & Rain Streak Removal mini project.
"""

import streamlit as st

from theme import inject_custom_css, CLARITY

st.set_page_config(
    page_title="Clarity — Dehazing & Deraining",
    page_icon="🌫️",
    layout="wide",
)

inject_custom_css()

# ---- Hero ---------------------------------------------------------------
st.markdown('<div class="eyebrow">DIGITAL IMAGE PROCESSING · MINI PROJECT</div>', unsafe_allow_html=True)
st.markdown("# Clarity, Restored")
st.markdown(
    """
    <p style="font-size:1.1rem; color:#93A5B1; max-width:640px;">
    Haze and rain degrade images the same way — light gets scattered
    before it reaches the lens. This project reverses that scattering
    computationally, recovering the clean scene underneath using
    classical DIP techniques and lightweight deep learning.
    </p>
    """,
    unsafe_allow_html=True,
)

col_cta1, col_cta2, _ = st.columns([1.1, 1, 2])
with col_cta1:
    st.page_link("pages/2_Try_the_Demo.py", label="Try the demo →", icon="🌫️")
with col_cta2:
    st.page_link("pages/1_How_to_Use.py", label="How to use", icon="📖")

st.markdown('<hr class="clarity-divider">', unsafe_allow_html=True)

# ---- Before / After illustrative visual ----------------------------------
col_a, col_arrow, col_b = st.columns([1, 0.3, 1])
with col_a:
    st.markdown(
        """
        <div class="stage-card" style="background:linear-gradient(135deg,#3a4652,#586573);
             height:170px; display:flex; align-items:flex-end; padding:1rem; filter:blur(1.5px) saturate(55%);">
        <span style="font-family:'IBM Plex Mono',monospace; font-size:0.8rem; color:#EAF2F5;">
        INPUT — hazy / rain-affected</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
with col_arrow:
    st.markdown(
        f"""<div style="display:flex; align-items:center; justify-content:center;
        height:170px; font-size:1.8rem; color:{CLARITY};">→</div>""",
        unsafe_allow_html=True,
    )
with col_b:
    st.markdown(
        f"""
        <div class="stage-card" style="background:linear-gradient(135deg,#1B2430,{CLARITY}33);
             height:170px; display:flex; align-items:flex-end; padding:1rem;">
        <span style="font-family:'IBM Plex Mono',monospace; font-size:0.8rem; color:#EAF2F5;">
        OUTPUT — restored scene</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown('<hr class="clarity-divider">', unsafe_allow_html=True)

# ---- Pipeline stages (a real sequence, so numbering carries meaning) -----
st.markdown("### How restoration happens")
stage1, stage2, stage3 = st.columns(3)

stages = [
    ("01", "Rain Streak Removal",
     "Decompose the image into low/high-frequency layers with a guided "
     "filter, isolate near-vertical streak patterns, and subtract them "
     "from the detail layer."),
    ("02", "Haze Removal",
     "Estimate atmospheric light and a per-pixel transmission map using "
     "the Dark Channel Prior, then invert the atmospheric scattering "
     "model."),
    ("03", "Refinement",
     "A guided filter smooths the transmission map along real edges, "
     "avoiding the halo artifacts a naive inversion would leave behind."),
]

for col, (num, title, desc) in zip((stage1, stage2, stage3), stages):
    with col:
        st.markdown(
            f"""
            <div class="stage-card">
            <div class="stage-number">{num}</div>
            <div style="font-weight:600; margin:0.4rem 0;">{title}</div>
            <div style="color:#93A5B1; font-size:0.9rem;">{desc}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.markdown('<hr class="clarity-divider">', unsafe_allow_html=True)

# ---- Tech stack -----------------------------------------------------------
st.markdown("### Built with")
badges = ["Dark Channel Prior", "Guided Filtering", "OpenCV",
          "AOD-Net (in progress)", "Streamlit", "Python"]
st.markdown("".join(f'<span class="badge">{b}</span>' for b in badges), unsafe_allow_html=True)

st.markdown('<hr class="clarity-divider">', unsafe_allow_html=True)
st.caption("Mini project · Image Dehazing and Rain Streak Removal using DIP Techniques")
