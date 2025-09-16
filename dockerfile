FROM python:3.11-slim

RUN pip install --no-cache-dir uv
WORKDIR /app

COPY requirements.txt .
RUN uv pip install --system -r requirements.txt 

COPY . .

CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
