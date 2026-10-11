# data_processor.py
import logging
import pandas as pd

logger = logging.getLogger(__name__)


def remove_duplicates(df):
    """Remove duplicate rows."""
    initial_rows = len(df)
    df_cleaned = df.drop_duplicates()
    rows_removed = initial_rows - len(df_cleaned)
    logger.debug(f"Removed {rows_removed} duplicate rows.")
    return df_cleaned


def handle_missing(df, axis="rows"):
    """Drop rows or columns containing missing values."""
    initial_rows = len(df)
    df_cleaned = df.dropna(axis=axis)
    rows_removed = initial_rows - len(df_cleaned)
    logger.debug(f"Removed {rows_removed} rows with missing values.")
    return df_cleaned


def remove_outliers(df, columns, method, threshold):
    """Remove outliers from the specified numeric columns."""
    if method not in ['iqr', 'zscore']:
        logger.error(f"Unsupported outlier method: {method}")
        raise ValueError(f"Unsupported outlier method: {method}")
        
    df_cleaned = df.copy()
    total_removed = 0
    
    for col in columns:
        if col not in df_cleaned.columns:
            logger.warning(f"Column not found: {col}")
            continue
            
        if not pd.api.types.is_numeric_dtype(df_cleaned[col]):
            logger.warning(f"Column is not numeric: {col}")
            continue

        initial_rows = len(df_cleaned)
        
        if method == 'iqr':
            Q1 = df_cleaned[col].quantile(0.25)
            Q3 = df_cleaned[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - threshold * IQR
            upper_bound = Q3 + threshold * IQR
            df_cleaned = df_cleaned[(df_cleaned[col] >= lower_bound) & (df_cleaned[col] <= upper_bound)]
            
        elif method == 'zscore':
            mean = df_cleaned[col].mean()
            std = df_cleaned[col].std()
            if std > 0:
                z_scores = np.abs((df_cleaned[col] - mean) / std)
                df_cleaned = df_cleaned[z_scores <= threshold]
                
        rows_removed = initial_rows - len(df_cleaned)
        total_removed += rows_removed
        
    logger.debug(f"Outlier removal ({method}, threshold={threshold}): removed {total_removed} rows.")
    return df_cleaned


def process_data(df, config):
    """Apply the processing steps enabled in the configuration."""
    pass


def create_cleaning_report(df_before, df_after):
    """Return a dictionary summarizing the cleaning results."""
    pass
