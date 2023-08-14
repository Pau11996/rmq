FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app_back

COPY Pipfile /app_back/
COPY Pipfile.lock /app_back/

COPY . /app_back/

RUN python -m pip install --upgrade pip
RUN pip install pipenv && pipenv install --deploy --system