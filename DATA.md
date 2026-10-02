# Data description

## Original thermal sequence

The original file, `1763233716_556705-NADIR-MERGED-RECTILINEAR.tiff`, contains 389 frames. Each frame is 512 pixels high by 640 pixels wide and has `float32` pixel values. This is the quantitative thermal source. The precise radiometric interpretation of those values should be confirmed from the camera documentation before treating them as temperature in a named physical unit.

The original TIFF is available from [Elphel's shared Google Drive file](https://drive.google.com/file/d/1nY5cdCgdhaYS_FOkD7Ob4g40M2Hmy3IY/view?usp=sharing). The locally inspected copy has this SHA-256 digest; verify that the Drive download matches it:

```text
71f55d32654d0b10a8c819b0a4a6dfa3dd4795eede329fd28bb881fc54273a63
```

## Reconstruction-oriented PNG sequence

`data/images_png_highpass/` contains `image_0000.png` through `image_0388.png`, plus `normalization.json`. The numeric suffix is the zero-based frame index in the source TIFF. Each PNG is a 512 × 640, 8-bit, single-channel image.

The processing implemented in [`scripts/exifsplitter_highpass.py`](scripts/exifsplitter_highpass.py) is:

1. For each floating-point frame `I`, compute `H = I - GaussianBlur(I, sigma=10 pixels)`.
2. Estimate one common amplitude `A` as the 99th percentile of sampled `abs(H)` values across the entire sequence.
3. Clip each residual to `[-A, A]`, map it to 0–255 with zero near middle gray, and save it as a lossless grayscale PNG.

The exact measured amplitude and parameters are in `normalization.json`. PNG brightness is **not** a temperature measurement; the transformation deliberately emphasizes local structure for image matching.

## Camera metadata

`data/1763233716_556705-INTERFRAME.corr-xml` is the original camera metadata file. Its `EYESIS_DCT_AUX.scenes_*` entries contain six numerical values. The first three have been interpreted by the project team as local-XYZ positions in meters, not GPS latitude/longitude. The physical point represented by those positions (camera optical center versus another sensor or platform reference point), the complete orientation convention, and the uncertainty have not yet been verified.

The original image extraction and trajectory comparison workflows associate image index `n` with the `n`th timestamp-sorted `scenes_*` record, excluding other XML entry types. Anyone using these records as pose priors should validate that association and the coordinate convention for their method. PNG preprocessing does not read the XML or embed pose metadata in the PNGs.

XML SHA-256:

```text
dec3cafef5733fc11e80de25d36375a8fa1e58b18cdb74d5f08b29c025d254c9
```

The TIFF, PNG sequence, and XML metadata are provided by [Elphel](https://www.elphel.com/) for public download. Their reuse terms have not been specified; see [DATA_LICENSE.md](DATA_LICENSE.md).

## Scope and limitations

- The raw TIFF, reconstruction PNGs, and XML are separate data products. Do not infer physical temperature from PNG grayscale values.
- The XML positions are not ground-truth 3D scene points. They can be used as optional camera-motion information after validating their semantics.
- No independent surveyed point cloud, metric surface model, or per-pixel depth ground truth is included at present.
