"""
Dark Channel Prior based Image Dehazing
Reference: He, Sun, Tang (2009), "Single Image Haze Removal Using Dark Channel Prior"

Model: I(x) = J(x)*t(x) + A*(1 - t(x))
We estimate A (atmospheric light) and t(x) (transmission map),
then invert the equation to recover J(x), the haze-free scene radiance.
"""

import cv2
import numpy as np


def get_dark_channel(image, patch_size=15):
    """Compute the dark channel of an image.
    image: HxWx3 float image in [0,1]
    """
    min_channel = np.min(image, axis=2)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (patch_size, patch_size))
    dark_channel = cv2.erode(min_channel, kernel)
    return dark_channel


def estimate_atmospheric_light(image, dark_channel, top_percent=0.001):
    """Estimate atmospheric light A using the brightest pixels
    in the dark channel (top 0.1% by default)."""
    h, w = dark_channel.shape
    num_pixels = h * w
    num_top = max(int(num_pixels * top_percent), 1)

    flat_dark = dark_channel.reshape(num_pixels)
    flat_image = image.reshape(num_pixels, 3)

    indices = np.argpartition(flat_dark, -num_top)[-num_top:]
    brightest_pixels = flat_image[indices]

    # Among these candidates, pick the pixel with highest overall intensity
    A = brightest_pixels[np.argmax(np.sum(brightest_pixels, axis=1))]
    return A


def estimate_transmission(image, A, omega=0.95, patch_size=15):
    """Estimate the coarse transmission map. omega keeps a small amount
    of haze for distant objects, which looks more natural."""
    normalized = image / A
    transmission = 1 - omega * get_dark_channel(normalized, patch_size)
    return transmission


def guided_filter_refine(guide_image, transmission, radius=40, eps=1e-3):
    """Refine the transmission map using a guided filter so edges align
    with the original image instead of looking blocky.
    Uses cv2.ximgproc if available (opencv-contrib-python), otherwise
    falls back to a manual guided filter implementation."""
    guide_gray = cv2.cvtColor((guide_image * 255).astype(np.uint8), cv2.COLOR_BGR2GRAY)
    try:
        refined = cv2.ximgproc.guidedFilter(
            guide=guide_gray, src=transmission.astype(np.float32),
            radius=radius, eps=eps
        )
    except AttributeError:
        refined = _guided_filter_manual(
            guide_gray.astype(np.float32) / 255.0,
            transmission.astype(np.float32),
            radius, eps
        )
    return refined


def _guided_filter_manual(guide, src, radius, eps):
    """Fallback guided filter (box-filter based) if opencv-contrib
    is not installed."""
    mean_guide = cv2.boxFilter(guide, cv2.CV_64F, (radius, radius))
    mean_src = cv2.boxFilter(src, cv2.CV_64F, (radius, radius))
    mean_guide_src = cv2.boxFilter(guide * src, cv2.CV_64F, (radius, radius))
    cov_guide_src = mean_guide_src - mean_guide * mean_src

    mean_guide_sq = cv2.boxFilter(guide * guide, cv2.CV_64F, (radius, radius))
    var_guide = mean_guide_sq - mean_guide * mean_guide

    a = cov_guide_src / (var_guide + eps)
    b = mean_src - a * mean_guide

    mean_a = cv2.boxFilter(a, cv2.CV_64F, (radius, radius))
    mean_b = cv2.boxFilter(b, cv2.CV_64F, (radius, radius))

    return mean_a * guide + mean_b


def recover_scene_radiance(image, A, transmission, t0=0.1):
    """Invert the haze model to recover J:
    J = (I - A) / max(t, t0) + A
    t0 puts a floor on the transmission to avoid amplifying noise
    in regions that are very heavily hazed.
    """
    t = np.clip(transmission, t0, 1.0)
    J = np.empty_like(image)
    for c in range(3):
        J[:, :, c] = (image[:, :, c] - A[c]) / t + A[c]
    return np.clip(J, 0, 1)


def dehaze(image_bgr, patch_size=15, omega=0.95, t0=0.1,
           guided_radius=40, guided_eps=1e-3):
    """Full Dark Channel Prior dehazing pipeline.
    image_bgr: HxWx3 uint8 BGR image (as read by cv2.imread)
    Returns: HxWx3 uint8 BGR dehazed image
    """
    image = image_bgr.astype(np.float64) / 255.0

    dark_channel = get_dark_channel(image, patch_size)
    A = estimate_atmospheric_light(image, dark_channel)
    raw_transmission = estimate_transmission(image, A, omega, patch_size)
    refined_transmission = guided_filter_refine(image, raw_transmission,
                                                 guided_radius, guided_eps)
    recovered = recover_scene_radiance(image, A, refined_transmission, t0)

    return (recovered * 255).astype(np.uint8)


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python dark_channel_prior.py <input_image> <output_image>")
        sys.exit(1)

    img = cv2.imread(sys.argv[1])
    if img is None:
        raise FileNotFoundError(f"Could not read {sys.argv[1]}")

    result = dehaze(img)
    cv2.imwrite(sys.argv[2], result)
    print(f"Saved dehazed image to {sys.argv[2]}")
