import pytest
import sqlite3
from project0.req import setup_incident_database, populate_database_with_data

def test_create_database():
    # Create the database
    conn = setup_incident_database()
    c = conn.cursor()
    
    # Check if the 'incidents' table exists
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='incidents';")
    table_exists = c.fetchone()
    assert table_exists is not None, "Table 'incidents' was not created."
    
    conn.close()

def test_insert_data():
    conn = setup_incident_database()
    
    # Example data to insert
    data = [{'date_time': '08/01/2024 14:30', 'incident_number': '2024-12345678', 'location': 'MAIN ST', 'nature': 'THEFT', 'incident_ori': 'OK12345'}]
    
    # Insert the data
    populate_database_with_data(conn, data)
    
    # Verify data insertion
    c = conn.cursor()
    c.execute("SELECT * FROM incidents WHERE incident_number='2024-12345678'")
    row = c.fetchone()
    
    assert row is not None, "Data was not inserted."
    assert row[1] == '2024-12345678', "Inserted data does not match the expected result."
    
    conn.close()
