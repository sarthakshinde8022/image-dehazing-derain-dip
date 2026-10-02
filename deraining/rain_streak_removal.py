"""
Classical Rain Streak Removal via Frequency Decomposition

Approach:
1. Decompose the rainy image into a smooth low-frequency base layer and
   a high-frequency detail layer using a Gaussian blur. Rain streaks,
   being thin and high-contrast, land almost entirely in the detail
   layer — a non-edge-preserving blur is used deliberately here, since
   an edge-preserving filter (e.g. a self-guided filter) would treat a
   streak's sharp edge as real structure worth keeping, leaking streak
   brightness into the base layer instead of isolating it.
2. Isolate thin, near-vertical streak patterns from the detail layer
   using a directional morphological white top-hat: eroding with a
   short, wide HORIZONTAL structuring element erases anything narrower
   than a chosen pixel width (the streaks), while wider genuine detail
   survives; the difference between the original detail and this result
   is exactly the streaks that got erased.
3. Subtract the isolated streak layer from the detail layer, then
   recombine with the base layer to reconstruct the derained image.

Model: O(x) = B(x) + R(x)
  O = observed rainy image, B = clean background, R = rain streak layer
"""

import cv2
import numpy as np


def decompose_frequency(image, radius=15, eps=1e-2):
    """Split an image into a low-frequency base layer and a high-frequency
    detail layer. image: HxWx3 float32 in [0, 1].

    Note: a self-guided filter (image guiding its own smoothing) was
    tried here first, but it treats rain streaks' sharp edges as real
    structure worth preserving, leaking streak brightness into the base
    layer instead of isolating it in the detail layer. A plain Gaussian
    blur has no such edge-preservation behavior, so it cleanly pushes
    thin high-frequency structures (including rain streaks) into the
    detail layer regardless of their local contrast. eps is kept as a
    parameter for interface consistency with the dehazing module but is
    unused here.
    """
    ksize = radius if radius % 2 == 1 else radius + 1
    base = cv2.GaussianBlur(image, (ksize, ksize), 0)
    detail = image.astype(np.float32) - base
    return base, detail


def isolate_rain_streaks(detail, max_streak_width=5):
    """Isolate thin, near-vertical streak patterns from the detail layer.

    Rain streaks are narrow in the horizontal direction (a few pixels
    wide), while genuine scene detail is typically wider. Eroding with a
    short, wide HORIZONTAL structuring element erases anything narrower
    than max_streak_width pixels; dilating then restores whatever
    survived. The difference between the original detail and this
    opened version is exactly what got erased — the thin streaks
    themselves. This is the classic morphological white top-hat,
    applied directionally to target near-vertical streaks specifically."""
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (max_streak_width, 1))
    rain_layer = np.zeros_like(detail)
    for c in range(3):
        opened = cv2.morphologyEx(detail[:, :, c], cv2.MORPH_OPEN, kernel)
        rain_layer[:, :, c] = detail[:, :, c] - opened
    return rain_layer


def derain(image_bgr, radius=15, eps=1e-2, max_streak_width=5):
    """Full classical rain streak removal pipeline.
    image_bgr: HxWx3 uint8 BGR image (as read by cv2.imread)
    Returns: HxWx3 uint8 BGR derained image
    """
    image = image_bgr.astype(np.float32) / 255.0

    base, detail = decompose_frequency(image, radius, eps)
    rain_layer = isolate_rain_streaks(detail, max_streak_width)
    clean_detail = detail - rain_layer
    result = base + clean_detail

    result = np.clip(result, 0, 1)
    return (result * 255).astype(np.uint8)


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python rain_streak_removal.py <input_image> <output_image>")
        sys.exit(1)

    img = cv2.imread(sys.argv[1])
    if img is None:
        raise FileNotFoundError(f"Could not read {sys.argv[1]}")

    result = derain(img)
    cv2.imwrite(sys.argv[2], result)
    print(f"Saved derained image to {sys.argv[2]}")
