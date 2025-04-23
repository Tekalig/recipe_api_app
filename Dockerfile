FROM python:alpine
LABEL maintainer="tekahazi.com"

ENV PYTHONUNBUFFERED 1

COPY ./requirements /tmp/requirements.txt
COPY ./launge /app
WORKDIR /app

EXPOSE 8000

RUN pip install --upgrade pip && \
    pip install -r /tmp/requirements.txt && \
    rm -rf /tmp && \
    adduser \
    --disabled-password \
    --no-create-home \
    django-user

ENV PATH="$PATH"

USER django-user