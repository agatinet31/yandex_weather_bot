FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN apt-get update && \
    pip3 install -r requirements.txt --no-cache-dir && \
    apt-get clean && \
    apt-get autoremove -y && \
    rm -rf /var/lib/apt/lists/*

CMD ["gunicorn", "yandex_weather.wsgi:application", "--bind", "0:8000" ]
