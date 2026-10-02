# Thermal Nadir UAV Sequence for 3D Reconstruction

This repository shares a 389-frame thermal nadir sequence acquired by a UAV carrying an LWIR-16, sixteen-lens camera. The images show a water-tower scene, terrain, and vegetation.

Our COLMAP workflow provides a starting point, but its reconstructed geometry does not yet meet the needs of our downstream research. We welcome alternative approaches to this reconstruction problem.

## Research question

Starting from the raw thermal TIFF and, optionally, the camera metadata, can you reconstruct a more complete and geometrically consistent 3D scene than the COLMAP baseline provided here? We welcome approaches that use thermal-specific feature extraction, multi-view stereo, pose priors, learned depth, sensor calibration, or other methods. Please state precisely which inputs you use.

## Data at a glance

| Item | Description |
| --- | --- |
| Raw thermal sequence | 389 frames, 512 × 640 pixels, 32-bit floating-point TIFF; [download from Elphel's shared Google Drive file](https://drive.google.com/file/d/1nY5cdCgdhaYS_FOkD7Ob4g40M2Hmy3IY/view?usp=sharing) |
| Example preprocessed sequence | 389 8-bit, single-channel PNG frames in `data/images_png_highpass/` |
| Camera metadata | Original `data/1763233716_556705-INTERFRAME.corr-xml` file, including local-XYZ scene records |
| Preprocessing | [`scripts/exifsplitter_highpass.py`](scripts/exifsplitter_highpass.py); frame-wise Gaussian high-pass filtering followed by one sequence-wide symmetric intensity mapping |
| COLMAP reference workflow | Feature matching, sparse SfM, dense MVS, and point fusion; see [BASELINE.md](BASELINE.md) |
| Baseline dense point cloud | [baseline/fused.ply](baseline/fused.ply), reconstructed from the example PNG sequence |

I generated the PNG sequence using my own high-pass preprocessing method for the COLMAP baseline. The PNGs are an example, not a required input: please start from the raw TIFF and explore your own preprocessing and reconstruction methods. Use the original floating-point TIFF for quantitative thermal values. Details on frame ordering, units, and metadata appear in [DATA.md](DATA.md).

## Data and attribution

The original TIFF and XML camera metadata are provided by [Elphel](https://www.elphel.com/). The PNG sequence and baseline point cloud are derived from these data. You may download and modify the files for your work. Please credit Elphel as the data source.

You may also download and modify the preprocessing script to reproduce or adapt the PNG preparation. See [ATTRIBUTION.md](ATTRIBUTION.md) for a summary.

## Get the data

1. Clone or download this repository for the example PNG sequence, XML metadata, preprocessing script, and baseline point cloud.
2. Download the original TIFF from [this Google Drive file](https://drive.google.com/file/d/1nY5cdCgdhaYS_FOkD7Ob4g40M2Hmy3IY/view?usp=sharing). Its original filename is `1763233716_556705-NADIR-MERGED-RECTILINEAR.tiff`. The raw TIFF is too large for an ordinary Git commit.
3. Verify the raw TIFF against the SHA-256 digest in [DATA.md](DATA.md).

## Reproduce the PNG preprocessing

The example PNGs are already generated. To reproduce this particular preprocessing method from the raw TIFF, install the packages in `requirements.txt` and run:

```bash
python scripts/exifsplitter_highpass.py 1763233716_556705-NADIR-MERGED-RECTILINEAR.tiff --output_dir regenerated_images_png_highpass
```

The script uses a Gaussian blur with `sigma=10` pixels and computes the 99th percentile of the absolute high-pass residual, sampled across all frames, for one shared mapping. The parameters and transformation are documented in [DATA.md](DATA.md), and the measured mapping is recorded in `data/images_png_highpass/normalization.json`. The original TIFF is not modified.

## COLMAP workflow and evaluation

[BASELINE.md](BASELINE.md) describes the processing approach behind [the baseline point cloud](baseline/fused.ply). This COLMAP reconstruction does **not** impose the XML-recorded positions as pose constraints. Contributors are free to use those records, but should describe the coordinate convention and how they associate records with frames.

Because no independent 3D ground truth is available, please support improvement claims with registration coverage, reprojection or consistency measures, views of the resulting point cloud or mesh, rendered-versus-original image comparisons, and failure regions. A lower reprojection error alone does not establish more accurate 3D geometry.

Please use GitHub Issues for method questions and Issues or pull requests for reproducible results. See [CONTRIBUTING.md](CONTRIBUTING.md) for the information that makes a result comparable.
