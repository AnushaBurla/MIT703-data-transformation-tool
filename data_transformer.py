import pandas as pd


class TransformationConfig:
    """Stores the filter settings chosen by the user."""

    def __init__(self, station_filter=None):
        self.station_filter = station_filter

    def apply_filter(self, df):
        """Return rows matching the configured filter, or all rows if none set."""
        if self.station_filter is None:
            return df
        return df[df["station_name"] == self.station_filter]


def clean_records(df):
    """Convert the date column to a real date, fill missing rainfall with 0."""
    df = df.copy()
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["rainfall_mm"] = df["rainfall_mm"].fillna(0.0)
    return df


def add_fahrenheit(df):
    """Add a calculated field: temperature in Fahrenheit."""
    df = df.copy()
    df["temperature_f"] = df["temperature_c"] * 9 / 5 + 32
    return df


def merge_with_station_metadata(df, metadata_df):
    """Merge readings with station metadata (region, operator) on station_name."""
    merged = df.merge(metadata_df, on="station_name", how="left")
    merged["region"] = merged["region"].fillna("Unknown")
    return merged


def average_temperature_by_station(df):
    """Calculate the average temperature for each station."""
    return df.groupby("station_name")["temperature_c"].mean()


def total_rainfall_by_station(df):
    """Calculate the total rainfall for each station."""
    return df.groupby("station_name")["rainfall_mm"].sum()
