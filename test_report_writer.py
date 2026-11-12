import pandas as pd

from report_writer import remove_private_columns, round_numbers, save_to_csv, save_text_summary


def test_remove_private_columns_drops_operator_fields():
    df = pd.DataFrame({
        "station_name": ["Riverside"],
        "operator_name": ["Someone"],
        "operator_email": ["someone@example.com"],
    })
    result = remove_private_columns(df)
    assert "operator_name" not in result.columns
    assert "operator_email" not in result.columns
    assert "station_name" in result.columns


def test_remove_private_columns_does_nothing_if_columns_absent():
    df = pd.DataFrame({"station_name": ["Riverside"]})
    result = remove_private_columns(df)
    assert list(result.columns) == ["station_name"]


def test_round_numbers_rounds_float_columns_only():
    df = pd.DataFrame({
        "station_name": ["Riverside"],
        "temperature_c": [22.456],
    })
    result = round_numbers(df)
    assert result["temperature_c"].iloc[0] == 22.46


def test_save_to_csv_never_includes_private_columns(tmp_path):
    df = pd.DataFrame({
        "station_name": ["Riverside"],
        "operator_email": ["someone@example.com"],
    })
    filepath = tmp_path / "test_output.csv"
    save_to_csv(df, str(filepath))

    saved_content = filepath.read_text()
    assert "someone@example.com" not in saved_content


def test_save_text_summary_contains_station_values(tmp_path):
    avg_temp = pd.Series({"Riverside": 22.5})
    total_rain = pd.Series({"Riverside": 8.0})
    filepath = tmp_path / "summary.txt"
    save_text_summary(avg_temp, total_rain, str(filepath))

    content = filepath.read_text()
    assert "Riverside: 22.50" in content
    assert "8.00" in content
