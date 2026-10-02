"""Export a multi-page thermal TIFF as globally normalized pure high-pass PNGs.

For every input frame I, this script computes:

    H = I - GaussianBlur(I, sigma)

It then maps every frame with the same zero-centred mapping:

    H = -A -> 0 (black),  H = 0 -> 128 (middle grey),  H = +A -> 255 (white)

where A is one robust percentile of |H| calculated across the full TIFF. The
script intentionally does not read XML, read EXIF, or write EXIF metadata.
The original float TIFF remains unchanged.
"""

import argparse
import json
from pathlib import Path

import numpy as np
from PIL import Image
from scipy.ndimage import gaussian_filter
import tifffile


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("tiff_path", type=Path, help="Input multi-page thermal TIFF.")
    parser.add_argument(
        "--output_dir",
        type=Path,
        default=Path("images_png_highpass"),
        help="New output directory for image_0000.png etc. (default: images_png_highpass).",
    )
    parser.add_argument(
        "--sigma",
        type=float,
        default=10.0,
        help="Gaussian blur sigma in pixels (default: 10.0).",
    )
    parser.add_argument(
        "--clip_percentile",
        type=float,
        default=99.0,
        help="Global percentile of |high-pass value| used as A (default: 99.0).",
    )
    parser.add_argument(
        "--sample_stride",
        type=int,
        default=16,
        help="Use every Nth pixel while estimating A (default: 16).",
    )
    return parser.parse_args()


def validate_args(args):
    if not args.tiff_path.is_file():
        raise FileNotFoundError(f"TIFF not found: {args.tiff_path}")
    if args.sigma <= 0:
        raise ValueError("sigma must be positive.")
    if not 0 < args.clip_percentile <= 100:
        raise ValueError("clip_percentile must be in (0, 100].")
    if args.sample_stride < 1:
        raise ValueError("sample_stride must be at least 1.")
    if args.output_dir.exists() and any(args.output_dir.iterdir()):
        raise FileExistsError(
            f"Output directory is not empty: {args.output_dir}. "
            "Choose a new --output_dir to avoid mixing image sets."
        )


def high_pass(frame, sigma):
    """Return I - GaussianBlur(I), preserving invalid input pixels as NaN."""
    values = np.asarray(frame, dtype=np.float32)
    if values.ndim != 2:
        raise ValueError(f"Expected a 2-D thermal frame, got shape {values.shape}.")

    valid = np.isfinite(values)
    if not np.any(valid):
        raise ValueError("Frame contains no finite thermal values.")

    # Gaussian filtering needs finite values. The median is used only to fill
    # invalid pixels temporarily; invalid pixels are restored to NaN afterward.
    median = np.median(values[valid])
    filled = np.where(valid, values, median)
    blurred = gaussian_filter(filled, sigma=sigma, mode="reflect")
    result = filled - blurred
    result[~valid] = np.nan
    return result


def estimate_amplitude(tiff_path, sigma, clip_percentile, sample_stride):
    """Estimate one shared, symmetric high-pass range A across all frames."""
    samples = []
    with tifffile.TiffFile(tiff_path) as tiff:
        if not tiff.pages:
            raise ValueError("TIFF has no image pages.")
        for frame_index, page in enumerate(tiff.pages):
            residual = high_pass(page.asarray(), sigma)
            sample = np.abs(residual.ravel()[::sample_stride])
            sample = sample[np.isfinite(sample)]
            if sample.size:
                samples.append(sample)
            print(f"  scanned frame {frame_index + 1}/{len(tiff.pages)}", end="\r")

    print()
    if not samples:
        raise ValueError("No finite high-pass values found in TIFF.")
    amplitude = float(np.percentile(np.concatenate(samples), clip_percentile))
    if not np.isfinite(amplitude) or amplitude <= 0:
        raise ValueError(f"Invalid high-pass amplitude A={amplitude}.")
    return amplitude


def residual_to_uint8(residual, amplitude):
    """Map one high-pass frame symmetrically: -A, 0, +A -> 0, 128, 255."""
    scaled = 127.5 + 127.5 * (residual / amplitude)
    scaled[~np.isfinite(scaled)] = 127.5
    return np.rint(np.clip(scaled, 0.0, 255.0)).astype(np.uint8)


def export_frames(tiff_path, output_dir, sigma, amplitude):
    output_dir.mkdir(parents=True, exist_ok=True)
    with tifffile.TiffFile(tiff_path) as tiff:
        frame_count = len(tiff.pages)
        for frame_index, page in enumerate(tiff.pages):
            residual = high_pass(page.asarray(), sigma)
            image = Image.fromarray(residual_to_uint8(residual, amplitude), mode="L")
            image.save(output_dir / f"image_{frame_index:04d}.png", format="PNG")
            print(f"  wrote frame {frame_index + 1}/{frame_count}", end="\r")
    print()
    return frame_count


def main():
    args = parse_args()
    validate_args(args)

    print("Pass 1/2: computing one global, symmetric high-pass normalization range...")
    amplitude = estimate_amplitude(
        args.tiff_path, args.sigma, args.clip_percentile, args.sample_stride
    )
    print(
        f"Shared mapping: -{amplitude:.6f} -> 0, 0 -> 128, "
        f"+{amplitude:.6f} -> 255"
    )

    print("Pass 2/2: exporting 8-bit grayscale pure high-pass PNG frames...")
    frame_count = export_frames(args.tiff_path, args.output_dir, args.sigma, amplitude)

    manifest = {
        "source_tiff": str(args.tiff_path),
        "frame_count": frame_count,
        "output_format": "8-bit grayscale PNG",
        "processing": {
            "method": "pure high-pass: I - GaussianBlur(I, sigma)",
            "gaussian_sigma_pixels": args.sigma,
            "blur_border_mode": "reflect",
            "normalization": "one global symmetric mapping across all frames",
            "clip_percentile_of_absolute_high_pass": args.clip_percentile,
            "sample_stride": args.sample_stride,
            "high_pass_value_at_gray_0": -amplitude,
            "high_pass_value_at_gray_128": 0.0,
            "high_pass_value_at_gray_255": amplitude,
        },
        "metadata": "No XML or EXIF metadata was read or written.",
    }
    manifest_path = args.output_dir / "normalization.json"
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    print(f"Done: {frame_count} frames written to {args.output_dir}")
    print(f"Processing record written to {manifest_path}")


if __name__ == "__main__":
    main()
