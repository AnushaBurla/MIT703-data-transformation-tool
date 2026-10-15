import pandas as pd


def load_csv_file(filepath):
    """Read a CSV file into a DataFrame."""
    return pd.read_csv(filepath)


def load_json_file(filepath):
    """Read a JSON file into a DataFrame."""
    # convert_dates=False keeps date-looking text as plain text here,
    # matching what pd.read_csv does, so both sources start out the
    # same way. Converting to a real date happens later, in cleaning.
    return pd.read_json(filepath, convert_dates=False)


def load_file(filepath):
    """Load a CSV or JSON file based on its file extension."""
    if filepath.endswith(".csv"):
        return load_csv_file(filepath)
    elif filepath.endswith(".json"):
        return load_json_file(filepath)
    else:
        raise ValueError(f"Unsupported file type: {filepath}")


def load_multiple_files(filepaths):
    """Load several CSV/JSON files and combine them into one DataFrame."""
    all_dataframes = []
    for filepath in filepaths:
        try:
            all_dataframes.append(load_file(filepath))
        except FileNotFoundError:
            print(f"Warning: {filepath} was not found, skipping it.")
        except ValueError as error:
            print(f"Warning: {error}")

    if not all_dataframes:
        return pd.DataFrame()

    return pd.concat(all_dataframes, ignore_index=True)


def validate_records(df, required_fields):
    """Keep only rows that have all required fields filled in."""
    df = df.copy()
    # Treat empty text the same as a truly missing value
    df[required_fields] = df[required_fields].replace("", pd.NA)

    before_count = len(df)
    valid_df = df.dropna(subset=required_fields)
    skipped_count = before_count - len(valid_df)
    return valid_df, skipped_count
