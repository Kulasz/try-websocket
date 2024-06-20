FROM python:3.12-slim

WORKDIR /usr/application

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc curl gnupg2 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY poetry.lock poetry.lock
COPY pyproject.toml pyproject.toml
COPY ./src src

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Add Poetry to PATH
ENV PATH="${PATH}:/root/.local/bin"

RUN poetry install --without=dev --no-interaction --no-ansi

EXPOSE 80

CMD ["poetry", "run", "fastapi", "run", "./src/traiding_app/main.py", "--port", "80"]