FROM alpine:latest

COPY cloudflare-ddns.py /app/
COPY config.yaml /app/
COPY requirements.txt /app/

RUN apk add --no-cache python3 && \
    apk add --update py3-pip && \
    pip install --upgrade pip && \
    pip install -r /app/requirements.txt

WORKDIR /app

CMD ["python3", "cloudflare-ddns.py"]
