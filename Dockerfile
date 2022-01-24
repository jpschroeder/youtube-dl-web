FROM ubuntu:20x04
MAINTAINER John Schroeder "john@schroederspace.com"
RUN apt-get update -y
RUN apt-get install -y python3-pip python-dev build-essential
COPY ./app /app
WORKDIR /app
RUN pip3 install -r requirements.txt
ENTRYPOINT ["python3"]
CMD ["main.py"]