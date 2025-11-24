# ohtuvarasto

[![GHA workflow badge](https://github.com/haikoj/ohtuvarasto/actions/workflows/main.yml/badge.svg)](https://github.com/haikoj/ohtuvarasto/actions)
[![codecov](https://codecov.io/github/haikoj/ohtuvarasto/graph/badge.svg?token=2Q5K38Y3EP)](https://codecov.io/github/haikoj/ohtuvarasto)

A warehouse/storage management application with a web-based user interface.

## Features

- Create and manage multiple warehouses
- Add and remove items from warehouses
- Track warehouse capacity and available space
- Edit warehouse properties with validation
- User-friendly web interface built with Flask

## Installation

1. Install dependencies:
```bash
poetry install
```

## Running the Application

### Web Interface

Start the Flask web server:
```bash
cd src
poetry run python app.py
```

Then open your browser and navigate to `http://127.0.0.1:5000`

### Command Line Demo

Run the original command-line demo:
```bash
poetry run python src/index.py
```

## Testing

Run tests:
```bash
poetry run pytest
```

Run tests with coverage:
```bash
poetry run coverage run -m pytest
poetry run coverage report
```

## Linting

Run pylint:
```bash
poetry run pylint src/
```

## Development Notes

- The Flask app runs in debug mode for development purposes only
- The secret key is hardcoded for development; use environment variables in production
- For production deployment, use a WSGI server like gunicorn instead of the Flask development server
