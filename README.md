# Bulk Certificate Generator API

A backend API that accepts a bulk certificate generation request and generates individual PDF certificates for multiple recipients.

## Features

- Bulk certificate generation using a single API request
- Recipient data validation
- Background processing
- Job status and progress tracking
- Individual certificate success/failure tracking
- Generated PDF certificate retrieval
- SQLite database for job and certificate tracking
- Automated API tests
- FastAPI interactive API documentation

## Tech Stack

- Python
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- ReportLab
- Pytest
- Uvicorn

## Project Structure

```text
Aereo_Bulk_Certificate/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── services.py
│   └── certificate_generator.py
│
├── tests/
│   ├── __init__.py
│   └── test_api.py
│
├── generated_certificates/
├── templates/
├── requirements.txt
├── .gitignore
└── README.md