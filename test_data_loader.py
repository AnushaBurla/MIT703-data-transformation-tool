import pandas as pd
import pytest

from data_loader import load_csv_file, load_file, load_multiple_files, validate_records


def test_load_csv_file_reads_expected_columns(tmp_path):
    csv_path = tmp_path / "sample.csv"
    csv_path.write_text("station_name,temperature_c\nRiverside,20.0\n")
    df = load_csv_file(str(csv_path))
    assert list(df.columns) == ["station_name", "temperature_c"]
    assert len(df) == 1


def test_load_file_raises_for_unsupported_extension(tmp_path):
    bad_path = tmp_path / "data.txt"
    bad_path.write_text("not a real data file")
    with pytest.raises(ValueError):
        load_file(str(bad_path))


def test_load_multiple_files_skips_missing_file_without_crashing(tmp_path, capsys):
    good_path = tmp_path / "good.csv"
    good_path.write_text("station_name,temperature_c\nHilltop,15.0\n")
    missing_path = tmp_path / "does_not_exist.csv"

    df = load_multiple_files([str(good_path), str(missing_path)])

    assert len(df) == 1
    captured = capsys.readouterr()
    assert "was not found" in captured.out


def test_validate_records_keeps_rows_with_required_fields():
    df = pd.DataFrame({
        "station_name": ["Riverside", "Hilltop"],
        "temperature_c": [20.0, 18.0],
    })
    valid_df, skipped = validate_records(df, ["station_name", "temperature_c"])
    assert len(valid_df) == 2
    assert skipped == 0


def test_validate_records_treats_empty_string_as_missing():
    df = pd.DataFrame({
        "station_name": ["Riverside", ""],
        "temperature_c": [20.0, 18.0],
    })
    valid_df, skipped = validate_records(df, ["station_name", "temperature_c"])
    assert len(valid_df) == 1
    assert skipped == 1


def test_validate_records_skips_every_row_when_all_are_missing_a_field():
    df = pd.DataFrame({
        "station_name": [None, None],
        "temperature_c": [20.0, 18.0],
    })
    valid_df, skipped = validate_records(df, ["station_name", "temperature_c"])
    assert len(valid_df) == 0
    assert skipped == 2
