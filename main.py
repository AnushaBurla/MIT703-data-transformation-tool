import argparse

from data_loader import load_multiple_files, validate_records, load_csv_file
from data_transformer import (
    TransformationConfig,
    clean_records,
    add_fahrenheit,
    merge_with_station_metadata,
    average_temperature_by_station,
    total_rainfall_by_station,
)
from report_writer import save_to_csv, save_to_json, save_text_summary


def parse_arguments():
    """Read command-line options for which files to use and how to filter."""
    parser = argparse.ArgumentParser(
        description="Combine, clean and summarise weather station readings."
    )
    parser.add_argument(
        "--readings", nargs="+", required=True,
        help="One or more CSV/JSON reading files to load",
    )
    parser.add_argument(
        "--metadata", required=True,
        help="CSV file with station metadata (station_name, region, operator details)",
    )
    parser.add_argument(
        "--station", default=None,
        help="Only include readings from this station (optional)",
    )
    return parser.parse_args()


def main():
    args = parse_arguments()

    df = load_multiple_files(args.readings)
    valid_df, skipped_count = validate_records(
        df, ["station_name", "date", "temperature_c"]
    )
    print(f"Loaded {len(df)} readings, {len(valid_df)} valid, {skipped_count} skipped")

    cleaned_df = clean_records(valid_df)
    cleaned_df = add_fahrenheit(cleaned_df)

    metadata_df = load_csv_file(args.metadata)
    merged_df = merge_with_station_metadata(cleaned_df, metadata_df)

    config = TransformationConfig(station_filter=args.station)
    filtered_df = config.apply_filter(merged_df)

    save_to_csv(filtered_df, "output_readings.csv")
    save_to_json(filtered_df, "output_readings.json")

    average_temp = average_temperature_by_station(filtered_df)
    total_rainfall = total_rainfall_by_station(filtered_df)
    save_text_summary(average_temp, total_rainfall, "output_summary.txt")

    print()
    print("Average temperature by station (C):")
    print(average_temp)
    print()
    print("Total rainfall by station (mm):")
    print(total_rainfall)
    print()
    print("Saved output_readings.csv, output_readings.json and output_summary.txt")


if __name__ == "__main__":
    main()
