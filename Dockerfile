FROM python:3.13-alpine

LABEL maintainer="tekahazi.com"

ENV PYTHONUNBUFFERED=1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./launge /app
WORKDIR /app

EXPOSE 8000

# Add debugging steps to identify the issue during the build process
RUN pip install --upgrade pip && \
    apk add --update --no-cache postgresql-client && \
    apk add --update --no-cache --virtual .tmp-build-deps \
    build-base postgresql-dev musl-dev && \
    pip install -r /tmp/requirements.txt && \
    rm -rf /tmp && \        
    apk del .tmp-build-deps && \
    adduser \
    --disabled-password \
    --no-create-home \
    django-user

ENV PATH="$PATH"

USER django-user