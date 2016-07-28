FROM ubuntu:latest
MAINTAINER John Schroeder "john@schroederspace.com"
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential
COPY ./app /app
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["main.py"]