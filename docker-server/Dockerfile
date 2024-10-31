FROM python:3.9-slim
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
EXPOSE 80
CMD ["gunicorn", "--workers", "2", "--threads", "10", "--bind", "0.0.0.0:80", "server:app"]