FROM python:3.11-slim
# Pracujeme přímo v /app
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
# Spouštíme uvicorn z kořene, kde najde složku app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

