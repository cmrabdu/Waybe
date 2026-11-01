# WAY-BE: small production image (Flask + Gunicorn, SQLite built from the bundled CSV).
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 \
    WAYBE_DB=/data/waybe.db

RUN pip install --no-cache-dir flask==3.1.* gunicorn==23.* \
 && useradd --create-home --uid 10001 waybe \
 && mkdir /data && chown waybe /data

WORKDIR /app
COPY --chown=waybe mobility ./mobility

USER waybe
EXPOSE 8000

# Build the database once (from mobility/ugly.csv), then serve.
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "2", "--threads", "2", \
     "--timeout", "30", "--max-requests", "2000", "--max-requests-jitter", "200", \
     "--access-logfile", "-", "mobility.wsgi:application"]
