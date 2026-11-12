import pandas as pd

from data_transformer import (
    TransformationConfig,
    add_fahrenheit,
    average_temperature_by_station,
    clean_records,
    merge_with_station_metadata,
    total_rainfall_by_station,
)


def test_clean_records_converts_date_and_fills_missing_rainfall():
    df = pd.DataFrame({
        "station_name": ["Riverside"],
        "date": ["2026-01-01"],
        "temperature_c": [20.0],
        "rainfall_mm": [None],
    })
    cleaned = clean_records(df)
    assert pd.api.types.is_datetime64_any_dtype(cleaned["date"])
    assert cleaned["rainfall_mm"].iloc[0] == 0.0


def test_clean_records_turns_invalid_date_into_nat():
    df = pd.DataFrame({
        "station_name": ["Riverside"],
        "date": ["not_a_date"],
        "temperature_c": [20.0],
        "rainfall_mm": [1.0],
    })
    cleaned = clean_records(df)
    assert pd.isna(cleaned["date"].iloc[0])


def test_add_fahrenheit_calculates_correct_value():
    df = pd.DataFrame({"temperature_c": [0.0, 100.0]})
    result = add_fahrenheit(df)
    assert result["temperature_f"].iloc[0] == 32.0
    assert result["temperature_f"].iloc[1] == 212.0


def test_transformation_config_filters_to_selected_station():
    df = pd.DataFrame({"station_name": ["Riverside", "Hilltop"]})
    config = TransformationConfig(station_filter="Riverside")
    filtered = config.apply_filter(df)
    assert list(filtered["station_name"]) == ["Riverside"]


def test_transformation_config_returns_all_rows_when_no_filter_set():
    df = pd.DataFrame({"station_name": ["Riverside", "Hilltop"]})
    config = TransformationConfig(station_filter=None)
    filtered = config.apply_filter(df)
    assert len(filtered) == 2


def test_merge_with_station_metadata_labels_unknown_station():
    readings = pd.DataFrame({"station_name": ["Mystery Station"], "temperature_c": [10.0]})
    metadata = pd.DataFrame({
        "station_name": ["Riverside"],
        "region": ["North Valley"],
        "operator_name": ["Someone"],
        "operator_email": ["someone@example.com"],
    })
    merged = merge_with_station_metadata(readings, metadata)
    assert merged["region"].iloc[0] == "Unknown"


def test_average_temperature_by_station_calculates_mean():
    df = pd.DataFrame({
        "station_name": ["Riverside", "Riverside"],
        "temperature_c": [20.0, 30.0],
    })
    averages = average_temperature_by_station(df)
    assert averages["Riverside"] == 25.0


def test_total_rainfall_by_station_calculates_sum():
    df = pd.DataFrame({
        "station_name": ["Hilltop", "Hilltop"],
        "rainfall_mm": [1.0, 2.5],
    })
    totals = total_rainfall_by_station(df)
    assert totals["Hilltop"] == 3.5
