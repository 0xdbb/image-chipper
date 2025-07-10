# Chipper

Chipper is a command-line Python tool for “chipping” (tiling) large geospatial raster images (e.g., GeoTIFF) into smaller, uniformly sized image chips. It preserves spatial and georeferencing metadata—ideal for workflows like training object detectors (e.g., YOLO) on satellite imagery.

## Features
- Splits a single geospatial raster into fixed-size tiles (chips).
- Preserves geospatial metadata in each output chip (GeoTIFF or image + metadata sidecar).
- Configurable tile size (default: 640×640 pixels, a common YOLO resolution).
- Customizable output directory and file format.
- Simple CLI with sensible defaults and built-in help.

## Requirements
- Python 3.7 or higher
- rasterio
- Pillow

Dependencies can be installed via the provided `requirements.txt` or manually:
```bash
pip install -r requirements.txt
```

## Installation
1. Clone or download this repository:
   ```bash
   git clone https://github.com/yourusername/chipper.git
   cd chipper
   ```
2. (Optional) Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Linux/macOS
   venv\\Scripts\\activate    # Windows
   ```
3. Install dependencies (see Requirements).

## Usage
```bash
python chipper.py --input <INPUT_FILE> [--size <PIXELS>] [--format {tif,png}] [--output-dir <DIR>]
```
or 

```bash
make
```

### Arguments
- `-i` or`--input`       Path to the input raster (GeoTIFF, JPEG2000, etc.).
- `-s` or ` --size`        Width and height (pixels) of each output chip. Default: `640`.
- `-f` or ` --format`      Output image format: `tif` (GeoTIFF) or `png`. Default: `tif`.
- `-o` or ` --output-dir`  Directory to save output chips. Default: `./chips`.
- `-h` or ` --help`        Show help and exit.
- `-b` or ` --bands`        What bands to process (Optional)

### Examples
- Chip a large GeoTIFF into 640×640 GeoTIFF tiles:
  ```bash
  python chipper.py --input data/satellite.tif -output-dir output/chips
  ```
- Generate 512×512 PNG chips:
  ```bash
  python chipper.py --input data/satellite.tif -size 640 --bands 3,2,1  --format png --output-dir output/png_chips
  ```
