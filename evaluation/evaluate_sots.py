"""
Evaluate Dark Channel Prior dehazing on the SOTS dataset (RESIDE benchmark).

Expected folder structure (standard SOTS layout):
    SOTS/
        indoor/
            hazy/   *.png   (e.g., 1400_1.png, 1400_2.png ...)
            gt/     *.png   (e.g., 1400.png)
        outdoor/
            hazy/   *.jpg   (e.g., 0001_0.8_0.2.jpg)
            gt/     *.png   (e.g., 0001.png)

If your extracted folder uses different subfolder names (some releases use
"nyuhaze500"/"clear" for indoor, or "hazy"/"clear" for outdoor), just rename
them to hazy/gt, or edit hazy_dir / gt_dir below.

Usage:
    python evaluate_sots.py --root /path/to/SOTS --subset indoor --limit 50
    python evaluate_sots.py --root /path/to/SOTS --subset outdoor --save_samples_dir samples/
"""

import argparse
import glob
import os

import cv2
import numpy as np
import pandas as pd
from skimage.metrics import peak_signal_noise_ratio as psnr
from skimage.metrics import structural_similarity as ssim

import os
import sys

# Allow running this file directly (python evaluation/evaluate_sots.py)
# as well as as a module (python -m evaluation.evaluate_sots) by ensuring
# the repo root is on sys.path either way.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from dehazing.dark_channel_prior import dehaze


def match_gt_filename(hazy_filename):
    """SOTS hazy filenames encode the ground-truth id before the first
    underscore, e.g. '1400_1.png' -> '1400', '0001_0.8_0.2.jpg' -> '0001'."""
    base = os.path.splitext(os.path.basename(hazy_filename))[0]
    gt_id = base.split("_")[0]
    return gt_id


def find_gt_path(gt_dir, gt_id):
    for ext in (".png", ".jpg", ".jpeg", ".bmp"):
        candidate = os.path.join(gt_dir, gt_id + ext)
        if os.path.exists(candidate):
            return candidate
    return None


def evaluate(root, subset, limit=None, save_samples_dir=None):
    hazy_dir = os.path.join(root, subset, "hazy")
    gt_dir = os.path.join(root, subset, "gt")

    hazy_paths = sorted(glob.glob(os.path.join(hazy_dir, "*")))
    if not hazy_paths:
        raise FileNotFoundError(
            f"No images found in {hazy_dir}. Check --root and folder names."
        )
    if limit:
        hazy_paths = hazy_paths[:limit]

    if save_samples_dir:
        os.makedirs(save_samples_dir, exist_ok=True)

    records = []
    for hazy_path in hazy_paths:
        gt_id = match_gt_filename(hazy_path)
        gt_path = find_gt_path(gt_dir, gt_id)
        if gt_path is None:
            print(f"[skip] no ground truth found for {hazy_path}")
            continue

        hazy_img = cv2.imread(hazy_path)
        gt_img = cv2.imread(gt_path)
        if hazy_img is None or gt_img is None:
            print(f"[skip] could not read {hazy_path} or {gt_path}")
            continue

        if hazy_img.shape != gt_img.shape:
            gt_img = cv2.resize(gt_img, (hazy_img.shape[1], hazy_img.shape[0]))

        dehazed_img = dehaze(hazy_img)

        p = psnr(gt_img, dehazed_img, data_range=255)
        s = ssim(gt_img, dehazed_img, data_range=255, channel_axis=2)

        records.append({
            "hazy_file": os.path.basename(hazy_path),
            "gt_file": os.path.basename(gt_path),
            "psnr": p,
            "ssim": s,
        })

        if save_samples_dir:
            stacked = np.hstack([hazy_img, dehazed_img, gt_img])
            out_name = os.path.splitext(os.path.basename(hazy_path))[0] + "_compare.png"
            cv2.imwrite(os.path.join(save_samples_dir, out_name), stacked)

        print(f"{os.path.basename(hazy_path):30s} PSNR={p:6.2f}  SSIM={s:.4f}")

    df = pd.DataFrame(records)
    if len(df):
        print("\n=== Summary ===")
        print(f"Images evaluated: {len(df)}")
        print(f"Mean PSNR: {df['psnr'].mean():.2f}")
        print(f"Mean SSIM: {df['ssim'].mean():.4f}")
    else:
        print("No image pairs were evaluated - check your dataset paths.")

    return df


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True, help="Path to SOTS root folder")
    parser.add_argument("--subset", choices=["indoor", "outdoor"], default="indoor")
    parser.add_argument("--limit", type=int, default=None,
                         help="Evaluate only the first N images (for quick testing)")
    parser.add_argument("--save_samples_dir", default=None,
                         help="If set, saves hazy|dehazed|gt comparison images here")
    parser.add_argument("--csv_out", default="sots_results.csv")
    args = parser.parse_args()

    df = evaluate(args.root, args.subset, args.limit, args.save_samples_dir)
    if len(df):
        df.to_csv(args.csv_out, index=False)
        print(f"\nSaved detailed results to {args.csv_out}")
