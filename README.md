MIT703 - Assessment 2: CSV/JSON Data Transformation Tool

Name: Anusha Burla
Student ID: SE20262831

What this project does

This is a command-line tool that loads CSV and/or JSON weather reading files, cleans them, merges them with station metadata, lets the user apply filters and calculations, and will save the results as CSV, JSON and a text summary. Built with pandas.

Project status

This project is being built between Week 5 and Week 12. This README will be updated as more parts are finished.

- data_loader.py - done. Loads CSV/JSON files into a pandas DataFrame, combines multiple files, and skips rows missing required fields.
- data_transformer.py - done. Cleans the date and rainfall fields, adds a calculated Fahrenheit field, merges readings with station metadata, and works out average temperature and total rainfall per station.
- report_writer.py - done. Saves results to CSV, JSON and a text summary, removes operator_name and operator_email before saving anything, and logs every save (and every time private columns are removed) to pipeline.log.
- main.py - done. Command-line entry point that runs the whole pipeline: load, clean, merge, optionally filter by station, calculate, and save.
- test_data_loader.py, test_data_transformer.py, test_report_writer.py - done. 19 pytest tests in total, covering normal cases, edge cases (empty values, missing stations, no filter set) and error conditions (unsupported file type, missing file) across all three modules.
- requirements.txt - done.

How to run the tests

Install the packages in requirements.txt first (pip install -r requirements.txt), then run:
pytest -v
All 19 tests should pass.

How to run this program

Example (all stations):
python main.py --readings sample_data/readings_riverside.csv sample_data/readings_hilltop.json --metadata sample_data/station_metadata.csv

Example (one station only):
python main.py --readings sample_data/readings_riverside.csv sample_data/readings_hilltop.json --metadata sample_data/station_metadata.csv --station Riverside

Run python main.py --help to see all the options.

Planned project structure

- main.py - runs the program and connects everything together
- data_loader.py - loads and checks the CSV/JSON files
- data_transformer.py - cleans, merges, filters and calculates the data
- report_writer.py - saves the final results as CSV, JSON and text

Input data schema

Weather reading files (CSV or JSON), one row per reading:
- station_name (text)
- date (date)
- temperature_c (number)
- rainfall_mm (number)

Station metadata file (station_metadata.csv), one row per station:
- station_name (text)
- region (text)
- operator_name (text) - the person responsible for that station
- operator_email (text)

How the data is combined

Multiple reading files are first combined by stacking them together (they all share the same columns). The combined readings are then merged with station_metadata.csv using station_name as the matching key, which adds the region and operator details to each reading.

Calculations

- temperature_f = temperature_c * 9/5 + 32 (calculated field)
- Average temperature per station = mean of temperature_c, grouped by station_name
- Total rainfall per station = sum of rainfall_mm, grouped by station_name

Privacy

operator_name and operator_email are personal information about the person responsible for each station, not just weather data. These two fields are only used internally while the program runs. report_writer.py removes both columns before saving any CSV or JSON file (the same approach grade_report.py used in Lab 2), and logs it every time this happens so there is a record of it. I tested this directly by searching the saved output files for the operator names and email addresses and confirmed neither appears anywhere in them.

Sample data

The sample_data folder has made-up data I created myself for testing: weather readings (readings_riverside.csv, readings_hilltop.json) and station metadata (station_metadata.csv) with a fictional operator name and email per station. None of this is real recorded data or real people. I deliberately did not source real personal information from the internet, since using a real person's name and email without their knowledge would itself be a privacy problem, which is exactly what this project's privacy handling is meant to avoid.
