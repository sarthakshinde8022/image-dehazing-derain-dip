"""
Try the Demo — interactive dehazing and rain streak removal tool.
"""

import io

import cv2
import numpy as np
import streamlit as st
from PIL import Image
from skimage.metrics import peak_signal_noise_ratio as psnr
from skimage.metrics import structural_similarity as ssim

from dehazing.dark_channel_prior import dehaze
from deraining.rain_streak_removal import derain
from theme import inject_custom_css

st.set_page_config(page_title="Try the Demo — Clarity", page_icon="🌫️", layout="wide")
inject_custom_css()

st.page_link("app.py", label="← Home", icon="🏠")

st.markdown('<div class="eyebrow">LIVE DEMO</div>', unsafe_allow_html=True)
st.markdown("# Try It")
st.markdown(
    '<p style="color:#93A5B1;">Upload a hazy or rainy image and watch the '
    'classical DIP pipeline restore it.</p>',
    unsafe_allow_html=True,
)
st.markdown('<hr class="clarity-divider">', unsafe_allow_html=True)

tab_dehaze, tab_derain = st.tabs(["Dehazing", "Rain Streak Removal"])

# ---------------------------------------------------------------- Dehazing
with tab_dehaze:
    with st.sidebar:
        st.markdown("### Dehazing Parameters")
        patch_size = st.slider("Patch size", min_value=3, max_value=31, value=15, step=2)
        omega = st.slider("Omega (haze retention)", 0.50, 1.00, 0.95, 0.01)
        t0 = st.slider("Min transmission (t0)", 0.01, 0.50, 0.10, 0.01)
        guided_radius = st.slider("Guided filter radius", 10, 80, 40, 5)
        st.markdown("---")
        st.page_link("pages/1_How_to_Use.py", label="What do these mean?", icon="📖")

    col_upload1, col_upload2 = st.columns(2)
    with col_upload1:
        uploaded_file = st.file_uploader(
            "Upload a hazy image", type=["jpg", "jpeg", "png"], key="hazy"
        )
    with col_upload2:
        gt_file = st.file_uploader(
            "Optional: ground-truth clean image (for PSNR/SSIM)",
            type=["jpg", "jpeg", "png"],
            key="gt",
        )

    if uploaded_file is not None:
        image = Image.open(uploaded_file).convert("RGB")
        img_array = np.array(image)
        img_bgr = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)

        with st.spinner("Running Dark Channel Prior dehazing..."):
            result_bgr = dehaze(
                img_bgr,
                patch_size=patch_size,
                omega=omega,
                t0=t0,
                guided_radius=guided_radius,
            )
        result_rgb = cv2.cvtColor(result_bgr, cv2.COLOR_BGR2RGB)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<div class="eyebrow">BEFORE</div>', unsafe_allow_html=True)
            st.image(image, use_container_width=True)
        with col2:
            st.markdown('<div class="eyebrow">AFTER</div>', unsafe_allow_html=True)
            st.image(result_rgb, use_container_width=True)

        result_pil = Image.fromarray(result_rgb)
        buf = io.BytesIO()
        result_pil.save(buf, format="PNG")
        st.download_button(
            "Download dehazed image",
            data=buf.getvalue(),
            file_name="dehazed.png",
            mime="image/png",
            key="download_dehazed",
        )

        if gt_file is not None:
            gt_image = Image.open(gt_file).convert("RGB")
            gt_array = np.array(gt_image)
            if gt_array.shape[:2] != result_rgb.shape[:2]:
                gt_array = cv2.resize(
                    gt_array, (result_rgb.shape[1], result_rgb.shape[0])
                )
            p = psnr(gt_array, result_rgb, data_range=255)
            s = ssim(gt_array, result_rgb, data_range=255, channel_axis=2)
            st.markdown('<hr class="clarity-divider">', unsafe_allow_html=True)
            st.markdown("### Metrics vs. ground truth")
            m1, m2 = st.columns(2)
            m1.metric("PSNR", f"{p:.2f} dB")
            m2.metric("SSIM", f"{s:.4f}")
    else:
        st.info("Upload a hazy image above to see the dehazing result.")

# ----------------------------------------------------------- Rain Removal
with tab_derain:
    with st.sidebar:
        st.markdown("### Rain Removal Parameters")
        derain_radius = st.slider(
            "Blur radius (base layer)", 5, 41, 15, 2, key="derain_radius"
        )
        max_streak_width = st.slider(
            "Max streak width (px)", 1, 15, 5, 1, key="max_streak_width"
        )
        st.caption(
            "Any bright structure narrower than this, in the horizontal "
            "direction, is treated as a rain streak."
        )

    col_upload3, col_upload4 = st.columns(2)
    with col_upload3:
        rainy_file = st.file_uploader(
            "Upload a rainy image", type=["jpg", "jpeg", "png"], key="rainy"
        )
    with col_upload4:
        gt_rain_file = st.file_uploader(
            "Optional: ground-truth clean image (for PSNR/SSIM)",
            type=["jpg", "jpeg", "png"],
            key="gt_rain",
        )

    if rainy_file is not None:
        rainy_image = Image.open(rainy_file).convert("RGB")
        rainy_array = np.array(rainy_image)
        rainy_bgr = cv2.cvtColor(rainy_array, cv2.COLOR_RGB2BGR)

        with st.spinner("Isolating and removing rain streaks..."):
            derained_bgr = derain(
                rainy_bgr,
                radius=derain_radius,
                max_streak_width=max_streak_width,
            )
        derained_rgb = cv2.cvtColor(derained_bgr, cv2.COLOR_BGR2RGB)

        col3, col4 = st.columns(2)
        with col3:
            st.markdown('<div class="eyebrow">BEFORE</div>', unsafe_allow_html=True)
            st.image(rainy_image, use_container_width=True)
        with col4:
            st.markdown('<div class="eyebrow">AFTER</div>', unsafe_allow_html=True)
            st.image(derained_rgb, use_container_width=True)

        derained_pil = Image.fromarray(derained_rgb)
        buf2 = io.BytesIO()
        derained_pil.save(buf2, format="PNG")
        st.download_button(
            "Download derained image",
            data=buf2.getvalue(),
            file_name="derained.png",
            mime="image/png",
            key="download_derained",
        )

        if gt_rain_file is not None:
            gt_rain_image = Image.open(gt_rain_file).convert("RGB")
            gt_rain_array = np.array(gt_rain_image)
            if gt_rain_array.shape[:2] != derained_rgb.shape[:2]:
                gt_rain_array = cv2.resize(
                    gt_rain_array, (derained_rgb.shape[1], derained_rgb.shape[0])
                )
            p2 = psnr(gt_rain_array, derained_rgb, data_range=255)
            s2 = ssim(gt_rain_array, derained_rgb, data_range=255, channel_axis=2)
            st.markdown('<hr class="clarity-divider">', unsafe_allow_html=True)
            st.markdown("### Metrics vs. ground truth")
            m3, m4 = st.columns(2)
            m3.metric("PSNR", f"{p2:.2f} dB")
            m4.metric("SSIM", f"{s2:.4f}")
    else:
        st.info("Upload a rainy image above to see the rain streak removal result.")
