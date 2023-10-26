FROM python:3.9-alpine

WORKDIR /service

COPY . /service

RUN pip install -r /service/requirements.txt

CMD ["bof", "run", "server","{version}"]