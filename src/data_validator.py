import logging
import pandas as pd

logger = logging.getLogger(__name__)

def validate_dataframe(df, required_columns, numeric_columns):
    """Validate the DataFrame and return valid data."""
    missing = [c for c in required_columns if c not in df.columns]
    if missing:
        logger.error(f"Missing required columns: {missing}")
        raise ValueError(f"Missing required columns: {missing}")

    rows_before = len(df)

    for col in numeric_columns:
        invalid_rows = []
        for i, value in df[col].items():
            if pd.notna(value):
                try:
                    float(value)
                except ValueError:
                    invalid_rows.append(i)

        if invalid_rows:
            logger.warning(
                f"Removed {len(invalid_rows)} rows with invalid numeric values in {col}"
            )
        df = df.drop(index=invalid_rows).copy()

        # convert to a numeric data type
        df[col] = pd.to_numeric(df[col])

    logger.debug(f"Validation: {rows_before} -> {len(df)} rows")
    return df