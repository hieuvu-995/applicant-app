# Act FX API Project

## Technologies

- Pypy3.6-7.0.0
- Django 3.0.4
- PostgreSQL database
- Swagger (API Document)

## Run Server

1. Create `.env` file, example: `.env.template`
2. Start Server:

  ```
  git submodule sync --recursive
  git submodule update --init --recursive --remote
  docker-compose up -d
  ```

## Run Unit Test

  ```
  docker-compose run web pypy3 manage.py test -v 2
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

Run `scripts/build.sh` to packing source into `dist/management-api-front.zip`:

 ```bash
 ./scripts/build.sh
 ```

## Happly Coding!
