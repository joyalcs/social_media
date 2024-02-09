FROM python:3.11
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
WORKDIR /backend
COPY requirements.txt /backend/
RUN pip install --upgrade pip && pip install -r requirements.txt
COPY . /backend/
EXPOSE 8000
CMD ["sh", "-c", "python manage.py wait_for_db && python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
