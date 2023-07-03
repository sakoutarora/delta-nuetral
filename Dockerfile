FROM python:3.9-slim

RUN mkdir /app
COPY requirement.txt app/requirement.txt
COPY main.py /app

WORKDIR /app

RUN apt-get update && apt-get install -y python3 python3-pip sudo
RUN pip3 install -r requirement.txt

CMD ["python", "main.py"]