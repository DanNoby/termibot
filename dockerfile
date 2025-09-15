FROM python:3.10-slim

RUN pip install --no-cache-dir uv
WORKDIR /app

COPY requirements.txt .
RUN uv pip install --system -r requirements.txt 

COPY . .

EXPOSE 8000

CMD ["python", "app.py"] 
