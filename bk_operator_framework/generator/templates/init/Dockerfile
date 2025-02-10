FROM python:3.12.6-alpine

WORKDIR /workspace

COPY main.py main.py
COPY api/ api/
COPY internal/ internal/
COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

# Please enter controller or webhook as service type
# More information can be found here: https://kopf.readthedocs.io/en/stable/cli/
CMD ["python", "main.py", "run", "{server_type}", "-A"]