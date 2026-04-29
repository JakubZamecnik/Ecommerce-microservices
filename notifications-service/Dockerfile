FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
# Přidali jsme -u (unbuffered), to je jistota
CMD ["python", "-u", "main.py"]
