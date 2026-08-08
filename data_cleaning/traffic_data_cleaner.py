import os
import sys
import pandas as pd
import numpy as np


# ============================================================
# CONFIGURATION
# ============================================================

# Change this to your actual dataset filename.
#
# Examples:
# FILE_PATH = "traffic_dataset.xlsx"
# FILE_PATH = "traffic_dataset.csv"

FILE_PATH = "../data/raw/traffic_dataset.csv"

# Output files
CLEANED_FILE = "../data/processed/traffic_dataset_cleaned.csv"
SUMMARY_FILE = "column_summary.csv"
REPORT_FILE = "data_cleaning_report.txt"


# ============================================================
# LOAD DATASET
# ============================================================

def load_dataset(file_path):

    if not os.path.exists(file_path):

        print("\nERROR: Dataset file not found.")
        print("File:", file_path)

        sys.exit(1)

    extension = os.path.splitext(file_path)[1].lower()

    try:

        if extension == ".csv":

            df = pd.read_csv(file_path)

        elif extension in [".xlsx", ".xls"]:

            df = pd.read_excel(file_path)

        else:

            print("\nERROR: Unsupported file format.")
            print("Supported formats: CSV, XLSX, XLS")

            sys.exit(1)

    except Exception as e:

        print("\nERROR while reading dataset:")
        print(e)

        sys.exit(1)

    return df


# ============================================================
# EXCEL COLUMN NAME
# Converts:
# 1  -> A
# 2  -> B
# ...
# 26 -> Z
# 27 -> AA
# ...
# 36 -> AJ
# ============================================================

def excel_column_name(number):

    result = ""

    while number > 0:

        number, remainder = divmod(
            number - 1,
            26
        )

        result = chr(
            65 + remainder
        ) + result

    return result


# ============================================================
# DETECT COLUMN TYPE
# ============================================================

def detect_type(series):

    # Already datetime
    if pd.api.types.is_datetime64_any_dtype(series):

        return "datetime"

    # Numeric
    if pd.api.types.is_numeric_dtype(series):

        return "numeric"

    # Try to detect datetime stored as text
    if series.dtype == "object" or pd.api.types.is_string_dtype(series):

        sample = (
            series
            .dropna()
            .astype(str)
            .head(100)
        )

        if len(sample) > 0:

            converted = pd.to_datetime(
                sample,
                errors="coerce"
            )

            valid_ratio = converted.notna().mean()

            if valid_ratio >= 0.8:

                return "datetime"

    return "categorical/text"


# ============================================================
# OUTLIER DETECTION
# Uses IQR method
# ============================================================

def count_outliers(series):

    numeric = pd.to_numeric(
        series,
        errors="coerce"
    ).dropna()

    if len(numeric) < 4:

        return 0

    q1 = numeric.quantile(0.25)
    q3 = numeric.quantile(0.75)

    iqr = q3 - q1

    if iqr == 0:

        return 0

    lower = q1 - (1.5 * iqr)
    upper = q3 + (1.5 * iqr)

    outliers = numeric[
        (numeric < lower) |
        (numeric > upper)
    ]

    return len(outliers)


# ============================================================
# STANDARDIZE COLUMN NAMES
# ============================================================

def clean_column_names(df):

    original_names = list(df.columns)

    cleaned_names = []

    for name in df.columns:

        name = str(name)

        name = name.strip()

        name = name.lower()

        name = name.replace(
            " ",
            "_"
        )

        name = name.replace(
            "-",
            "_"
        )

        cleaned_names.append(name)

    df.columns = cleaned_names

    return df, original_names


# ============================================================
# REMOVE COMPLETELY EMPTY ROWS/COLUMNS
# ============================================================

def remove_empty_data(df):

    before_rows = len(df)
    before_columns = len(df.columns)

    # Remove columns where every value is missing
    df = df.dropna(
        axis=1,
        how="all"
    )

    # Remove rows where every value is missing
    df = df.dropna(
        axis=0,
        how="all"
    )

    removed_rows = before_rows - len(df)
    removed_columns = before_columns - len(df.columns)

    return (
        df,
        removed_rows,
        removed_columns
    )


# ============================================================
# STANDARDIZE TEXT VALUES
# ============================================================

def clean_text_columns(df):

    text_columns = []

    for column in df.columns:

        detected_type = detect_type(
            df[column]
        )

        if detected_type == "categorical/text":

            text_columns.append(column)

            df[column] = (
                df[column]
                .astype("string")
                .str.strip()
            )

            # Empty strings become missing values
            df[column] = df[column].replace(
                "",
                pd.NA
            )

    return df, text_columns


# ============================================================
# CONVERT DATETIME COLUMNS
# ============================================================

