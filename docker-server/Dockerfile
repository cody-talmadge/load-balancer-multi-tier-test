FROM python:3.9-slim
WORKDIR /app
COPY . /app
RUN apt-get update
RUN apt-get install -y redis-server supervisor
RUN pip install -r requirements.txt
COPY serpervisord.conf /etc/supervisor/conf.d/supervisord.conf
EXPOSE 80
CMD ["gunicorn", "--workers", "2", "--threads", "10", "--bind", "0.0.0.0:80", "server:app"]