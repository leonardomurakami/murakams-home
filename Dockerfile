FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_CACHE_DIR=/tmp/uv_cache

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    libgobject-2.0-0 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libgdk-pixbuf-2.0-0 \
    libffi-dev \
    shared-mime-info \
    libcairo2 \
    libcairo-gobject2 \
    fontconfig \
    fonts-dejavu-core \
    nginx \
    supervisor \
    && rm -rf /var/lib/apt/lists/*

RUN pip install uv

COPY requirements.txt uv.lock ./

RUN uv pip install --system --no-cache-dir -r requirements.txt \
    && rm -rf $UV_CACHE_DIR

COPY . .

RUN rm -f /etc/nginx/sites-enabled/default
COPY nginx.conf /etc/nginx/sites-enabled/default
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

EXPOSE 80

HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:80/ || exit 1

CMD ["supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