def convert_datetime_columns(df):

    datetime_columns = []

    for column in df.columns:

        detected_type = detect_type(
            df[column]
        )

        if detected_type == "datetime":

            try:

                converted = pd.to_datetime(
                    df[column],
                    errors="coerce"
                )

                # Only use conversion if it actually
                # produced useful datetime values.

                valid_ratio = converted.notna().mean()

                if valid_ratio >= 0.8:

                    df[column] = converted

                    datetime_columns.append(
                        column
                    )

            except Exception:

                pass

    return df, datetime_columns


# ============================================================
# CREATE TIME FEATURES
# ============================================================

def create_time_features(
    df,
    datetime_columns
):

    created_features = []

    for column in datetime_columns:

        # Avoid creating hundreds of duplicate features
        # if multiple datetime columns exist.

        prefix = column

        hour_name = f"{prefix}_hour"
        day_name = f"{prefix}_day_of_week"
        weekend_name = f"{prefix}_is_weekend"

        df[hour_name] = (
            df[column].dt.hour
        )

        df[day_name] = (
            df[column].dt.dayofweek
        )

        df[weekend_name] = (
            df[day_name] >= 5
        ).astype(int)

        created_features.extend(
            [
                hour_name,
                day_name,
                weekend_name
            ]
        )

    return df, created_features


# ============================================================
# MISSING VALUE ANALYSIS
# ============================================================

def analyze_missing_values(df):

    missing_information = []

    for column in df.columns:

        missing_count = df[column].isna().sum()

        missing_percent = (
            missing_count /
            len(df) *
            100
            if len(df) > 0
            else 0
        )

        missing_information.append(
            {
                "Column": column,
                "Missing Count": missing_count,
                "Missing %": round(
                    missing_percent,
                    2
                )
            }
        )

    return pd.DataFrame(
        missing_information
    )


# ============================================================
# SAFE MISSING VALUE HANDLING
#
# IMPORTANT:
# We only automatically fill NUMERIC columns
# using their MEDIAN.
#
# We do NOT automatically fill categorical columns.
# We do NOT automatically fill datetime columns.
# ============================================================

def handle_numeric_missing_values(df):

    changes = []

    for column in df.columns:

        detected_type = detect_type(
            df[column]
        )

        if detected_type == "numeric":

            missing_before = (
                df[column]
                .isna()
                .sum()
            )

            if missing_before > 0:

                median_value = (
                    df[column]
                    .median()
                )

                # If median exists, fill missing
                if pd.notna(median_value):

                    df[column] = (
                        df[column]
                        .fillna(median_value)
                    )

                    changes.append(
                        {
                            "Column": column,
                            "Action": "Filled numeric missing values with median",
                            "Values Changed": missing_before
                        }
                    )

    return df, changes


# ============================================================
# COLUMN ANALYSIS
# ============================================================

def analyze_columns(df):

    results = []

    for index, column in enumerate(df.columns):

        series = df[column]

        excel_col = excel_column_name(
            index + 1
        )

        detected_type = detect_type(
            series
        )

        missing_count = (
            series
            .isna()
            .sum()
        )

        missing_percent = (
            missing_count /
            len(df) *
            100
            if len(df) > 0
            else 0
        )

        unique_values = (
            series
            .nunique(
                dropna=True
            )
        )

        possible_outliers = ""

        minimum = ""
        maximum = ""
        mean = ""
        median = ""

        if detected_type == "numeric":

            numeric = pd.to_numeric(
                series,
                errors="coerce"
            ).dropna()

            if len(numeric) > 0:

                minimum = numeric.min()
                maximum = numeric.max()
                mean = numeric.mean()
                median = numeric.median()

                possible_outliers = (
                    count_outliers(series)
                )

        results.append(
            {
                "Excel Column": excel_col,
                "Column Name": column,
                "Detected Type": detected_type,
                "Pandas Type": str(
                    series.dtype
                ),
                "Missing Count": missing_count,
                "Missing %": round(
                    missing_percent,
                    2
                ),
                "Unique Values": unique_values,
                "Minimum": minimum,
                "Maximum": maximum,
                "Mean": mean,
                "Median": median,
                "Possible Outliers": possible_outliers
            }
        )

    return pd.DataFrame(results)


# ============================================================
# CREATE TEXT REPORT
# ============================================================

