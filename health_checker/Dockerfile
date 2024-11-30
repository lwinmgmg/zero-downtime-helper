FROM python:3.12-alpine

WORKDIR /build

RUN mkdir /build/data

RUN pip install requests

COPY find_and_replace.py .
COPY health_check.py .
COPY welcome.py .

CMD [ "python", "welcome.py"]
