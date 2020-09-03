#!/bin/bash

PROJECT_NAME='linuxpolls'
WEBSITE_NAME='linuxpolls'
PROJECT_DIR=`pwd`
VENV_NAME='django_venv'
NWORKERS=3
DOMAIN='com'

# Check if .env and credentials.json exist
LP_ENV=${PROJECT_DIR}/${PROJECT_NAME}/.env
GSA_CRED=${PROJECT_DIR}/${PROJECT_NAME}/credentials.json
if [ -f "$LP_ENV" -a -f "$GSA_CRED" ]; then
    echo ""$LP_ENV" and "$GSA_CRED" found."
else 
    echo ""$LP_ENV" and/or "$GSA_CRED" do not exist."
    exit 0
fi

# Update system postgresql postgresql-contrib  
sudo apt update
sudo apt upgrade -y
sudo apt-get install nginx libpq-dev build-essential ufw python3-dev python3-venv certbot python3-certbot-nginx -y

# Install virtual environment and requirements
python3 -m venv ../${VENV_NAME}
source ../${VENV_NAME}/bin/activate
pip install --upgrade wheel
pip install gunicorn psycopg2-binary
pip install -r requirements.txt

# Migrate project database and collect static files
python manage.py migrate 
python manage.py collectstatic 
mkdir ip2location

# Gunicorn setup
sudo mkdir /var/log/gunicorn
sudo PROJECT_DIR=${PROJECT_DIR} PROJECT_NAME=${PROJECT_NAME} VENV_NAME=${VENV_NAME} NWORKERS=${NWORKERS} envsubst < deploy/gunicorn.service > gunicorn.service
sudo mv gunicorn.service /etc/systemd/system/gunicorn.service
sudo systemctl start gunicorn
sudo systemctl enable gunicorn

# Nginx setup 
PROJECT_NAME=${WEBSITE_NAME} PROJECT_DIR=${PROJECT_DIR} DOMAIN=${DOMAIN} envsubst < deploy/nginx.conf > nginx.conf
sudo mv nginx.conf /etc/nginx/sites-available/${WEBSITE_NAME}
sudo ln -s /etc/nginx/sites-available/${WEBSITE_NAME} /etc/nginx/sites-enabled

# Allow HTTPS traffic and add SSL certificate with certbot
sudo ufw allow ssh
sudo ufw enable 
sudo ufw allow 'Nginx Full'
sudo ufw delete allow 'Nginx HTTP'
sudo certbot --nginx -d ${WEBSITE_NAME}.${DOMAIN} -d www.${WEBSITE_NAME}.${DOMAIN}

# Restart Gunicorn and Nginx
sudo systemctl restart gunicorn
sudo systemctl restart nginx