def create_report(
    original_shape,
    cleaned_shape,
    duplicate_count,
    removed_empty_rows,
    removed_empty_columns,
    text_columns,
    datetime_columns,
    created_features,
    missing_changes,
    summary
):

    with open(
        REPORT_FILE,
        "w",
        encoding="utf-8"
    ) as report:

        report.write(
            "=" * 80 + "\n"
        )

        report.write(
            "TRAFFIC DATA CLEANING REPORT\n"
        )

        report.write(
            "=" * 80 + "\n\n"
        )

        # ----------------------------------------------------
        # Dataset size
        # ----------------------------------------------------

        report.write(
            "DATASET SIZE\n"
        )

        report.write(
            "-" * 80 + "\n"
        )

        report.write(
            f"Original rows: "
            f"{original_shape[0]:,}\n"
        )

        report.write(
            f"Original columns: "
            f"{original_shape[1]}\n"
        )

        report.write(
            f"Final rows: "
            f"{cleaned_shape[0]:,}\n"
        )

        report.write(
            f"Final columns: "
            f"{cleaned_shape[1]}\n\n"
        )

        # ----------------------------------------------------
        # Duplicates
        # ----------------------------------------------------

        report.write(
            "DUPLICATES\n"
        )

        report.write(
            "-" * 80 + "\n"
        )

        report.write(
            f"Exact duplicate rows found: "
            f"{duplicate_count:,}\n\n"
        )

        # ----------------------------------------------------
        # Empty rows/columns
        # ----------------------------------------------------

        report.write(
            "EMPTY DATA\n"
        )

        report.write(
            "-" * 80 + "\n"
        )

        report.write(
            f"Completely empty rows removed: "
            f"{removed_empty_rows:,}\n"
        )

        report.write(
            f"Completely empty columns removed: "
            f"{removed_empty_columns:,}\n\n"
        )

        # ----------------------------------------------------
        # Text columns
        # ----------------------------------------------------

        report.write(
            "TEXT/CATEGORICAL COLUMNS\n"
        )

        report.write(
            "-" * 80 + "\n"
        )

        for column in text_columns:

            report.write(
                f"- {column}\n"
            )

        report.write("\n")

        # ----------------------------------------------------
        # Datetime columns
        # ----------------------------------------------------

        report.write(
            "DATETIME COLUMNS\n"
        )

        report.write(
            "-" * 80 + "\n"
        )

        for column in datetime_columns:

            report.write(
                f"- {column}\n"
            )

        report.write("\n")

        # ----------------------------------------------------
        # Created features
        # ----------------------------------------------------

        report.write(
            "CREATED TIME FEATURES\n"
        )

        report.write(
            "-" * 80 + "\n"
        )

        for feature in created_features:

            report.write(
                f"- {feature}\n"
            )

        report.write("\n")

        # ----------------------------------------------------
        # Missing values
        # ----------------------------------------------------

        report.write(
            "MISSING VALUE CHANGES\n"
        )

        report.write(
            "-" * 80 + "\n"
        )

        if len(missing_changes) == 0:

            report.write(
                "No numeric missing values were filled.\n"
            )

        else:

            for change in missing_changes:

                report.write(
                    f"- {change['Column']}: "
                    f"{change['Action']} "
                    f"({change['Values Changed']} values)\n"
                )

        report.write("\n")

        # ----------------------------------------------------
        # Column analysis
        # ----------------------------------------------------

        report.write(
            "COLUMN ANALYSIS\n"
        )

        report.write(
            "-" * 80 + "\n\n"
        )

        for _, row in summary.iterrows():

            report.write(
                f"{row['Excel Column']} - "
                f"{row['Column Name']}\n"
            )

            report.write(
                f"  Type: "
                f"{row['Detected Type']}\n"
            )

            report.write(
                f"  Missing: "
                f"{row['Missing Count']} "
                f"({row['Missing %']}%)\n"
            )

            report.write(
                f"  Unique values: "
                f"{row['Unique Values']}\n"
            )

            if row["Detected Type"] == "numeric":

                report.write(
                    f"  Minimum: "
                    f"{row['Minimum']}\n"
                )

                report.write(
                    f"  Maximum: "
                    f"{row['Maximum']}\n"
                )

                report.write(
                    f"  Mean: "
                    f"{row['Mean']}\n"
                )

                report.write(
                    f"  Median: "
                    f"{row['Median']}\n"
                )

                report.write(
                    f"  Possible outliers: "
                    f"{row['Possible Outliers']}\n"
                )

            report.write("\n")


# ============================================================
# MAIN PROGRAM
# ============================================================

