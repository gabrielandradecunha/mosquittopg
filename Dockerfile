FROM python:3.9

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

#COPY requirements.txt ./
#RUN pip install --no-cache-dir -r requirements.txt

RUN pip install --upgrade pip
RUN pip install paho-mqtt psycopg2 python-dotenv

COPY . /app

COPY .env /app/

EXPOSE 1883

CMD ["python3", "main.py"]
