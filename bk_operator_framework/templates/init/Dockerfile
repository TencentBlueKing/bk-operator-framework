FROM python:3.12.6-alpine

WORKDIR /workspace

COPY main.py main.py
COPY api/ api/
COPY internal/ internal/
COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

CMD ["python", "main.py", "run"]