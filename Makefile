DEFAULT_GOAL: run

run:
	python3 chipper.py --input-dir ../segmine/ingestion-worker/tmp/ --size 1280 --format tif --output-dir output/tif_chips

.PHONY: run
