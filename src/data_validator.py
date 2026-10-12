import logging
import pandas as pd

logger = logging.getLogger(__name__)

def validate_dataframe(df, required_columns, numeric_columns):
    """Validate the DataFrame and return valid data.
    required_columns: a list of column names that must exist.
    numeric_columns: a list of column names whose values should be numeric.
    """
    df_valid = df.copy()
    rows_before = len(df_valid)

    for col in required_columns:
        if col not in df_valid.columns:
            logger.error(f"Missing required column: {col}")
            raise ValueError(f"Missing required column: {col}")

    for col in numeric_columns:
        if col not in df_valid.columns:
            logger.warning(f"Numeric column not found, skipping: {col}")
            continue

        invalid_rows = []
        for i, value in df_valid[col].items():
            if pd.notna(value):
                try:
                    float(value)
                except (ValueError, TypeError):
                    logger.warning(
                        f"Invalid numeric value {value!r} in column '{col}' at row {i}"
                    )
                    invalid_rows.append(i)

        if invalid_rows:
            df_valid = df_valid.drop(index=invalid_rows)

        # Convert to a numeric data type
        df_valid[col] = pd.to_numeric(df_valid[col])

    rows_after = len(df_valid)
    logger.debug(
        f"Validation complete: {rows_after} valid rows, "
        f"{rows_before - rows_after} removed"
    )

    return df_valid