def main():

    print()
    print("=" * 70)
    print("TRAFFIC DATA CLEANING PROGRAM")
    print("=" * 70)

    # --------------------------------------------------------
    # 1. LOAD DATASET
    # --------------------------------------------------------

    print("\n[1/9] Loading dataset...")

    df = load_dataset(
        FILE_PATH
    )

    original_shape = df.shape

    print(
        "Dataset loaded successfully."
    )

    print(
        f"Rows: {original_shape[0]:,}"
    )

    print(
        f"Columns: {original_shape[1]}"
    )

    # --------------------------------------------------------
    # 2. REMOVE EXACT DUPLICATES
    # --------------------------------------------------------

    print(
        "\n[2/9] Checking duplicates..."
    )

    duplicate_count = (
        df.duplicated()
        .sum()
    )

    print(
        f"Duplicate rows found: "
        f"{duplicate_count:,}"
    )

    if duplicate_count > 0:

        df = df.drop_duplicates()

        print(
            "Exact duplicates removed."
        )

    # --------------------------------------------------------
    # 3. CLEAN COLUMN NAMES
    # --------------------------------------------------------

    print(
        "\n[3/9] Cleaning column names..."
    )

    df, original_column_names = (
        clean_column_names(df)
    )

    print(
        "Column names standardized."
    )

    # --------------------------------------------------------
    # 4. REMOVE COMPLETELY EMPTY DATA
    # --------------------------------------------------------

    print(
        "\n[4/9] Checking completely empty rows/columns..."
    )

    (
        df,
        removed_empty_rows,
        removed_empty_columns
    ) = remove_empty_data(df)

    print(
        f"Empty rows removed: "
        f"{removed_empty_rows:,}"
    )

    print(
        f"Empty columns removed: "
        f"{removed_empty_columns:,}"
    )

    # --------------------------------------------------------
    # 5. CLEAN TEXT
    # --------------------------------------------------------

    print(
        "\n[5/9] Cleaning text columns..."
    )

    df, text_columns = (
        clean_text_columns(df)
    )

    print(
        f"Text/categorical columns found: "
        f"{len(text_columns)}"
    )

    # --------------------------------------------------------
    # 6. DATETIME PROCESSING
    # --------------------------------------------------------

    print(
        "\n[6/9] Detecting datetime columns..."
    )

    df, datetime_columns = (
        convert_datetime_columns(df)
    )

    print(
        f"Datetime columns found: "
        f"{len(datetime_columns)}"
    )

    for column in datetime_columns:

        print(
            f"  - {column}"
        )

    # --------------------------------------------------------
    # 7. CREATE TIME FEATURES
    # --------------------------------------------------------

    print(
        "\n[7/9] Creating time features..."
    )

    (
        df,
        created_features
    ) = create_time_features(
        df,
        datetime_columns
    )

    print(
        f"Created {len(created_features)} "
        f"time features."
    )

    # --------------------------------------------------------
    # 8. HANDLE NUMERIC MISSING VALUES
    # --------------------------------------------------------

    print(
        "\n[8/9] Handling numeric missing values..."
    )

    (
        df,
        missing_changes
    ) = handle_numeric_missing_values(
        df
    )

    if len(missing_changes) == 0:

        print(
            "No numeric missing values required filling."
        )

    else:

        for change in missing_changes:

            print(
                f"  {change['Column']}: "
                f"{change['Values Changed']} "
                f"values filled with median."
            )

    # --------------------------------------------------------
    # 9. FINAL ANALYSIS
    # --------------------------------------------------------

    print(
        "\n[9/9] Running final quality check..."
    )

    summary = analyze_columns(
        df
    )

    cleaned_shape = df.shape

    remaining_missing = (
        df.isna()
        .sum()
        .sum()
    )

    remaining_duplicates = (
        df.duplicated()
        .sum()
    )

    print(
        "\nFinal dataset:"
    )

    print(
        f"Rows: {cleaned_shape[0]:,}"
    )

    print(
        f"Columns: {cleaned_shape[1]}"
    )

    print(
        f"Remaining missing values: "
        f"{remaining_missing:,}"
    )

    print(
        f"Remaining exact duplicates: "
        f"{remaining_duplicates:,}"
    )

    # --------------------------------------------------------
    # SAVE CLEANED DATASET
    # --------------------------------------------------------

    print(
        "\nSaving cleaned dataset..."
    )

    df.to_csv(
        CLEANED_FILE,
        index=False
    )

    # --------------------------------------------------------
    # SAVE COLUMN SUMMARY
    # --------------------------------------------------------

    summary.to_csv(
        SUMMARY_FILE,
        index=False
    )

    # --------------------------------------------------------
    # CREATE TEXT REPORT
    # --------------------------------------------------------

    create_report(
        original_shape=original_shape,
        cleaned_shape=cleaned_shape,
        duplicate_count=duplicate_count,
        removed_empty_rows=removed_empty_rows,
        removed_empty_columns=removed_empty_columns,
        text_columns=text_columns,
        datetime_columns=datetime_columns,
        created_features=created_features,
        missing_changes=missing_changes,
        summary=summary
    )

    # --------------------------------------------------------
    # DONE
    # --------------------------------------------------------

    print()
    print("=" * 70)
    print("CLEANING COMPLETE")
    print("=" * 70)

    print("\nFiles created:")

    print(
        f"1. {CLEANED_FILE}"
    )

    print(
        f"2. {SUMMARY_FILE}"
    )

    print(
        f"3. {REPORT_FILE}"
    )

    print(
        "\nYour original dataset was not modified."
    )


# ============================================================
# PROGRAM ENTRY POINT
# ============================================================

if __name__ == "__main__":

    main()