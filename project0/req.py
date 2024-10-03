import requests
import sqlite3
import re
from io import BytesIO
import os
from pypdf import PdfReader

# Function to download the PDF from a given URL
def fetch_pdf_from_url(pdf_url):
    #print(f"Attempting to download PDF from: {pdf_url}")
    response = requests.get(pdf_url)
    
    if response.status_code == 200:
        #print("PDF downloaded successfully.")
        return BytesIO(response.content)
    else:
        error_message = f"Failed to download PDF. Status code: {response.status_code}"
        raise Exception(error_message)

def extract_incident_data(pdf_file):
    pdf_reader = PdfReader(pdf_file)
    incident_records = []

    for page in pdf_reader.pages:
        text = page.extract_text(extraction_mode="layout")
        lines = text.split('\n')
        
        for line in lines:
            if is_valid_incident_line(line):
                cleaned_line = clean_line(line)
                parts = split_line(cleaned_line)
                
                if len(parts) == 5:
                    incident_records.append(create_incident_dict(parts))

    #print(f"Total incidents extracted: {len(incident_records)}")
    return incident_records

def is_valid_incident_line(line):
    return line.strip() and not line.strip().startswith("Date / Time")

def clean_line(line):
    return line.replace("NORMAN POLICE DEPARTMENT", "").strip()

def split_line(line):
    return re.split(r'\s{2,}', line)

def create_incident_dict(parts):
    return {
        'date_time': parts[0],
        'incident_number': parts[1],
        'location': parts[2],
        'nature': parts[3],
        'incident_ori': parts[4]
    }
# Function to create an SQLite database and incidents table
def setup_incident_database():
    #print("Setting up SQLite database...")
    #resources_dir = os.path.join("/Users/manojvirinchichitta/DE/cis6930fa24-project0/", 'resources')
    #if not os.path.exists(resources_dir):
        #os.makedirs(resources_dir)
    
    #db_path = os.path.join(resources_dir, 'normanpd.db')
    connection = sqlite3.connect(os.path.abspath('resources/normanpd.db'))

    cursor = connection.cursor()
    
    #print("Dropping existing incidents table if it exists...")
    cursor.execute('DROP TABLE IF EXISTS incidents')
    
    #print("Creating new incidents table...")
    cursor.execute('''CREATE TABLE incidents
                      (date_time TEXT, incident_number TEXT, location TEXT, nature TEXT, incident_ori TEXT)''')
    connection.commit()
    #print("Database setup complete.")
    return connection

# Function to insert extracted incident data into the database
def populate_database_with_data(connection, incident_data):
    #print(f"Inserting {len(incident_data)} incident records into the database...")
    cursor = connection.cursor()
    
    cursor.executemany('''INSERT INTO incidents VALUES (:date_time, :incident_number, :location, :nature, :incident_ori)''', incident_data)
    connection.commit()
    #print("Data insertion complete.")

# Function to analyze and summarize incident nature data
def summarize_incident_natures(connection):
    #print("Analyzing incident nature occurrences...")
    cursor = connection.cursor()
    
    cursor.execute('''SELECT nature, COUNT(*) as count 
                      FROM incidents 
                      GROUP BY nature 
                      ORDER BY nature''')
    results = cursor.fetchall()
    
    #print(f"Total unique incident natures: {len(results)}")
    for nature, count in results:
        print(f"{nature}|{count}")