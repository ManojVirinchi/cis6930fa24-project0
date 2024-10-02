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

def extract_pdf_data(pdf_reader):
    complete_incident_records = []
    incomplete_row_buffer = ''
    header_keywords = ('Date / Time', 'Daily Incident Summary (Public)')
    incident_ori_endings = ('EMSSTAT', 'OK0140200', '14005', '14009')

    def is_header_row(row):
        return any(row.startswith(keyword) for keyword in header_keywords)

    def is_complete_incident(row):
        return any(row.endswith(ending) for ending in incident_ori_endings)

    for page in pdf_reader.pages:
        text_rows = page.extract_text().split('\n')

        for current_row in text_rows:
            if "NORMAN POLICE DEPARTMENT" in current_row:
                 current_row=re.sub(r"NORMAN POLICE DEPARTMENT", "", current_row)
            
            if is_header_row(current_row):
                continue
            if is_complete_incident(current_row):
                if incomplete_row_buffer:
                    current_row = f"{incomplete_row_buffer} {current_row}"
                    incomplete_row_buffer = ''
                current_row = re.sub(r"NORMAN POLICE DEPARTMENT", "", current_row)
                complete_incident_records.append(current_row.strip())
            else:
                incomplete_row_buffer = f"{incomplete_row_buffer} {current_row.strip()}".strip()

    if incomplete_row_buffer:
        incomplete_row_buffer = re.sub(r"NORMAN POLICE DEPARTMENT", "", incomplete_row_buffer)
        complete_incident_records.append(incomplete_row_buffer)

    return complete_incident_records

# Function to extract incident data from the PDF content
def extract_incident_data(pdf_file):
    #print("Starting PDF data extraction...")
    pdf_reader = PdfReader(pdf_file)
    complete_incident_records = extract_pdf_data(pdf_reader)
    incident_records = []

    date_time_pattern = r'(\d{1,2}/\d{1,2}/\d{4}\s+\d{1,2}:\d{2})'
    incident_number_pattern = r'(2024-\d+)'
    location_pattern = r'((?:[A-Z\d]+[\-\.\; \/\,\<\>]*)+)' 
    nature_pattern = r'((?:\b[A-Za-z]+\b(?:[\/\- ]*)?)+)' 
    incident_ori_pattern = r'(OK\d+|EMSSTAT|14005)'

    full_incident_pattern = f"{date_time_pattern}\\s+{incident_number_pattern}\\s*{location_pattern}\\s+{nature_pattern}\\s+{incident_ori_pattern}"

    for record in complete_incident_records:

        # record.replace('NORMAN POLICE DEPARTMENT', '')
        print(record)
        match = re.match(full_incident_pattern, record)
        if match:
            date_time, incident_number, original_location, original_nature, incident_ori = match.groups()
            combined_location_nature = f'{original_location.strip()} {original_nature.strip()}'
            #print(f"\n>>> Combined location and nature: '{combined_location_nature}' <<<\n")
            
            special_words = [' MVA ', ' COP ', ' 911 ']
            location, nature = smart_split(combined_location_nature, special_words, original_location, original_nature)

            #print(f"Location after split: '{location}'")
            #print(f"Nature after split: '{nature}'")
            matchN = re.match(r'([A-Z]+)([A-Z][a-z].*)', nature)
            if matchN:
                prev, nxt = matchN.groups()
                nature = nxt.strip()
                location += " " + prev
            

            incident_records.append({
                'date_time': date_time.strip(),
                'incident_number': incident_number.strip(),
                'location': location,
                'nature': nature,
                'incident_ori': incident_ori.strip()
            })
        #else:
            #print("log: "+record)

    #print(f"Extraction complete. Total number of rows extracted: {len(incident_records)}")
    return incident_records

def smart_split(combined_string, special_words, original_location, original_nature):
    indices = [combined_string.find(word) for word in special_words if word in combined_string]
    
    if indices:
        split_index = min(indices)
        location = combined_string[:split_index].strip()
        nature = combined_string[split_index:].strip()
        return location, nature
    else:
        return original_location.strip(), original_nature.strip()

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