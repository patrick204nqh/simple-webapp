FROM python:3.9-slim

RUN apt-get update && apt-get install -y \
    curl \
    netcat-traditional \
    net-tools \
    iputils-ping \
    dnsutils \
    nmap \
    telnet \
    supervisor \
    jq \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better Docker layer caching
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

WORKDIR /app

COPY app/ /app/
COPY config/supervisord.conf /etc/supervisor/conf.d/supervisord.conf
COPY scripts/entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh /app/scripts/*.sh

RUN mkdir -p /app/config

EXPOSE 80 61208

CMD ["/entrypoint.sh"]