# CRACK THE CODE

CRACK THE CODE is a Django-based programming learning platform for beginner-friendly tutorials, practice exercises, coding challenges, and progress tracking.

## Features

- Responsive landing page and navigation
- Multi-language learning pages for HTML, CSS, Python, Java, and C
- Interactive coding playground with safe execution hooks
- Coding challenge listing with filters and difficulty levels
- User authentication, dashboard, settings, and progress tracking
- SQLite by default and PostgreSQL-ready configuration

## Local setup

1. Create and activate a virtual environment:
   - `python -m venv .venv`
   - `.venv\Scripts\activate`
2. Install dependencies:
   - `pip install -r requirements.txt`
3. Apply database migrations:
   - `python manage.py migrate`
4. Load demo content:
   - `python manage.py seed_data`
5. Start the server:
   - `python manage.py runserver`

## Secure execution service

The app includes code-execution hooks for Python, Java, and C. The service is intentionally not invoked directly in Django or on the host OS. Configure the following environment variables to enable external execution:

- `EXECUTION_SERVICE_URL`
- `EXECUTION_SERVICE_TOKEN`

If these values are not set, the playground will clearly report that execution is not configured.

## License

This project is distributed under the MIT license.
