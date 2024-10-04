# Incident Report Data Processor

## Overview

This Python script is designed to process police incident reports from a specified PDF URL. It extracts essential information such as the date, incident number, location, nature of the incident, and the Originating Agency Identifier (ORI). The data is stored in an SQLite database for easy retrieval and analysis, and the script also provides functionality to summarize and display the nature of incidents from the database.

## Features

- **Download PDF from URL:** Retrieves the incident report PDF from a provided URL.
- **Extract Incident Data:** Utilizes regex patterns to extract key details such as the date, incident number, location, nature, and ORI from the PDF.
- **Store Data in SQLite Database:** Sets up an SQLite database to store the extracted incident data, facilitating subsequent analysis.
- **Summarize Incidents by Nature:** Analyzes and presents the occurrences of each type of incident based on the extracted data.

## Requirements

- **Python Version:** Ensure you have Python 3.x installed.
- **Required Libraries:**  
  - `requests`  
  - `sqlite3` (included with Python)  
  - `re` (regular expressions, included with Python)  
  - `io` (included with Python)  
  - `PyPDF`

## Installation Instructions

- **Install Dependencies:**
   1. **Get Pipenv:**  
      If you don't already have `pipenv`, you can install it using `pip`:
      ```bash
      pip install pipenv
      ```

   2. **Install Required Libraries:**  
      Navigate to your project directory and run the following command to install `requests` and `PyPDF`:
      ```bash
      pipenv install requests PyPDF
      ```

      To activate the virtual environment created by `pipenv`, run:
      ```bash
      pipenv shell
      ```

      Additionally, install `pytest` for testing purposes:
      ```bash
      pipenv install pytest --dev
      ```

- **Project Setup:** <br>
   Ensure your project directory contains the following files:
   - `main.py` (the main script to run the application)
   - `req.py` (contains utility functions for data fetching, extraction, and storage)

## How to Run the Application

1. **Download and Process Incident PDF:**  
   To process a PDF from a specified URL, run the following command:
   ```bash
   pipenv run main.py <pdf_url>
   ```
   Replace `<pdf_url>` with the actual URL of the incident report PDF. For example:
   ```bash
   pipenv run main.py https://www.normanok.gov/sites/default/files/documents/2024-08/2024-08-01_daily_incident_summary.pdf
   ```

2. **View Incident Nature Summary:**  
   After processing the PDF, the script will print a summary of different incident types and their respective counts. This data is stored in an SQLite database for future reference.

## Functions

### `main.py`

- **`fetch_pdf_from_url(pdf_url)`**  
  - Downloads the PDF file from the specified URL.
  - **Parameters:**  
    - `pdf_url`: The URL of the PDF to download.
  - **Returns:**  
    - A `BytesIO` object containing the PDF data.

- **`extract_incident_data(pdf_file)`**  
  - Extracts incident data from the PDF content using PDF Reader and regex pattern.
  - It uses some helper functions to split the data and also handle few edge cases.
  - **Parameters:**  
    - `pdf_file`: The PDF file to extract data from (as a `BytesIO` object).
  - **Returns:**  
    - A list of dictionaries containing the extracted details (date/time, incident number, location, nature, ORI).


- **`setup_incident_database()`**  
  - Sets up an SQLite database to store incident data, creating a table named `incidents` and dropping any existing table with the same name.
  - **Returns:**  
    - A connection object to the SQLite database.

- **`populate_database_with_data(connection, incident_data)`**  
  - Inserts the extracted incident data into the SQLite database.
  - **Parameters:**  
    - `connection`: The SQLite connection object.
    - `incident_data`: A list of dictionaries containing the incident data to insert.

- **`summarize_incident_natures(connection)`**  
  - Summarizes and prints the counts of each incident type in the database.
  - **Parameters:**  
    - `connection`: The SQLite connection object.

## Running Tests

- The project includes four test cases:  
    - `test_download`: Verifies that the PDF is downloaded correctly from the URL, with the file stored in the `test_files` directory.  
    - `test_extract`: Ensures that the extraction method in `req.py` accurately retrieves incidents in dictionary format.  
    - `test_database`: Confirms that the database is created successfully and that all incidents are populated correctly.  
    - `test_analyze`: Tests the accuracy of the incident nature counts.  

- To run all the tests in the project, execute:
   ```bash
   pipenv run pytest -v
   ```

## Bugs and Assumptions

- **Assumptions:**
  - The incident report PDF is expected to follow a consistent format.
  - The script assumes that the PDF content can be extracted without encountering formatting or encoding issues.
  - Locations may contain uppercase letters, numbers, and specific punctuation (such as hyphens, periods, semicolons, spaces, and commas).
  - Nature descriptions are assumed to be free of special characters.
  - Words may be separated by spaces or slashes to indicate multiple incident types (e.g., "Theft / Burglary").
  - Ignoring the locations that are in multiple lines as we dont need them in our functinality.

- **Bugs:**
  - Should the PDF structure change, the regex patterns may require updating to maintain accuracy in data extraction.
  - The script currently does not handle potential errors, such as network failures during PDF download, missing fields in the PDF, or issues with malformed PDFs.


## Demo

[Project Demo](https://youtu.be/VY0aQRCT_2w)



