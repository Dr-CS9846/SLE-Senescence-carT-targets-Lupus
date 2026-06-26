FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY scripts/ scripts/
COPY data/senmayo_125genes.csv data/senmayo_125genes.csv
# Raw GEO datasets must be mounted at runtime:
#   docker run -v /path/to/datasets:/app/datasets sle-pipeline
VOLUME /app/datasets
ENTRYPOINT ["python", "scripts/pipeline_complete.py"]
