FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libgthread-2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . .

RUN pip install --no-cache-dir pygame==2.6.1

ENV SDL_AUDIODRIVER=dummy
ENV DISPLAY=:0

CMD ["python3", "main.py"]
