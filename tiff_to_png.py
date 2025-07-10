import argparse
from pathlib import Path
from PIL import Image
from icecream import ic


def convert_tif_to_png(input_dir: Path, output_dir: Path):
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    tif_files = list(input_dir.glob("*.tif")) + list(input_dir.glob("*.tiff"))

    if not tif_files:
        ic("No .tif or .tiff files found in the input directory.")
        return

    for tif_path in tif_files:
        png_path = output_dir / (tif_path.stem + ".png")
        if png_path.exists():
            ic("Skipping existing file", png_path)
            continue

        try:
            with Image.open(tif_path) as img:
                img = img.convert("RGB")
                img.save(png_path, "PNG")
                ic("Converted:", tif_path.name, "->", png_path.name)
        except Exception as e:
            ic("Error converting", tif_path.name, e)


def main():
    parser = argparse.ArgumentParser(
        description="Convert a directory of .tif files to .png"
    )
    parser.add_argument(
        "--input_dir",
        "-i",
        default="./input_tifs",
        type=str,
        help="Path to directory with .tif files (default: ./input_tifs)",
    )
    parser.add_argument(
        "--output_dir",
        "-o",
        default="./output_pngs",
        type=str,
        help="Path to output directory for .png files (default: ./output_pngs)",
    )
    args = parser.parse_args()

    convert_tif_to_png(args.input_dir, args.output_dir)


if __name__ == "__main__":
    main()
