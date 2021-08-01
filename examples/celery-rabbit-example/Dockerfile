FROM python:3.8.6-buster

ENV PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PYTHONDONTWRITEBYTECODE=1 \
  # pip:
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100

RUN apt-get update \
  && apt-get install --no-install-recommends -y \
    bash \
    build-essential \
    curl \
    gettext \
    git \
    libpq-dev \
    nano

WORKDIR /code

# Copy and install dependencies:
COPY requirements.txt /code/
RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r /code/requirements.txt

# Copy source files:
COPY . /code/
# COPY app.py /code/



