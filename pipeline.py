"""
Data Processing Pipeline - CLI Template
DS 3500 - MP1
Usage:
python pipeline.py --input data.csv --output clean.csv
python pipeline.py --input data.csv --output results.json --format
json --verbose
"""
import argparse
import logging
import sys
from pathlib import Path

logger = logging.getLogger(__name__)

def setup_logging(verbose=False):
    logging.basicConfig(level=logging.DEBUG if verbose else logging.INFO,
                        format='%(asctime)s %(levelname)s %(message)s', datefmt='%H:%M:%S')

def parse_arguments():
    p = argparse.ArgumentParser()
    p.add_argument('-i', '--input', required=True)
    p.add_argument('-o', '--output', required=True)
    p.add_argument('--format', default='csv', choices=['csv', 'json'])
    p.add_argument('-v', '--verbose', action='store_true')
    return p.parse_args()

def validate_input(filepath):
    if Path(filepath).is_file():
        logger.info(f"Input file validated: {filepath}")
        return True
    logger.error(f"Input file not found: {filepath}")
    return False

def main():
    args = parse_arguments()
    setup_logging(args.verbose)
    logger.debug(f"Arguments parsed: input={args.input}, output={args.output}, format={args.format}")
    if not validate_input(args.input): sys.exit(1)

if __name__ == "__main__":
    main()