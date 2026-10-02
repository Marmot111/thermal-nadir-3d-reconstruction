# Existing reconstruction baseline

The current baseline uses the high-pass PNG sequence in COLMAP. It performs feature extraction and image matching, sparse structure-from-motion (SfM), image undistortion, dense multi-view stereo (MVS), and point fusion. A mesh is subsequently produced for visual inspection.

## Image preparation

See [DATA.md](DATA.md) and [`scripts/exifsplitter_highpass.py`](scripts/exifsplitter_highpass.py). The high-pass PNGs are lossless 8-bit grayscale images produced with one shared normalization across all 389 frames. The original thermal TIFF remains available for alternative preprocessing.

## COLMAP setup

The inspected COLMAP project configuration for this baseline indicates a shared `SIMPLE_RADIAL` camera, SIFT feature extraction, GPU use, and geometric consistency for PatchMatch stereo. The project was run through COLMAP's GUI automatic reconstruction. The XML local-XYZ positions were retained separately for trajectory evaluation and were **not** used as position constraints by the incremental mapper.

The baseline is offered as a reference, not as a verified geometric ground truth. The full COLMAP database, dense stereo workspace, and milestone report are not bundled in this release. If the team chooses to distribute the baseline point cloud and sparse model, they can be attached to a future GitHub Release with exact configuration and version information.

## What to report when comparing methods

Please state the exact input imagery and preprocessing, whether XML positions or other priors were used, your camera model and calibration assumptions, and your software version and parameters. Provide the reconstructed point cloud or mesh and visualizations from comparable viewpoints. Explain how you assessed scene completeness and geometry, especially around the water tower, ground, and vegetation.

The project does not yet provide independent dense 3D ground truth, so no single scalar metric should be described as definitive reconstruction accuracy.
