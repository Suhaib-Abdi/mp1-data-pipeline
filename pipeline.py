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
from data_loaders import load_data
from data_processor import process_data, create_cleaning_report

logger = logging.getLogger(__name__)



def parse_arguments():
    p = argparse.ArgumentParser()
    p.add_argument('-i', '--input', required=True)
    p.add_argument('-c', '--config', required=True)
    p.add_argument('-o', '--output', required=True)
    p.add_argument('-v', '--verbose', action='store_true')
    return p.parse_args()



def main():
    args = parse_arguments()
    setup_logging(args.verbose)
    
    if not validate_input(args.input) or not validate_input(args.config):
        sys.exit(1)
        
    try:
        df_before = load_data(args.input)
        config = load_data(args.config)
    except ValueError:
        sys.exit(1)
        
    try:
        df_after = process_data(df_before, config)
    except ValueError:
        sys.exit(1)

    # Function 5 is called here
    report = create_cleaning_report(df_before, df_after)
    print(report)
    
    logger.info(f"Processing complete: {len(df_before)} -> {len(df_after)} rows")
    
    df_after.to_csv(args.output, index=False)
    logger.info(f"Saved cleaned data to {args.output}")

if __name__ == "__main__":
    main()