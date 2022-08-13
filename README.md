# Applicant Management API Project

## Technologies

- Python 3.8.10
- Django 3.0.4
- PostgreSQL database
- Postman (API Document)

## Run Server

1. Create `environment` file, , example: `variables.env` ---for ubuntu system, `window-variables.txt` ---for window. 
   Config variables properties system
2. Run virtual environment, example: `virtualenv`
3. Install requirements library:
   ```
   pip install -r requirements.txt
   ```
4. Import environment varible:

   With ubuntu os:
   ```
   source varibles.env
   ```
   With window os:
   ```
   for /F %A in (window-variables.txt) do SET %A
   ```
  
5. Start Server:
- Run migrate data for fist run (or when change model related to database):
   ```
   python manage.py migrate
   ```  
   ```
   python manage.py makemigrations
   ```  

- Run server with port 8000 (default 8080):

   ```
   python manage.py runserver 8000
   ```  

## Generate 1000 dummy applicants

- Run `/scripts/dump_applicant.sh` for create dummy applicants via API request:

    ```bash
    ./scripts/dump_applicant.sh
    ```

## Coding convention

- You have to format your code using Black before create PR:

    ```bash
    ./scripts/format-code.sh
    ```
- **ALWAYS** follow PEP08 style guilde for Python code: [pep8.org](https://pep8.org) and [PEP8](https://www.python.org/dev/peps/pep-0008/)
- Pull Request must pass `flake8` linter:

    ```bash
    flake8 .
    ```

## Packing Source For Deployment

Run `scripts/build.sh` to packing source into `dist/applicant-api.zip`:

 ```bash
 ./scripts/build.sh
 ```
## API Document

Refer at: 
