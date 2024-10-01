import pytest
from project0.req import extract_incident_data
from io import BytesIO
import os

def test_extract_data():
    test_pdf_path = os.path.join('test_files', 'test_pdf.pdf')
    
    # Ensure the test PDF exists
    assert os.path.exists(test_pdf_path), "Test PDF file does not exist."
    
    with open(test_pdf_path, 'rb') as f:
        pdf_file = BytesIO(f.read())
    
    # Test data extraction from the PDF
    extracted_data = extract_incident_data(pdf_file)
    
    # Ensure that the extracted data is a list of dictionaries
    assert isinstance(extracted_data, list)
    assert len(extracted_data) > 0, "No data extracted from the PDF."
    
    # Ensure the keys are present in each extracted dictionary
    for incident in extracted_data:
        assert 'date_time' in incident
        assert 'incident_number' in incident
        assert 'location' in incident
        assert 'nature' in incident
        assert 'incident_ori' in incident
