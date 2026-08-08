"""
Data Preprocessing Script for Traffic Digital Twin Dataset
=========================================================

This script loads, inspects, and preprocesses the traffic digital twin dataset.
Key processing steps include:
1. Loading dataset using pandas.
2. Displaying dataset information and shape.
3. Checking for missing values.
4. Extracting datetime features (hour, day, month, dayofweek) from timestamps.
5. Encoding categorical features and boolean indicators.
6. Separating features (X) and target (y).
"""

import os
import sys
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder


def get_default_dataset_path() -> str:
    """
    Locates the cleaned traffic dataset file path.
    Uses the centrally cleaned dataset at data/processed/traffic_dataset_cleaned.csv.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Primary: cleaned dataset in data/processed/ (relative from backend/ai/training)
    possible_paths = [
        os.path.join(script_dir, "..", "..", "..", "data", "processed", "traffic_dataset_cleaned.csv"),
        os.path.join(os.getcwd(), "data", "processed", "traffic_dataset_cleaned.csv"),
        os.path.join(os.getcwd(), "..", "data", "processed", "traffic_dataset_cleaned.csv"),
    ]

    for path in possible_paths:
        abs_path = os.path.abspath(path)
        if os.path.exists(abs_path):
            return abs_path

    # Return default path if not found
    return os.path.abspath(possible_paths[0])


def load_dataset(file_path: str) -> pd.DataFrame:
    """
    Loads the CSV dataset using pandas.

    Parameters:
        file_path (str): Absolute or relative path to the CSV file.

    Returns:
        pd.DataFrame: Loaded dataset.
    """
    print(f"[INFO] Loading dataset from: {file_path}")
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Dataset file not found at: {file_path}")
        
    df = pd.read_csv(file_path)
    print(f"[SUCCESS] Dataset loaded successfully. Shape: {df.shape}")
    return df


def display_dataset_info(df: pd.DataFrame) -> None:
    """
    Displays dataset summary information, first few rows, and summary statistics.

    Parameters:
        df (pd.DataFrame): The input DataFrame.
    """
    print("\n" + "="*50)
    print(" 1. DATASET INFORMATION ")
    print("="*50)
    print("\n--- DataFrame Info ---")
    df.info()

    print("\n--- First 5 Rows ---")
    print(df.head())

    print("\n--- Summary Statistics (Numerical) ---")
    print(df.describe())


def check_missing_values(df: pd.DataFrame) -> pd.Series:
    """
    Checks and displays missing (null) values in each column of the dataset.

    Parameters:
        df (pd.DataFrame): The input DataFrame.

    Returns:
        pd.Series: Missing value counts per column.
    """
    print("\n" + "="*50)
    print(" 2. MISSING VALUES CHECK ")
    print("="*50)
    
    missing = df.isnull().sum()
    missing_pct = (df.isnull().sum() / len(df)) * 100
    
    missing_df = pd.DataFrame({'Missing_Count': missing, 'Missing_Percentage': missing_pct})
    missing_cols = missing_df[missing_df['Missing_Count'] > 0]
    
    if missing_cols.empty:
        print("[INFO] No missing values found in the dataset.")
    else:
        print("[WARNING] Found missing values in the following columns:")
        print(missing_cols)
        
    return missing


def process_timestamp_features(df: pd.DataFrame, timestamp_col: str = "timestamp") -> pd.DataFrame:
    """
    Converts timestamp column into useful temporal features:
    - hour
    - day
    - month
    - dayofweek (0=Monday, 6=Sunday)
    - year

    Parameters:
        df (pd.DataFrame): Input DataFrame.
        timestamp_col (str): Name of timestamp column.

    Returns:
        pd.DataFrame: DataFrame with extracted datetime features and original timestamp removed.
    """
    df = df.copy()
    if timestamp_col in df.columns:
        print(f"\n[INFO] Extracting datetime features from '{timestamp_col}'...")
        # Convert to pandas datetime
        df[timestamp_col] = pd.to_datetime(df[timestamp_col], errors='coerce')
        
        # Extract features
        df['hour'] = df[timestamp_col].dt.hour
        df['day'] = df[timestamp_col].dt.day
        df['month'] = df[timestamp_col].dt.month
        df['dayofweek'] = df[timestamp_col].dt.dayofweek
        df['year'] = df[timestamp_col].dt.year
        
        # Drop original timestamp column
        df.drop(columns=[timestamp_col], inplace=True)
        print("[SUCCESS] Datetime features extracted: hour, day, month, dayofweek, year.")
    else:
        print(f"[WARNING] Column '{timestamp_col}' not found in DataFrame.")
        
    return df


def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    Imputes missing values for numerical and categorical columns.
    - Numerical columns: imputed with median value.
    - Categorical columns: imputed with mode or 'Unknown'.

    Parameters:
        df (pd.DataFrame): Input DataFrame.

    Returns:
        pd.DataFrame: DataFrame with missing values handled.
    """
    df = df.copy()
    num_cols = df.select_dtypes(include=['number', 'float64', 'int64']).columns
    for col in num_cols:
        if df[col].isnull().sum() > 0:
            median_val = df[col].median()
            df[col] = df[col].fillna(median_val)
            print(f"[IMPUTE] Filled {col} missing values with median ({median_val}).")

    cat_cols = df.select_dtypes(include=['object', 'string', 'category']).columns
    for col in cat_cols:
        if df[col].isnull().sum() > 0:
            mode_val = df[col].mode()[0] if not df[col].mode().empty else 'Unknown'
            df[col] = df[col].fillna(mode_val)
            print(f"[IMPUTE] Filled {col} missing values with mode ('{mode_val}').")

    return df


