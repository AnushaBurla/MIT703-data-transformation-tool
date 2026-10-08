import csv
import json


def load_csv_file(filepath):
    """Read a CSV file and return a list of dictionaries, one per row."""
    with open(filepath, newline="") as file:
        reader = csv.DictReader(file)
        return list(reader)


def load_json_file(filepath):
    """Read a JSON file and return its contents as a list of dictionaries."""
    with open(filepath) as file:
        return json.load(file)


def load_file(filepath):
    """Load a CSV or JSON file based on its file extension."""
    if filepath.endswith(".csv"):
        return load_csv_file(filepath)
    elif filepath.endswith(".json"):
        return load_json_file(filepath)
    else:
        raise ValueError(f"Unsupported file type: {filepath}")


def load_multiple_files(filepaths):
    """Load several CSV/JSON files and combine all records into one list."""
    all_records = []
    for filepath in filepaths:
        try:
            records = load_file(filepath)
            all_records.extend(records)
        except FileNotFoundError:
            print(f"Warning: {filepath} was not found, skipping it.")
        except (json.JSONDecodeError, csv.Error):
            print(f"Warning: {filepath} could not be read, skipping it.")
    return all_records


def validate_records(records, required_fields):
    """Keep only records that have all the required fields filled in."""
    valid_records = []
    skipped_count = 0

    for record in records:
        is_valid = True
        for field in required_fields:
            if field not in record or not record[field]:
                is_valid = False
                break

        if is_valid:
            valid_records.append(record)
        else:
            skipped_count += 1

    return valid_records, skipped_count
