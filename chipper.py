import os
import argparse
import rasterio
from rasterio.windows import Window
from PIL import Image
import numpy as np
from tqdm import tqdm


def chip_image(input_path, chip_size, output_dir, output_format, bands=None):
    os.makedirs(output_dir, exist_ok=True)

    with rasterio.open(input_path) as src:
        img_width = src.width
        img_height = src.height
        crs = src.crs

        n_chips_x = (img_width + chip_size - 1) // chip_size
        n_chips_y = (img_height + chip_size - 1) // chip_size
        total_chips = n_chips_x * n_chips_y

        chip_id = 0
        saved_chips = 0

        with tqdm(
            total=total_chips, desc=f"🔨 Chipping {os.path.basename(input_path)}"
        ) as pbar:
            for top in range(0, img_height, chip_size):
                for left in range(0, img_width, chip_size):
                    window = Window(left, top, chip_size, chip_size)
                    transform_chip = src.window_transform(window)

                    chip = src.read(indexes=bands, window=window)

                    if np.all(chip == 0):
                        pbar.update(1)
                        continue

                    w = min(chip_size, img_width - left)
                    h = min(chip_size, img_height - top)

                    chip_filename_base = os.path.join(
                        output_dir,
                        f"{os.path.splitext(os.path.basename(input_path))[0]}_chip_{chip_id}",
                    )

                    if output_format == "tif":
                        chip_filename = f"{chip_filename_base}.tif"
                        with rasterio.open(
                            chip_filename,
                            "w",
                            driver="GTiff",
                            height=h,
                            width=w,
                            count=len(bands) if bands else src.count,
                            dtype=src.dtypes[0],
                            crs=crs,
                            transform=transform_chip,
                        ) as dst:
                            dst.write(chip)

                    elif output_format == "png":
                        chip_filename = f"{chip_filename_base}.png"

                        chip_rgb = np.moveaxis(chip, 0, -1)  # Channels last

                        if chip_rgb.dtype != np.uint8:
                            chip_rgb = np.nan_to_num(
                                chip_rgb, nan=0.0, posinf=255.0, neginf=0.0
                            )

                            if np.max(chip_rgb) <= 1.0:
                                chip_rgb = (chip_rgb * 255).astype(np.uint8)
                            else:
                                chip_rgb = np.clip(chip_rgb, 0, 255).astype(np.uint8)

                        img = Image.fromarray(chip_rgb)
                        img.save(chip_filename)

                    else:
                        raise ValueError("Unsupported format. Choose 'tif' or 'png'.")

                    chip_id += 1
                    saved_chips += 1
                    pbar.update(1)

    print(f"\n✅ Done! {saved_chips} non-empty chips saved from '{input_path}'.")


def main():
    parser = argparse.ArgumentParser(
        description="Chipper: Tile large geospatial rasters into smaller chips (with spatial metadata)."
    )
    parser.add_argument("-i", "--input", type=str, help="Path to input raster")
    parser.add_argument(
        "-d", "--input-dir", type=str, help="Path to a directory of rasters"
    )
    parser.add_argument(
        "-s", "--size", type=int, default=640, help="Chip size in pixels (default: 640)"
    )
    parser.add_argument(
        "-f",
        "--format",
        type=str,
        choices=["tif", "png"],
        default="tif",
        help="Output format (tif or png)",
    )
    parser.add_argument(
        "-o",
        "--output-dir",
        type=str,
        default="chips",
        help="Directory to save output chips (default: ./chips)",
    )
    parser.add_argument(
        "-b",
        "--bands",
        type=str,
        default=None,
        help="Optional: comma-separated band indexes to use, e.g., '4,3,2'. If not set, all bands are used.",
    )

    args = parser.parse_args()

    if not args.input and not args.input_dir:
        parser.error(
            "❌ You must specify either --input (single file) or --input-dir (directory)"
        )

    # Parse bands if provided
    if args.bands:
        bands = list(map(int, args.bands.split(",")))
    else:
        bands = None

    # Process a single file
    if args.input:
        chip_image(args.input, args.size, args.output_dir, args.format, bands)

    # Process a directory
    if args.input_dir:
        for filename in os.listdir(args.input_dir):
            if filename.lower().endswith(
                (".tif", ".tiff")
            ):  # Only process raster files
                input_path = os.path.join(args.input_dir, filename)
                chip_image(input_path, args.size, args.output_dir, args.format, bands)


if __name__ == "__main__":
    main()
