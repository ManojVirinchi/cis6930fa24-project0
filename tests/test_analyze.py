import pytest
import sqlite3
from io import StringIO
from unittest.mock import patch
from project0.req import setup_incident_database, populate_database_with_data, summarize_incident_natures

@patch('sys.stdout', new_callable=StringIO)
def test_analyze_nature(mock_stdout):
    conn = setup_incident_database()
    # Insert mock data
    data = [
        {'date_time': '08/01/2024 14:30', 'incident_number': '2024-12345678', 'location': 'MAIN ST', 'nature': 'THEFT', 'incident_ori': 'OK12345'},
        {'date_time': '08/01/2024 15:00', 'incident_number': '2024-12345679', 'location': 'OAK ST', 'nature': 'THEFT', 'incident_ori': 'OK12346'},
        {'date_time': '08/01/2024 16:00', 'incident_number': '2024-12345680', 'location': 'PINE ST', 'nature': 'ASSAULT', 'incident_ori': 'OK12347'}
    ]
    populate_database_with_data(conn, data)
    
    # Analyze nature counts
    summarize_incident_natures(conn)
    
    # Assert the output
    output = mock_stdout.getvalue().strip()
    assert "THEFT|2" in output
    assert "ASSAULT|1" in output
    
    conn.close()
