"""
Data Processing Pipeline - CLI Template
DS 3500 - MP1
"""
import argparse
import logging
import sys

from src import (
    create_cleaning_report,
    load_data,
    process_data,
    save_data,
    setup_logging,
    validate_dataframe,
    validate_input,
)

logger = logging.getLogger(__name__)


def parse_arguments():
    p = argparse.ArgumentParser(description="Data Processing Pipeline")
    p.add_argument('-i', '--input', required=True, help="Path to input data file")
    p.add_argument('-c', '--config', required=True, help="Path to configuration file")
    p.add_argument('-o', '--output', required=True, help="Path to output data file")
    p.add_argument('-v', '--verbose', action='store_true', help="Enable verbose debug logging")
    return p.parse_args()


def main():
    args = parse_arguments()

    # 1. Setup logging
    setup_logging(args.verbose)
    logger.debug(f"Arguments parsed: input={args.input}, config={args.config}, output={args.output}")

    # 2. Validate input file paths
    
    if not validate_input(args.input):
        sys.exit(1)
    if not validate_input(args.config):
        sys.exit(1)

    # 3. Load data and configuration
    try:
        df = load_data(args.input)
        config = load_data(args.config)
    except ValueError as e:
        logger.error(f"Loading failed: {e}")
        sys.exit(1)

    # 4. Extract validation configuration
    validation_config = config.get("validation", {})
    required_cols = validation_config.get("required_columns", [])
    numeric_cols = validation_config.get("numeric_columns", [])

    # 5. Validate DataFrame
    rows_before_val = len(df)
    try:
        df = validate_dataframe(df, required_cols, numeric_cols)
    except ValueError as e:
        logger.error(f"Validation failed: {e}")
        sys.exit(1)

    logger.info(f"Validation complete: {rows_before_val} -> {len(df)} rows")

    # 6. Process Data
    df_before_proc = df.copy()
    try:
        df = process_data(df, config)
    except ValueError as e:
        logger.error(f"Processing failed: {e}")
        sys.exit(1)
    logger.info(f"Processing complete: {len(df_before_proc)} -> {len(df)} rows")
    # 7. Create Report
    report = create_cleaning_report(df_before_proc, df)

    # 8. Save Cleaned Data
    save_data(df, args.output)
    logger.info(f"Saved cleaned data to {args.output}")

    # 9. Print cleaning report
    print("Cleaning report:")
    print(report)


if __name__ == "__main__":
    main()