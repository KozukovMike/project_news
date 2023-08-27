FROM python:latest

WORKDIR /app

COPY requirements.txt .

RUN python -m pip install -r requirements.txt

RUN python -m dostoevsky download fasttext-social-network-model

EXPOSE 1276

COPY . .

CMD ["python", "brain.py"]