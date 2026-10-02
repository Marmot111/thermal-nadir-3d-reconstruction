# Thermal Nadir UAV Sequence for 3D Reconstruction

This repository shares a 389-frame thermal nadir sequence acquired by a UAV carrying an LWIR-16, sixteen-lens camera. We invite reproducible methods that improve reconstruction of the observed water-tower scene, terrain, and vegetation from thermal imagery.

Our current COLMAP reconstruction provides a useful baseline, but its geometry is not yet accurate enough for our downstream research. There is no independently surveyed 3D ground-truth model in this release, so this is an open research problem rather than a ranked benchmark.

## Research question

Given the thermal sequence and, optionally, the camera metadata, can you reconstruct a more complete and geometrically consistent 3D scene than the supplied COLMAP baseline? We welcome approaches that use thermal-specific feature extraction, multi-view stereo, pose priors, learned depth, sensor calibration, or other methods. Please state precisely which inputs you use.

## Data at a glance

| Item | Description |
| --- | --- |
| Raw thermal sequence | 389 frames, 512 × 640 pixels, 32-bit floating-point TIFF; [download from Elphel's shared Google Drive file](https://drive.google.com/file/d/1nY5cdCgdhaYS_FOkD7Ob4g40M2Hmy3IY/view?usp=sharing) |
| Reconstruction-oriented sequence | 389 lossless, 8-bit, single-channel PNG frames in `data/images_png_highpass/` |
| Camera metadata | Original `data/1763233716_556705-INTERFRAME.corr-xml` file, including local-XYZ scene records |
| Preprocessing | [`scripts/exifsplitter_highpass.py`](scripts/exifsplitter_highpass.py); frame-wise Gaussian high-pass filtering followed by one sequence-wide symmetric intensity mapping |
| Existing reconstruction | COLMAP feature matching, sparse SfM, dense MVS, and point fusion; see [BASELINE.md](BASELINE.md) |

The PNGs are intended for reconstruction. Use the original floating-point TIFF for quantitative thermal values. Details on frame ordering, units, and metadata appear in [DATA.md](DATA.md).

## License and attribution

The original TIFF, the PNG sequence, and the XML camera metadata are provided by [Elphel](https://www.elphel.com/) and are made publicly available for download with Elphel's permission. Elphel is credited as the data owner. No reuse license, including CC BY 4.0, has been specified for these data; see [DATA_LICENSE.md](DATA_LICENSE.md). Public availability does not by itself grant permission to redistribute or adapt the data.

The preprocessing script is included for reproducibility; no separate reuse license has been specified for the code. The team's milestone report is not included in this release.

## Get the data

1. Clone or download this repository for the PNG sequence, XML metadata, and preprocessing script.
2. Download the original TIFF from [this Google Drive file](https://drive.google.com/file/d/1nY5cdCgdhaYS_FOkD7Ob4g40M2Hmy3IY/view?usp=sharing). Its original filename is `1763233716_556705-NADIR-MERGED-RECTILINEAR.tiff`. The raw TIFF is too large for an ordinary Git commit.
3. Verify the raw TIFF against the SHA-256 digest in [DATA.md](DATA.md).

## Reproduce the PNG preprocessing

The provided PNGs are already generated. To regenerate them from the raw TIFF, install the packages in `requirements.txt` and run:

```bash
python scripts/exifsplitter_highpass.py 1763233716_556705-NADIR-MERGED-RECTILINEAR.tiff --output_dir regenerated_images_png_highpass
```

The script uses a Gaussian blur with `sigma=10` pixels and computes the 99th percentile of the absolute high-pass residual, sampled across all frames, for one shared mapping. The parameters and transformation are documented in [DATA.md](DATA.md), and the measured mapping is recorded in `data/images_png_highpass/normalization.json`. The original TIFF is not modified.

## Existing baseline and evaluation

[BASELINE.md](BASELINE.md) records the processing approach and its limitations. The existing COLMAP reconstruction does **not** impose the XML-recorded positions as pose constraints. Contributors are free to use those records, but should describe the coordinate convention and how they associate records with frames.

Because this release does not include an independent 3D ground truth, please report the evidence behind any improvement claim: registration coverage, reprojection or consistency measures, views of the resulting point cloud or mesh, rendered-versus-original image comparisons, and failure regions. A lower reprojection error alone does not establish more accurate 3D geometry.

Please use GitHub Issues for method questions and Issues or pull requests for reproducible results. See [CONTRIBUTING.md](CONTRIBUTING.md) for the information that makes a result comparable.

## Release notes

The Google Drive file opens without a Google login. No milestone report PDF is included in this repository.
