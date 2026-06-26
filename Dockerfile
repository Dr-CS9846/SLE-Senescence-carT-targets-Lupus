FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY scripts/ scripts/
COPY data/senmayo_125genes.csv data/senmayo_125genes.csv
COPY data/external_validation/ data/external_validation/
ENTRYPOINT ["python", "scripts/pipeline_complete.py"]
