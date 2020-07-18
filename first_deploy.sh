#!/bin/bash

PROJECT_NAME='linuxpolls'
PROJECT_DIR=`pwd`
VENV_NAME='django_env'
NWORKERS=3

DOMAIN='me'

# Update system
sudo apt update
sudo apt upgrade -y
sudo apt-get install postgresql postgresql-contrib libpq-dev build-essential nginx python3-dev python3-venv certbot python3-certbot-nginx -y

# Install virtual environment and requirements
python3 -m venv ../${VENV_NAME}
source ../${VENV_NAME}/bin/activate
pip install --upgrade wheel
pip install gunicorn psycopg2-binary
pip install -r requirements.txt

# Migrate project database
python manage.py migrate 

# Gunicorn setup
sudo mkdir /var/log/gunicorn
sudo PROJECT_DIR=${PROJECT_DIR} PROJECT_NAME=${PROJECT_NAME} VENV_NAME=${VENV_NAME} NWORKERS=${NWORKERS} envsubst < deploy/gunicorn.service > gunicorn.service
sudo mv gunicorn.service /etc/systemd/system/gunicorn.service
sudo systemctl start gunicorn
sudo systemctl enable gunicorn

# Nginx setup
#sudo adduser $USER www-data  
sudo ../${VENV_NAME}/bin/python manage.py collectstatic 
PROJECT_NAME=${PROJECT_NAME} DOMAIN=${DOMAIN} envsubst < deploy/nginx.conf > nginx.conf
sudo mv nginx.conf /etc/nginx/sites-available/${PROJECT_NAME}
sudo ln -s /etc/nginx/sites-available/${PROJECT_NAME} /etc/nginx/sites-enabled
#sudo systemctl restart nginx
#sudo ufw allow 'Nginx Full'

# Allow HTTPS traffic and add SSL certificate with certbot
sudo ufw allow ssh
sudo ufw enable
sudo ufw allow 'Nginx Full'
sudo ufw delete allow 'Nginx HTTP'
sudo certbot --nginx -d ${PROJECT_NAME}.${DOMAIN} -d www.${PROJECT_NAME}.${DOMAIN}
sudo systemctl restart gunicorn
sudo systemctl restart nginx