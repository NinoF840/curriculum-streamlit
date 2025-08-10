# 🚀 Nino Medical AI Pro - Guida Deploy

Guida completa per il deploy di Nino Medical AI Pro su diverse piattaforme.

## 📋 Requisiti di Sistema

### Minimi
- **CPU**: 2 core
- **RAM**: 4 GB
- **Storage**: 10 GB liberi
- **Network**: Connessione internet stabile
- **OS**: Linux/Windows/macOS con Docker

### Raccomandati
- **CPU**: 4+ core
- **RAM**: 8+ GB
- **Storage**: 20+ GB SSD
- **Network**: 100+ Mbps
- **OS**: Linux Ubuntu 20.04+ / CentOS 8+

## 🐳 Deploy con Docker

### 1. Deploy Locale (Sviluppo)

```bash
# Clona repository
git clone https://github.com/tuousername/nino-medical-ai.git
cd nino-medical-ai

# Build immagine
docker build -t nino-medical-ai:latest .

# Esegui container
docker run -d \
  --name nino-medical-ai \
  -p 8501:8501 \
  -v $(pwd)/cache:/app/cache \
  -v $(pwd)/auth:/app/auth \
  nino-medical-ai:latest
```

### 2. Deploy Completo (Docker Compose)

```bash
# Deploy base
docker-compose up -d

# Deploy con monitoring
docker-compose --profile monitoring up -d

# Deploy produzione con proxy
docker-compose --profile production up -d

# Verifica servizi
docker-compose ps
docker-compose logs nino-medical-ai
```

### 3. Configurazione Ambiente

Crea file `.env`:

```env
# Database
POSTGRES_USER=ninomed_user
POSTGRES_PASSWORD=your_secure_password
POSTGRES_DB=ninomedical

# Redis
REDIS_PASSWORD=your_redis_password

# App
SECRET_KEY=your_secret_key_here
DEBUG=false
ALLOWED_HOSTS=localhost,yourdomain.com

# SSL (opzionale)
SSL_CERT_PATH=/path/to/cert.pem
SSL_KEY_PATH=/path/to/key.pem
```

## ☁️ Deploy su Cloud

### 1. Streamlit Cloud (Consigliato per demo)

1. **Prepara Repository**:
   ```bash
   # Crea requirements.txt ottimizzato per cloud
   pip freeze > requirements.txt
   
   # Aggiungi secrets.toml in .streamlit/
   mkdir -p .streamlit
   echo '[general]' > .streamlit/secrets.toml
   echo 'SECRET_KEY = "your_secret_key"' >> .streamlit/secrets.toml
   ```

