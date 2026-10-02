# COLMAP reference workflow

The current baseline uses the example high-pass PNG sequence in COLMAP. It performs feature extraction and image matching, sparse structure-from-motion (SfM), image undistortion, dense multi-view stereo (MVS), and point fusion. The resulting dense point cloud is available as [baseline/fused.ply](baseline/fused.ply). A mesh was subsequently produced for visual inspection but is not included here.

## Image preparation

See [DATA.md](DATA.md) and [`scripts/exifsplitter_highpass.py`](scripts/exifsplitter_highpass.py). The high-pass PNGs are 8-bit grayscale images produced with one shared normalization across all 389 frames and saved using lossless PNG encoding. They represent one preprocessing approach, not a required input for new reconstructions. Start from the original thermal TIFF to try alternative methods.

## COLMAP setup

The COLMAP baseline used a shared `SIMPLE_RADIAL` camera model, SIFT feature extraction, GPU acceleration, and geometric consistency for PatchMatch stereo. It was run through COLMAP's GUI automatic reconstruction. The XML local-XYZ positions were retained separately for trajectory evaluation and were **not** used as position constraints by the incremental mapper.

The provided `fused.ply` contains 594,768 points. It is a binary little-endian PLY with XYZ positions, normals, and RGB vertex colors. Its SHA-256 digest is `d3f15ccc0803c151a9d1647e78a4af2b5f967b6ebe3b8184f18c3db9f675c847`.

## What to report when comparing methods

Please state the exact input imagery and preprocessing, whether XML positions or other priors were used, your camera model and calibration assumptions, and your software version and parameters. Provide the reconstructed point cloud or mesh and visualizations from comparable viewpoints. Explain how you assessed scene completeness and geometry, especially around the water tower, ground, and vegetation.
