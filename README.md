MIT703 - Assessment 2: CSV/JSON Data Transformation Tool

Name: Anusha Burla
Student ID: SE20262831

What this project does

This is a command-line tool that loads CSV and/or JSON files, cleans and combines the data, lets the user apply filters and calculations, and saves the results as CSV, JSON and a text summary.

Project status

This project is being built between Week 5 and Week 12. This README will be updated as more parts are finished.

- data_loader.py - done. Loads CSV/JSON files, combines them, and skips records missing required fields.
- data_transformer.py - done. Cleans the number fields, adds a calculated Fahrenheit field, filters by station, and works out average temperature and total rainfall per station.
- report_writer.py - not started yet.
- main.py - not started yet.

Planned project structure

- main.py - runs the program and connects everything together
- data_loader.py - loads and checks the CSV/JSON files
- data_transformer.py - cleans, combines, filters and calculates the data
- report_writer.py - saves the final results as CSV, JSON and text

Sample data

The sample_data folder has made-up weather station readings I created myself for testing (Riverside and Hilltop stations). This is not real recorded weather data, just example data to develop and test the code with.
