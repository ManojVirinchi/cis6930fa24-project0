import requests
import sqlite3
import re
from io import BytesIO
from pypdf import PdfReader
from req import setup_incident_database, populate_database_with_data, fetch_pdf_from_url, extract_incident_data, summarize_incident_natures
import argparse

def main():
    
    parser = argparse.ArgumentParser(description="Process incident report PDF URL.")
    parser.add_argument('--incidents', type=str, help="URL of the PDF file to process")
    args = parser.parse_args()

    if args.incidents:
        url = args.incidents
        
        try:
            #print("Downloading PDF...")
            pdf_file = fetch_pdf_from_url(url)
            #print("PDF downloaded successfully.")
            
            #print("Extracting data...")
            data = extract_incident_data(pdf_file)
            
            #print(f"Extracted {len(data)} incidents from the PDF.")
            
            #print("Creating database...")
            conn = setup_incident_database()
            
            #print("Inserting data into database...")
            populate_database_with_data(conn, data)
            
            #print("\nNature occurrences:")
            summarize_incident_natures(conn)
            
            conn.close()
        except Exception as e:
            print(f"An error occurred: {str(e)}")
    else:
        print("Please provide a URL with --incidents")

if __name__ == "__main__":
    main()
