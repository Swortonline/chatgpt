FROM python:3.10-slim-bullseye

WORKDIR /app/
COPY . .

RUN pip3 install -r requirements.txt

RUN apt update; apt-get install -yy apache2

CMD ["bash","run.sh"]

EXPOSE 9080
