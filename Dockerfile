FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .


RUN python manage.py migrate
RUN python manage.py collectstatic --noinput


EXPOSE 8000


CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]