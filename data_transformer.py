class TransformationConfig:
    """Stores the filter settings chosen by the user."""

    def __init__(self, station_filter=None):
        self.station_filter = station_filter

    def matches(self, record):
        """Check if a record passes the configured filter."""
        if self.station_filter is None:
            return True
        return record.get("station_name") == self.station_filter


def clean_records(records):
    """Turn text numbers into real numbers, skipping ones that fail."""
    cleaned_records = []
    for record in records:
        try:
            cleaned = dict(record)
            cleaned["temperature_c"] = float(cleaned["temperature_c"])
            rainfall = cleaned.get("rainfall_mm", "")
            if rainfall in ("", None):
                cleaned["rainfall_mm"] = 0.0
            else:
                cleaned["rainfall_mm"] = float(rainfall)
            cleaned_records.append(cleaned)
        except (ValueError, TypeError):
            continue
    return cleaned_records


def add_fahrenheit(records):
    """Add a calculated field: temperature in Fahrenheit."""
    for record in records:
        record["temperature_f"] = record["temperature_c"] * 9 / 5 + 32
    return records


def filter_records(records, config):
    """Keep only the records that match the given filter settings."""
    return [record for record in records if config.matches(record)]


def average_temperature_by_station(records):
    """Calculate the average temperature for each station."""
    totals = {}
    counts = {}
    for record in records:
        station = record["station_name"]
        totals[station] = totals.get(station, 0) + record["temperature_c"]
        counts[station] = counts.get(station, 0) + 1

    averages = {}
    for station in totals:
        averages[station] = totals[station] / counts[station]
    return averages


def total_rainfall_by_station(records):
    """Calculate the total rainfall for each station."""
    totals = {}
    for record in records:
        station = record["station_name"]
        totals[station] = totals.get(station, 0) + record["rainfall_mm"]
    return totals
