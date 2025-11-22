#!/bin/bash

set -e

echo "🚀 Iniciando deploy no Amazon Linux 2..."

# --- Atualização e dependências ---
sudo yum update -y
sudo yum install -y python3 python3-venv python3-pip nginx git

# --- Ativar Nginx ---
sudo systemctl enable nginx
sudo systemctl start nginx

# --- Clonar projeto ---
if [ ! -d "back-end-capstone-project" ]; then
    git clone https://github.com/oEnzoRibas/back-end-capstone-project.git
fi

cd back-end-capstone-project

# --- Ambiente virtual ---
python3 -m venv venv
source venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt
pip install gunicorn

# --- Diretórios ---
APP_DIR=$(pwd)
SOCKET_PATH="$APP_DIR/app.sock"

# --- Criar serviço systemd ---
SERVICE_FILE=/etc/systemd/system/flaskapp.service

sudo bash -c "cat > $SERVICE_FILE" <<EOF
[Unit]
Description=Gunicorn for Flask App
After=network.target

[Service]
User=ec2-user
Group=nginx
WorkingDirectory=$APP_DIR
Environment='PATH=$APP_DIR/venv/bin'
ExecStart=$APP_DIR/venv/bin/gunicorn --workers 3 --bind unix:$SOCKET_PATH app:app

[Install]
WantedBy=multi-user.target
EOF

# --- Iniciar serviço ---
sudo systemctl daemon-reload
sudo systemctl start flaskapp
sudo systemctl enable flaskapp

# --- Configurar Nginx ---
NGINX_FILE=/etc/nginx/conf.d/flaskapp.conf

sudo bash -c "cat > $NGINX_FILE" <<EOF
server {
    listen 80;
    server_name _;

    location / {
        proxy_pass http://unix:$SOCKET_PATH;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF

sudo nginx -t
sudo systemctl restart nginx

echo "🎉 Deploy concluído com sucesso!"
echo "Acesse: http://SEU-IP"
