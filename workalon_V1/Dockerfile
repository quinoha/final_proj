FROM python:3.10

ENV PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive
    
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENTRYPOINT ["python", "main_pc_session.py"]
CMD ["--routine", "auto"]