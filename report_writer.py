import logging

logging.basicConfig(
    filename="pipeline.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)

PRIVATE_COLUMNS = ["operator_name", "operator_email"]


def remove_private_columns(df):
    """Drop personal operator details before any report is saved."""
    columns_to_drop = [col for col in PRIVATE_COLUMNS if col in df.columns]
    if columns_to_drop:
        logging.info(f"Removing private columns before saving: {columns_to_drop}")
    return df.drop(columns=columns_to_drop)


def round_numbers(df):
    """Round decimal number columns to 2 places for clean, readable output."""
    df = df.copy()
    decimal_columns = df.select_dtypes(include="float").columns
    df[decimal_columns] = df[decimal_columns].round(2)
    return df


def save_to_csv(df, filepath):
    """Save a DataFrame to CSV, with private columns removed first."""
    safe_df = round_numbers(remove_private_columns(df))
    safe_df.to_csv(filepath, index=False)
    logging.info(f"Saved {len(safe_df)} rows to {filepath}")


def save_to_json(df, filepath):
    """Save a DataFrame to JSON, with private columns removed first."""
    safe_df = round_numbers(remove_private_columns(df))
    safe_df.to_json(filepath, orient="records", indent=2)
    logging.info(f"Saved {len(safe_df)} rows to {filepath}")


def save_text_summary(average_temp, total_rainfall, filepath):
    """Save a plain text summary of the aggregated results."""
    with open(filepath, "w") as file:
        file.write("Weather Summary Report\n")
        file.write("=======================\n\n")
        file.write("Average temperature by station (C):\n")
        for station, value in average_temp.items():
            file.write(f"  {station}: {value:.2f}\n")
        file.write("\n")
        file.write("Total rainfall by station (mm):\n")
        for station, value in total_rainfall.items():
            file.write(f"  {station}: {value:.2f}\n")
    logging.info(f"Saved text summary to {filepath}")