def encode_categorical_columns(df: pd.DataFrame, target_col: str = "congestion_level") -> tuple[pd.DataFrame, dict]:
    """
    Encodes categorical columns (strings, objects, booleans) into numerical values.
    
    Parameters:
        df (pd.DataFrame): Input DataFrame.
        target_col (str): Name of the target column (e.g., 'congestion_level').

    Returns:
        tuple[pd.DataFrame, dict]: (Encoded DataFrame, Dictionary of LabelEncoders for each column)
    """
    df = df.copy()
    encoders = {}

    print("\n" + "="*50)
    print(" 3. CATEGORICAL ENCODING ")
    print("="*50)

    # 1. Convert boolean columns to integer (0 or 1)
    bool_cols = df.select_dtypes(include=['bool']).columns.tolist()
    for col in bool_cols:
        print(f"[ENCODE] Converting boolean column '{col}' to int (0/1).")
        df[col] = df[col].astype(int)

    # Custom mapping for target if applicable (e.g. congestion_level: Low, Moderate/Medium, High, Severe)
    if target_col in df.columns:
        unique_targets = df[target_col].unique()
        ordinal_mapping = {'Low': 0, 'Medium': 1, 'Moderate': 1, 'High': 2, 'Severe': 3}
        if set(unique_targets).issubset(set(ordinal_mapping.keys())):
            print(f"[ENCODE] Mapping target '{target_col}' using ordinal dictionary: {ordinal_mapping}")
            df[target_col] = df[target_col].map(ordinal_mapping).astype(int)

    # 2. Encode remaining categorical (object/string) columns
    cat_cols = df.select_dtypes(include=['object', 'string', 'category']).columns.tolist()
    if target_col in cat_cols:
        cat_cols.remove(target_col)
    
    print(f"[INFO] Categorical feature columns identified: {cat_cols}")

    for col in cat_cols:
        print(f"[ENCODE] Applying LabelEncoder to feature column '{col}'.")
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col].astype(str))
        encoders[col] = le

    return df, encoders


def preprocess_data(file_path: str = None, target_col: str = "congestion_level") -> tuple[pd.DataFrame, pd.Series]:
    """
    Main preprocessing pipeline function.
    Loads dataset, displays info, checks missing values, processes timestamp,
    encodes categorical features, and splits into X (features) and y (target).

    Parameters:
        file_path (str, optional): Path to CSV dataset. Defaults to auto-located dataset.
        target_col (str): Column name to be used as target.

    Returns:
        tuple[pd.DataFrame, pd.Series]: (X_features, y_target)
    """
    if file_path is None:
        file_path = get_default_dataset_path()

    # Step 1: Load Dataset
    df = load_dataset(file_path)

    # Step 2: Display Dataset Info
    display_dataset_info(df)

    # Step 3: Check and Handle Missing Values
    check_missing_values(df)
    df = handle_missing_values(df)

    # Filter columns to user-specified set if present
    specified_columns = [
        "road_name", "city_zone", "latitude", "longitude", "vehicle_count",
        "avg_speed_kmph", "travel_time_index", "congestion_level", "weather_condition",
        "temperature_c", "humidity_pct", "visibility_km", "signal_status",
        "signal_cycle_time_sec", "avg_wait_time_sec", "incident_reported",
        "incident_type", "road_closure", "construction_zone", "event_nearby",
        "timestamp", "is_peak_hour", "is_weekend", "is_public_holiday"
    ]
    
    # Retain all specified columns that exist in the loaded dataset
    existing_specified = [c for c in specified_columns if c in df.columns]
    if len(existing_specified) > 0:
        print(f"\n[INFO] Filtering dataset to {len(existing_specified)} specified columns.")
        df = df[existing_specified]

    # Step 4: Process Timestamp Features
    df = process_timestamp_features(df, timestamp_col="timestamp")

    # Step 5: Encode Categorical Features & Target
    df_encoded, encoders = encode_categorical_columns(df, target_col=target_col)

    # Step 6: Separate Features and Target
    if target_col in df_encoded.columns:
        X = df_encoded.drop(columns=[target_col])
        y = df_encoded[target_col]
        print(f"\n[SUCCESS] Split completed:")
        print(f" - Features (X) shape: {X.shape}")
        print(f" - Target (y) shape  : {y.shape}")
        return X, y, encoders
    else:
        print(f"\n[WARNING] Target column '{target_col}' not found. Returning processed DataFrame as X, None as y.")
        return df_encoded, None, encoders


if __name__ == "__main__":
    print("="*60)
    print(" RUNNING PREPROCESSING SCRIPT ")
    print("="*60)

    dataset_path = get_default_dataset_path()
    X, y, encoders = preprocess_data(file_path=dataset_path, target_col="congestion_level")

    print("\n--- Sample Processed Features (X.head()) ---")
    print(X.head())

    if y is not None:
        print("\n--- Target Value Counts (y) ---")
        print(y.value_counts())
