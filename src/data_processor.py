import logging
import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)


def remove_duplicates(df):
    """Remove duplicate rows."""
    rows_before = len(df)
    df_cleaned = df.drop_duplicates()
    logger.debug(f"remove_duplicates: {rows_before} -> {len(df_cleaned)} rows")
    return df_cleaned


def handle_missing(df, axis="rows"):
    """Drop rows or columns containing missing values."""
    if axis not in ["rows", "columns"]:
        logger.error(f"Unsupported axis for handling missing values: {axis}")
        raise ValueError(f"Unsupported axis for handling missing values: {axis}")

    if axis == "rows":
        df_cleaned = df.dropna(axis=0)
        logger.debug(f"handle_missing: {len(df)} -> {len(df_cleaned)} rows")
    else:  # columns
        df_cleaned = df.dropna(axis=1)
        logger.debug(f"handle_missing: {df.shape[1]} -> {df_cleaned.shape[1]} columns")

    return df_cleaned


def remove_outliers(df, columns, method, threshold):
    """Remove outliers from the specified numeric columns."""
    #Cleans out crazy high or low numbers so extreme values don't wreck your analysis
    if method not in ['iqr', 'zscore']:
        logger.error(f"Unsupported outlier method: {method}")
        raise ValueError(f"Unsupported outlier method: {method}")

    df_cleaned = df.copy()

    for col in columns:
        if col not in df_cleaned.columns:
            logger.warning(f"Column not found: {col}")
            continue

        if not pd.api.types.is_numeric_dtype(df_cleaned[col]):
            logger.warning(f"Column is not numeric: {col}")
            continue

        rows_before = len(df_cleaned)

        if method == 'iqr':
            Q1 = df_cleaned[col].quantile(0.25)
            Q3 = df_cleaned[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - threshold * IQR
            upper_bound = Q3 + threshold * IQR
            df_cleaned = df_cleaned[(df_cleaned[col] >= lower_bound) & (df_cleaned[col] <= upper_bound)]
            removed = rows_before - len(df_cleaned)
            logger.debug(f"{col}: method=iqr, threshold={threshold}, removed={removed}")

        elif method == 'zscore':
            mean = df_cleaned[col].mean()
            std = df_cleaned[col].std()
            if std > 0:
                z_scores = np.abs((df_cleaned[col] - mean) / std)
                df_cleaned = df_cleaned[z_scores <= threshold]
            removed = rows_before - len(df_cleaned)
            logger.debug(f"{col}: zscore threshold={threshold}, removed={removed}")

    return df_cleaned


def process_data(df, config):
    """Apply the processing steps enabled in the configuration."""
    df_processed = df.copy()

    processing_config = (config or {}).get('processing') or {}

    # 1. Remove duplicates
    if processing_config.get('remove_duplicates', False):
        df_processed = remove_duplicates(df_processed)

    missing_config = processing_config.get('missing') or {}
    if missing_config.get('enabled', False):
        axis = missing_config.get('axis', 'rows')
        df_processed = handle_missing(df_processed, axis=axis)

    # 3. Remove outliers
    outliers_config = processing_config.get('outliers') or {}
    if outliers_config.get('enabled', False):
        columns = outliers_config.get('columns', [])
        method = outliers_config.get('method')
        threshold = outliers_config.get('threshold')
        df_processed = remove_outliers(df_processed, columns, method, threshold)

    return df_processed


def create_cleaning_report(df_before, df_after):
    """Return a dictionary summarizing the cleaning results."""
    return {
        'rows_before': len(df_before),
        'rows_after': len(df_after),
        'rows_removed': len(df_before) - len(df_after),
        'columns_before': len(df_before.columns),
        'columns_after': len(df_after.columns),
        'columns_removed': len(df_before.columns) - len(df_after.columns)
    }