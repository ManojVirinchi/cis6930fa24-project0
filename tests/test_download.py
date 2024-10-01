import pytest
from project0.req import fetch_pdf_from_url
from io import BytesIO
import os

def test_download_pdf():
    # URL of the PDF to download for testing
    test_url = "https://www.normanok.gov/sites/default/files/documents/2024-08/2024-08-01_daily_incident_summary.pdf"
    
    # Use the download_pdf function to download the PDF
    pdf_file = fetch_pdf_from_url(test_url)
    
    # Test if the download_pdf function returns a valid BytesIO object
    assert isinstance(pdf_file, BytesIO), "download_pdf did not return a BytesIO object."
    
    # Test if the BytesIO object contains content (not empty)
    assert pdf_file.getbuffer().nbytes > 0, "Downloaded PDF is empty."
