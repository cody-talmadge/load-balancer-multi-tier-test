FROM python:3.9-slim
WORKDIR /app
COPY . /app
RUN apt-get update
RUN apt-get install -y redis-server supervisor
RUN pip install -r requirements.txt
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
EXPOSE 80
CMD ["supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]