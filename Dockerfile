FROM python:3.12-alpine AS builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt --user

FROM python:3.12-alpine

WORKDIR /app
RUN adduser -D appuser && \
    apk add --no-cache tini
USER appuser
COPY --from=builder /root/.local /home/appuser/.local
COPY src/ src/

ENV PATH=/home/appuser/.local/bin:$PATH \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

ENTRYPOINT ["/sbin/tini", "--"]
CMD ["python", "-m", "src.main"]
