# Udacity catalog project
A basic CRUD app for managing items in a catalog.

## Requirements
- Python 3.4+
## Running project
1. Install Python 3 pip and virtualenv on Ubuntu:
    ```bash
    sudo apt-get install python3-pip
    pip3 install virtualenv
    ```
2. Setup virtual environment:
    ```bash
    cd /path/to/project
    virtualenv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

3. Run project in debug mode.
    ```bash
    python manage.py generate_key
    cp example_google_auth.py instance/google_auth.py
    python manage.py create_tables
    python manage.py populate
    python manage.py runserver
    ```
## Notes
- Data can be accessed in JSON format at /api.
- instance/google_auth.py must exist and contain GOOGLE_CLIENT_ID and GOOGLE_SECRET, example_google_auth.py can be used, or a new ones can be generated at https://developers.google.com/identity/sign-in/web/.
- Run tests:
    ```bash
    cd /path/to/project
    source venv/bin/activate
    pytest tests