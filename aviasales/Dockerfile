FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ app/
COPY main.py .
COPY RS_Via-3.xml RS_ViaOW.xml .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
