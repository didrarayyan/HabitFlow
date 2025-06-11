#!/bin/bash

# HabitFlow Production Deployment Script
# This script deploys HabitFlow to production

set -e

echo "🚀 Deploying HabitFlow to production..."

# Configuration
DOMAIN=${DOMAIN:-"your-domain.com"}
EMAIL=${EMAIL:-"admin@your-domain.com"}
ENVIRONMENT=${ENVIRONMENT:-"production"}

# Check if required environment variables are set
if [ "$DOMAIN" = "your-domain.com" ]; then
    echo "❌ Please set the DOMAIN environment variable"
    echo "   Example: DOMAIN=habitflow.com ./scripts/deploy-prod.sh"
    exit 1
fi

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Create production environment file if it doesn't exist
if [ ! -f infra/.env.production ]; then
    echo "❌ Production environment file not found at infra/.env.production"
    echo "   Please create this file with your production configuration."
    exit 1
fi

# Create SSL certificates directory
mkdir -p infra/ssl

# Generate SSL certificates with Let's Encrypt (if certbot is available)
if command -v certbot &> /dev/null; then
    echo "🔒 Generating SSL certificates..."
    certbot certonly --standalone -d $DOMAIN -d www.$DOMAIN --email $EMAIL --agree-tos --non-interactive
    
    # Copy certificates to nginx directory
    cp /etc/letsencrypt/live/$DOMAIN/fullchain.pem infra/ssl/
    cp /etc/letsencrypt/live/$DOMAIN/privkey.pem infra/ssl/
else
    echo "⚠️ Certbot not found. SSL certificates will need to be configured manually."
fi

# Create production nginx configuration
cat > infra/nginx/nginx.conf << EOF
events {
    worker_connections 1024;
}

http {
    upstream backend {
        server backend:8000;
    }

    upstream frontend {
        server frontend:80;
    }

    server {
        listen 80;
        server_name $DOMAIN www.$DOMAIN;
        return 301 https://\$server_name\$request_uri;
    }

    server {
        listen 443 ssl http2;
        server_name $DOMAIN www.$DOMAIN;

        ssl_certificate /etc/nginx/ssl/fullchain.pem;
        ssl_certificate_key /etc/nginx/ssl/privkey.pem;

        location /api/ {
            proxy_pass http://backend/api/;
            proxy_set_header Host \$host;
            proxy_set_header X-Real-IP \$remote_addr;
            proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto \$scheme;
        }

        location / {
            proxy_pass http://frontend/;
            proxy_set_header Host \$host;
            proxy_set_header X-Real-IP \$remote_addr;
            proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto \$scheme;
        }
    }
}
EOF

# Build and deploy with Docker Compose
echo "🐳 Building and deploying containers..."
docker-compose -f infra/docker-compose.yml --env-file infra/.env.production build
docker-compose -f infra/docker-compose.yml --env-file infra/.env.production up -d --remove-orphans

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 30

# Run database migrations
echo "🗄️ Running database migrations..."
docker-compose -f infra/docker-compose.yml exec backend python -c "
from app.core.database import create_tables
import asyncio
asyncio.run(create_tables())
print('Database tables created successfully!')
"

# Create initial admin user
echo "👤 Creating initial admin user..."
docker-compose -f infra/docker-compose.yml exec backend python -c "
from app.services.user_service import UserService
from app.core.database import SessionLocal
from app.schemas.user import UserCreate
import os

db = SessionLocal()
user_service = UserService(db)

admin_email = os.getenv('FIRST_SUPERUSER', 'admin@habitflow.com')
admin_password = os.getenv('FIRST_SUPERUSER_PASSWORD', 'admin123')

existing_user = user_service.get_by_email(email=admin_email)
if not existing_user:
    admin_user = UserCreate(
        email=admin_email,
        password=admin_password,
        full_name='Admin User',
        is_active=True
    )
    user = user_service.create(obj_in=admin_user)
    print(f'Admin user created: {user.email}')
else:
    print(f'Admin user already exists: {existing_user.email}')

db.close()
"

# Setup log rotation
echo "📝 Setting up log rotation..."
cat > /etc/logrotate.d/habitflow << EOF
/var/lib/docker/containers/*/*.log {
    daily
    missingok
    rotate 7
    compress
    notifempty
    create 0644 root root
    postrotate
        docker kill --signal="USR1" \$(docker ps -q) 2>/dev/null || true
    endscript
}
EOF

# Setup automatic SSL renewal (if certbot is available)
if command -v certbot &> /dev/null; then
    echo "🔄 Setting up automatic SSL renewal..."
    (crontab -l 2>/dev/null; echo "0 12 * * * /usr/bin/certbot renew --quiet --post-hook 'docker-compose -f /path/to/habitflow/infra/docker-compose.yml restart nginx'") | crontab -
fi

echo "✅ Production deployment complete!"
echo ""
echo "🎉 HabitFlow is now running at:"
echo "   https://$DOMAIN"
echo "   https://www.$DOMAIN"
echo ""
echo "📊 Monitor the application:"
echo "   Logs: docker-compose -f infra/docker-compose.yml logs -f"
echo "   Status: docker-compose -f infra/docker-compose.yml ps"
echo ""
echo "🔧 Management commands:"
echo "   Stop: docker-compose -f infra/docker-compose.yml down"
echo "   Restart: docker-compose -f infra/docker-compose.yml restart"
echo "   Update: git pull && docker-compose -f infra/docker-compose.yml up -d --build"

