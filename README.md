# Image Dehazing and Rain Streak Removal using DIP Techniques

Mini project combining classical Digital Image Processing methods with
lightweight deep learning for two restoration tasks: haze removal and
rain streak removal.

## Repo structure

```
.
├── README.md
├── LICENSE
├── requirements.txt
├── .gitignore
├── app.py                          # Streamlit demo (all modules)
├── dehazing/
│   ├── __init__.py
│   └── dark_channel_prior.py       # classical DCP dehazing
├── deraining/
│   └── __init__.py                 # rain streak removal (in progress)
└── evaluation/
    ├── __init__.py
    └── evaluate_sots.py            # PSNR/SSIM evaluation on SOTS
```

As AOD-Net (dehazing) and the CNN-based deraining module get added, they'll
live in `dehazing/` and `deraining/` respectively, alongside the classical
implementations — so the repo doubles as a classical-vs-ML comparison.

## 1. Setup

```bash
git clone https://github.com/<your-username>/<repo-name>.git
cd <repo-name>
pip install -r requirements.txt
```

`opencv-contrib-python` gives you `cv2.ximgproc.guidedFilter` for fast,
accurate transmission-map refinement. If it's not available, the code
automatically falls back to a manual guided filter implementation.

## 2. Dataset layout

Download SOTS from the [RESIDE benchmark](https://sites.google.com/view/reside-dehaze-datasets)
and place it outside the repo (it's excluded via `.gitignore` since it's
too large for git). Point `--root` at it:

```
SOTS/
    indoor/
        hazy/   1400_1.png, 1400_2.png, ...
        gt/     1400.png, ...
    outdoor/
        hazy/   0001_0.8_0.2.jpg, ...
        gt/     0001.png, ...
```

If your download uses different subfolder names, rename them to `hazy` /
`gt`, or edit `hazy_dir` / `gt_dir` in `evaluation/evaluate_sots.py`.

## 3. Try it on a single image

```bash
python dehazing/dark_channel_prior.py path/to/hazy_image.png path/to/output_dehazed.png
```

## 4. Run the full SOTS evaluation

```bash
# Quick sanity check on 20 images
python evaluation/evaluate_sots.py --root /path/to/SOTS --subset indoor --limit 20

# Full run, saving side-by-side comparison images
python evaluation/evaluate_sots.py --root /path/to/SOTS --subset indoor \
    --save_samples_dir samples_indoor/ --csv_out indoor_results.csv

python evaluation/evaluate_sots.py --root /path/to/SOTS --subset outdoor \
    --save_samples_dir samples_outdoor/ --csv_out outdoor_results.csv
```

This prints per-image PSNR/SSIM, an overall summary, and saves a CSV you can
drop straight into your project report (tables, bar charts, etc.).

## 5. What to expect

Dark Channel Prior is a strong classical baseline but it's known to
underperform on SOTS indoor (dense, uniform haze) compared to outdoor
scenes (more depth variation, which DCP relies on). Typical published DCP
numbers on SOTS are roughly:

| Subset  | PSNR (approx.) | SSIM (approx.) |
|---------|----------------|-----------------|
| Indoor  | ~16-18 dB      | ~0.75-0.80      |
| Outdoor | ~18-21 dB      | ~0.80-0.85      |

Deep learning methods like AOD-Net typically push indoor PSNR into the
19-21 dB range and beyond — this gap is exactly the comparison your
"classical vs. light ML" project narrative should highlight.

## 6. Known failure modes to discuss in your report

- **Sky/bright regions:** DCP tends to over-darken large sky areas since the
  dark-channel assumption breaks down there. Worth showing a failure example.
- **Color shift:** slight color casts can appear if atmospheric light
  estimation picks a non-neutral bright pixel (e.g. a white object instead
  of true sky/haze).
- **Halo artifacts** around depth discontinuities if the transmission map
  isn't well refined — this is exactly why the guided filter step matters;
  try comparing with/without it for your report.

## 7. Interactive demo (Streamlit)

Run the app locally from the repo root:

```bash
streamlit run app.py
```

This opens a browser tab where you can upload a hazy image, tweak the DCP
parameters with sliders, and see the dehazed result live — much better for
a viva/demo than static screenshots. If you upload a matching ground-truth
image too, it'll show PSNR/SSIM on the spot. Once the deraining module is
added, it'll get its own tab in the same app.

## 8. Putting the project on GitHub

From the repo root:

```bash
git init
git add .
git commit -m "Initial commit: DCP dehazing baseline + Streamlit demo"
git branch -M main
git remote add origin https://github.com/<your-username>/<repo-name>.git
git push -u origin main
```

The included `.gitignore` keeps the repo lightweight by excluding the SOTS
dataset, virtual environments, and any trained model weights — don't commit
the dataset itself, just document how to download it (link the RESIDE
dataset page above) so anyone cloning the repo can reproduce your results.

Everything for this project — dehazing, deraining, evaluation, demo app,
and eventually your report — stays in this single repo, so it's the one
link you need to share for submission or your GitHub profile.

## 9. Deploying the Streamlit app (free, no server needed)

1. Push your repo to GitHub (step 8).
2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with
   GitHub.
3. Click "New app", pick your repo/branch, and set the main file path to
   `app.py`.
4. Deploy — you'll get a public URL you can drop straight into your project
   report or share with your evaluator.

Since AOD-Net will need a trained weights file, when you get to that stage
keep the `.pth` file under GitHub's 100 MB limit or use Git LFS; otherwise
host the weights elsewhere (e.g., a GitHub release asset) and download them
at app startup.

## 10. Roadmap

- [x] Classical dehazing — Dark Channel Prior + guided filter refinement
- [x] SOTS evaluation pipeline (PSNR/SSIM)
- [x] Streamlit demo app
- [ ] Classical rain streak removal (frequency decomposition)
- [ ] AOD-Net (lightweight CNN dehazing) trained on ITS/OTS
- [ ] Lightweight CNN deraining module
- [ ] Combined dehazing + deraining pipeline
- [ ] Project report