2. **Deploy su Streamlit Cloud**:
   - Vai su [share.streamlit.io](https://share.streamlit.io)
   - Connetti GitHub repository
   - Seleziona `nino_medical_ai_app.py` come main file
   - Configura secrets in dashboard

3. **Configurazione Streamlit Cloud**:
   ```toml
   # .streamlit/config.toml
   [server]
   headless = true
   port = 8501
   enableCORS = false
   
   [theme]
   base = "light"
   primaryColor = "#1f4e79"
   ```

### 2. Heroku

1. **Prepara per Heroku**:
   ```bash
   # Crea Procfile
   echo "web: streamlit run nino_medical_ai_app.py --server.port=\$PORT --server.address=0.0.0.0" > Procfile
   
   # Crea runtime.txt
   echo "python-3.11.7" > runtime.txt
   ```

2. **Deploy**:
   ```bash
   # Installa Heroku CLI e login
   heroku create nino-medical-ai-pro
   heroku buildpacks:set heroku/python
   
   # Configure environment variables
   heroku config:set SECRET_KEY=your_secret_key
   heroku config:set DEBUG=false
   
   # Deploy
   git add .
   git commit -m "Deploy to Heroku"
   git push heroku main
   ```

### 3. Google Cloud Run

1. **Prepara per Cloud Run**:
   ```bash
   # Build e push immagine
   gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/nino-medical-ai
   
   # Deploy su Cloud Run
   gcloud run deploy nino-medical-ai \
     --image gcr.io/YOUR_PROJECT_ID/nino-medical-ai \
     --platform managed \
     --region europe-west1 \
     --allow-unauthenticated \
     --port 8501 \
     --memory 2Gi \
     --cpu 2
   ```

2. **Configurazione avanzata**:
   ```yaml
   # cloudbuild.yaml
   steps:
     - name: 'gcr.io/cloud-builders/docker'
       args: ['build', '-t', 'gcr.io/$PROJECT_ID/nino-medical-ai', '.']
     - name: 'gcr.io/cloud-builders/docker'
       args: ['push', 'gcr.io/$PROJECT_ID/nino-medical-ai']
     - name: 'gcr.io/cloud-builders/gcloud'
       args:
         - 'run'
         - 'deploy'
         - 'nino-medical-ai'
         - '--image=gcr.io/$PROJECT_ID/nino-medical-ai'
         - '--region=europe-west1'
         - '--platform=managed'
         - '--allow-unauthenticated'
   ```

### 4. AWS ECS/Fargate

1. **Crea task definition**:
   ```json
   {
     "family": "nino-medical-ai",
     "networkMode": "awsvpc",
     "requiresCompatibilities": ["FARGATE"],
     "cpu": "2048",
     "memory": "4096",
     "executionRoleArn": "arn:aws:iam::ACCOUNT:role/ecsTaskExecutionRole",
     "containerDefinitions": [
       {
         "name": "nino-medical-ai",
         "image": "your-account.dkr.ecr.region.amazonaws.com/nino-medical-ai:latest",
         "portMappings": [{"containerPort": 8501, "protocol": "tcp"}],
         "environment": [
           {"name": "STREAMLIT_SERVER_PORT", "value": "8501"}
         ]
       }
     ]
   }
   ```

2. **Deploy con AWS CLI**:
   ```bash
   # Build e push su ECR
   aws ecr get-login-password --region region | docker login --username AWS --password-stdin your-account.dkr.ecr.region.amazonaws.com
   docker build -t nino-medical-ai .
   docker tag nino-medical-ai:latest your-account.dkr.ecr.region.amazonaws.com/nino-medical-ai:latest
   docker push your-account.dkr.ecr.region.amazonaws.com/nino-medical-ai:latest
   
   # Crea servizio ECS
   aws ecs create-service --cluster your-cluster --service-name nino-medical-ai --task-definition nino-medical-ai --desired-count 2
   ```

## 🔧 Configurazione Produzione

### 1. Reverse Proxy (Nginx)

```nginx
# /etc/nginx/sites-available/nino-medical-ai
server {
    listen 80;
    server_name yourdomain.com;
    
    # Redirect to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com;
    
    # SSL configuration
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    
    # Security headers
    add_header X-Frame-Options DENY;
    add_header X-Content-Type-Options nosniff;
    add_header X-XSS-Protection "1; mode=block";
    
    # Proxy to Streamlit
    location / {
        proxy_pass http://127.0.0.1:8501;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # WebSocket support
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        
        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
}
```

### 2. SSL Certificate (Let's Encrypt)

```bash
# Installa Certbot
sudo apt update
sudo apt install certbot python3-certbot-nginx

# Ottieni certificato
sudo certbot --nginx -d yourdomain.com

# Auto-renewal
sudo crontab -e
# Aggiungi: 0 12 * * * /usr/bin/certbot renew --quiet
```

### 3. Monitoring e Logging

```yaml
# docker-compose.monitoring.yml
version: '3.8'
services:
  # Log aggregation con ELK Stack
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:8.11.0
    environment:
      - discovery.type=single-node
      - "ES_JAVA_OPTS=-Xms512m -Xmx512m"
    volumes:
      - elasticsearch-data:/usr/share/elasticsearch/data
    ports:
      - "9200:9200"

  kibana:
    image: docker.elastic.co/kibana/kibana:8.11.0
    ports:
      - "5601:5601"
    environment:
      - ELASTICSEARCH_HOSTS=http://elasticsearch:9200

  # Application Performance Monitoring
  apm-server:
    image: docker.elastic.co/apm/apm-server:8.11.0
    depends_on:
      - elasticsearch
    ports:
      - "8200:8200"
    environment:
      - output.elasticsearch.hosts=["elasticsearch:9200"]
```

## 📊 Monitoraggio e Maintenance

### 1. Health Checks

```bash
# Verifica salute applicazione
curl -f http://localhost:8501/_stcore/health

# Verifica metriche
curl http://localhost:8501/_stcore/metrics

# Monitor logs
docker logs -f nino-medical-ai
```

### 2. Backup Automatico

```bash
#!/bin/bash
# backup-script.sh

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backup/nino-medical-ai"

# Database backup
docker exec nino-medical-postgres pg_dump -U ninomed_user ninomedical > "$BACKUP_DIR/db_$DATE.sql"

# Application data backup
tar -czf "$BACKUP_DIR/data_$DATE.tar.gz" \
  ./cache \
  ./auth \
  ./models \
  ./exports

# Clean old backups (keep 7 days)
find $BACKUP_DIR -name "*.sql" -mtime +7 -delete
find $BACKUP_DIR -name "*.tar.gz" -mtime +7 -delete

echo "Backup completed: $DATE"
```

### 3. Update Strategy

```bash
# Zero-downtime update
#!/bin/bash
# update-script.sh

echo "Starting rolling update..."

# Pull new image
docker-compose pull nino-medical-ai

# Recreate with new image
docker-compose up -d --no-deps --force-recreate nino-medical-ai

# Verify health
sleep 30
if curl -f http://localhost:8501/_stcore/health; then
    echo "Update successful"
    # Clean old images
    docker image prune -f
else
    echo "Update failed, rolling back..."
    docker-compose down
    docker-compose up -d
fi
```

## 🔒 Security Best Practices

### 1. Container Security

```dockerfile
# Usa immagini base sicure
FROM python:3.11.7-slim

# Non eseguire come root
USER nonroot

# Scansiona vulnerabilità
RUN apt-get update && apt-get upgrade -y
```

### 2. Network Security

```yaml
# Firewall rules
- ufw allow 22/tcp      # SSH
- ufw allow 80/tcp      # HTTP
- ufw allow 443/tcp     # HTTPS
- ufw deny 8501/tcp     # Block direct Streamlit access
- ufw enable
```

### 3. Data Protection

```python
# Encryption at rest
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'OPTIONS': {
            'sslmode': 'require',
            'sslcert': 'client-cert.pem',
            'sslkey': 'client-key.pem',
            'sslrootcert': 'ca-cert.pem',
        }
    }
}
```

## 🧪 Testing Deploy

### 1. Smoke Tests

```bash
# Test delle funzionalità base
curl -X GET http://localhost:8501/_stcore/health
curl -X GET http://localhost:8501/

# Test autenticazione
curl -X POST http://localhost:8501/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"test","password":"test"}'
```

### 2. Load Testing

```bash
# Usando Apache Bench
ab -n 1000 -c 10 http://localhost:8501/

# Usando wrk
wrk -t12 -c400 -d30s http://localhost:8501/
```

## 📞 Support e Troubleshooting

### Common Issues

1. **Container won't start**:
   ```bash
   docker logs nino-medical-ai
   docker exec -it nino-medical-ai bash
   ```

2. **Memory issues**:
   ```bash
   docker stats
   # Increase memory limits in docker-compose.yml
   ```

3. **Database connection**:
   ```bash
   docker exec -it nino-medical-postgres psql -U ninomed_user -d ninomedical
   ```

### 📧 Contacts

- **Email**: ninomedical.ai@gmail.com
- **GitHub**: [Repository Issues](https://github.com/tuousername/nino-medical-ai/issues)
- **Documentation**: [Wiki](https://github.com/tuousername/nino-medical-ai/wiki)

---

© 2025 Antonino Piacenza - Nino Medical AI Pro
