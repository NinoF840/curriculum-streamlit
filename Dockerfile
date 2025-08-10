# Nino Medical AI Pro - Dockerfile
# Multi-stage build per ottimizzare dimensione finale

# Stage 1: Builder
FROM python:3.11.7-slim as builder

# Informazioni del maintainer
LABEL maintainer="Antonino Piacenza <ninomedical.ai@gmail.com>"
LABEL version="1.0"
LABEL description="Nino Medical AI Pro - Piattaforma IA per applicazioni mediche"

# Variabili ambiente per build
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    DEBIAN_FRONTEND=noninteractive

# Installa dipendenze di sistema per build
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    g++ \
    libffi-dev \
    libssl-dev \
    libxml2-dev \
    libxslt1-dev \
    zlib1g-dev \
    libjpeg-dev \
    libpng-dev \
    libfreetype6-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Crea utente non-root per security
RUN useradd --create-home --shell /bin/bash ninomed

# Directory lavoro
WORKDIR /app

# Copia requirements e installa dipendenze Python
COPY requirements.txt .
RUN pip install --user --no-warn-script-location -r requirements.txt

# Stage 2: Runtime
FROM python:3.11.7-slim as runtime

# Variabili ambiente per runtime
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/home/ninomed/.local/bin:$PATH" \
    STREAMLIT_SERVER_PORT=8501 \
    STREAMLIT_SERVER_ADDRESS=0.0.0.0 \
    STREAMLIT_BROWSER_GATHER_USAGE_STATS=false \
    STREAMLIT_THEME_BASE=light

# Installa solo runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libffi8 \
    libssl3 \
    libxml2 \
    libxslt1.1 \
    zlib1g \
    libjpeg62-turbo \
    libpng16-16 \
    libfreetype6 \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get autoremove -y \
    && apt-get autoclean

# Crea utente non-root
RUN useradd --create-home --shell /bin/bash --uid 1000 ninomed

# Copia dipendenze Python dal builder
COPY --from=builder --chown=ninomed:ninomed /home/ninomed/.local /home/ninomed/.local

# Directory applicazione
WORKDIR /app
RUN chown ninomed:ninomed /app

# Cambia a utente non-root
USER ninomed

# Copia codice applicazione
COPY --chown=ninomed:ninomed . .

# Crea directory necessarie
RUN mkdir -p cache auth models assets screenshots logs

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

# Esponi porta Streamlit
EXPOSE 8501

# Comando di avvio
CMD ["streamlit", "run", "nino_medical_ai_app.py", "--server.address", "0.0.0.0", "--server.port", "8501", "--browser.gatherUsageStats", "false"]
