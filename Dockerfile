FROM python:3.10-slim

RUN apt-get update && apt-get install -y netcat-openbsd

RUN alias python=python3

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY entrypoint.sh /app/
RUN chmod +x /app/entrypoint.sh


COPY . .


EXPOSE 8000


# ENTRYPOINT ["/app/entrypoint.sh"]

# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
